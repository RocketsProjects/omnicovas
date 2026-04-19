"""
omnicovas.core.api_bridge

FastAPI HTTP and WebSocket bridge between the Python core and the Tauri UI.

Architecture:
    Python core (asyncio)
        → FastAPI on dynamic localhost port
            → Tauri webview (tauri://localhost)
                → HTTP polling for state
                → WebSocket subscription for live events

Law 6 (Performance Priority):
    - Non-blocking startup: FastAPI bound BEFORE ready signal emitted
    - Dynamic port selection avoids conflicts with other dev tools

Law 8 (Sovereignty & Transparency):
    - /state exposes current StateManager snapshot
    - /activity-log exposes recent dispatcher events
    - /health exposes basic runtime stats

See: Master Blueprint v4.0 Section 3 (Tech Stack)
See: Phase 1 Development Guide Week 5, Part A
"""

from __future__ import annotations

import asyncio
import logging
import socket
import time
from collections import deque
from typing import Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from omnicovas.core.state_manager import StateManager

logger = logging.getLogger(__name__)

ACTIVITY_LOG_CAPACITY = 1000


def find_free_port() -> int:
    """Bind to port 0 to let the OS pick a free port, then return it."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


class WebSocketBroadcaster:
    """
    Tracks active WebSocket clients and broadcasts messages to all of them.

    Handles client disconnection gracefully — a dead client never blocks
    broadcast to live clients.
    """

    def __init__(self) -> None:
        self._clients: set[WebSocket] = set()
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket) -> None:
        """Accept a new WebSocket connection."""
        await websocket.accept()
        async with self._lock:
            self._clients.add(websocket)
        logger.info("WebSocket client connected (%d total)", len(self._clients))

    async def disconnect(self, websocket: WebSocket) -> None:
        """Remove a WebSocket client."""
        async with self._lock:
            self._clients.discard(websocket)
        logger.info("WebSocket client disconnected (%d remaining)", len(self._clients))

    async def broadcast(self, message: dict[str, Any]) -> None:
        """Send a message to every connected client."""
        async with self._lock:
            clients = list(self._clients)

        dead: list[WebSocket] = []
        for client in clients:
            try:
                await client.send_json(message)
            except Exception as e:
                logger.debug("WebSocket send failed, dropping client: %s", e)
                dead.append(client)

        if dead:
            async with self._lock:
                for client in dead:
                    self._clients.discard(client)

    @property
    def client_count(self) -> int:
        """Number of currently connected WebSocket clients."""
        return len(self._clients)


class ApiBridge:
    """FastAPI application hosting the Python↔Tauri bridge."""

    def __init__(
        self,
        state_manager: StateManager,
        host: str = "127.0.0.1",
        port: int | None = None,
        resource_monitor: Any = None,
    ) -> None:
        self._state = state_manager
        self._host = host
        self._port = port if port is not None else find_free_port()
        self._resource_monitor = resource_monitor
        self._app = self._build_app()
        self._broadcaster = WebSocketBroadcaster()
        self._activity_log: deque[dict[str, Any]] = deque(maxlen=ACTIVITY_LOG_CAPACITY)
        self._server_task: asyncio.Task[None] | None = None
        self._started_at: float | None = None
        self._events_counter = 0
        self._ready_event = asyncio.Event()

    @property
    def port(self) -> int:
        """The port this bridge is configured to bind to."""
        return self._port

    @property
    def host(self) -> str:
        """The host this bridge is bound to (default 127.0.0.1)."""
        return self._host

    def _build_app(self) -> FastAPI:
        """Build the FastAPI application with routes and middleware."""
        app = FastAPI(
            title="OmniCOVAS Core API",
            description="Internal bridge between Python core and Tauri UI",
            version="0.1.0",
        )

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=False,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @app.get("/health")  # type: ignore[misc,untyped-decorator,unused-ignore]
        async def health() -> dict[str, Any]:
            """Liveness probe + runtime stats."""
            uptime = 0.0
            if self._started_at is not None:
                uptime = time.monotonic() - self._started_at
            return {
                "status": "ok",
                "version": "0.1.0",
                "uptime_seconds": int(uptime),
                "events_processed": self._events_counter,
                "websocket_clients": self._broadcaster.client_count,
            }

        @app.get("/state")  # type: ignore[misc,untyped-decorator,unused-ignore]
        async def get_state() -> dict[str, Any]:
            """Current StateManager snapshot."""
            return self._state.public_snapshot()

        @app.get("/activity-log")  # type: ignore[misc,untyped-decorator,unused-ignore]
        async def get_activity_log() -> dict[str, Any]:
            """Recent events seen by the dispatcher."""
            return {
                "total": len(self._activity_log),
                "entries": list(self._activity_log),
            }

        @app.get("/resources")  # type: ignore[misc,untyped-decorator,unused-ignore]
        async def get_resources() -> dict[str, Any]:
            """Live resource usage snapshot (Principle 10)."""
            if self._resource_monitor is None:
                return {"enabled": False}

            latest = self._resource_monitor.latest
            budget = self._resource_monitor.budget
            return {
                "enabled": True,
                "snapshot": (
                    {
                        "memory_used_mb": round(latest.memory_used_mb, 1),
                        "memory_total_mb": round(latest.memory_total_mb, 1),
                        "cpu_percent": round(latest.cpu_percent, 1),
                        "disk_free_gb": round(latest.disk_free_gb, 1),
                        "disk_total_gb": round(latest.disk_total_gb, 1),
                    }
                    if latest is not None
                    else None
                ),
                "budget": {
                    "max_cache_size_mb": budget.max_cache_size_mb,
                    "max_galaxy_dump_size_gb": budget.max_galaxy_dump_size_gb,
                    "max_background_task_cpu_percent": (
                        budget.max_background_task_cpu_percent
                    ),
                    "max_api_calls_per_minute_total": (
                        budget.max_api_calls_per_minute_total
                    ),
                },
            }

        @app.websocket("/ws/events")  # type: ignore[misc,untyped-decorator,unused-ignore]
        async def ws_events(websocket: WebSocket) -> None:
            """Push live events to connected clients."""
            await self._broadcaster.connect(websocket)
            try:
                await websocket.send_json(
                    {"type": "initial_state", "state": self._state.public_snapshot()}
                )
                while True:
                    await websocket.receive_text()
            except WebSocketDisconnect:
                pass
            except Exception as e:
                logger.debug("WebSocket closed: %s", e)
            finally:
                await self._broadcaster.disconnect(websocket)

        return app

    async def push_event(self, event: dict[str, Any]) -> None:
        """Record an event and broadcast it."""
        entry = {
            "timestamp": event.get("timestamp"),
            "event_type": event.get("event", "Unknown"),
            "summary": self._summarize(event),
        }
        self._activity_log.append(entry)
        self._events_counter += 1

        await self._broadcaster.broadcast({"type": "event", "event": entry})

    def _summarize(self, event: dict[str, Any]) -> str:
        """Build a short human-readable summary of an event for the log."""
        event_type = event.get("event", "Unknown")
        if event_type == "FSDJump":
            return f"Jump → {event.get('StarSystem', '?')}"
        if event_type == "Docked":
            return f"Docked at {event.get('StationName', '?')}"
        if event_type == "Undocked":
            return f"Undocked from {event.get('StationName', '?')}"
        if event_type == "HullDamage":
            hp = event.get("Health", 0.0)
            return f"Hull damage → {hp * 100:.1f}%"
        if event_type == "Status":
            return "Status update"
        return str(event_type)

    async def start(self) -> None:
        """Launch the uvicorn server in the background."""
        import uvicorn

        config = uvicorn.Config(
            app=self._app,
            host=self._host,
            port=self._port,
            log_level="warning",
            access_log=False,
        )
        server = uvicorn.Server(config)

        async def run() -> None:
            await server.serve()

        self._server_task = asyncio.create_task(run())
        self._started_at = time.monotonic()

        for _ in range(50):
            await asyncio.sleep(0.1)
            if server.started:
                self._ready_event.set()
                logger.info("ApiBridge ready at http://%s:%d", self._host, self._port)
                return

        logger.error("ApiBridge failed to start within 5s")

    async def wait_until_ready(self, timeout: float = 5.0) -> bool:
        """Block until the server has bound, or timeout expires."""
        try:
            await asyncio.wait_for(self._ready_event.wait(), timeout=timeout)
            return True
        except asyncio.TimeoutError:
            return False

    async def stop(self) -> None:
        """Stop the server gracefully."""
        if self._server_task is not None:
            self._server_task.cancel()
            try:
                await self._server_task
            except asyncio.CancelledError:
                pass
            self._server_task = None
            logger.info("ApiBridge stopped.")

    @property
    def activity_log(self) -> list[dict[str, Any]]:
        """Read-only view of the activity log ring buffer."""
        return list(self._activity_log)
