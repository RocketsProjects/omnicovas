"""
omnicovas.db.models

SQLAlchemy database models for OmniCOVAS persistent storage.

Two databases are maintained separately:
    - session DB: event history, sessions, metadata
    - galaxy DB: bulk imported data (Spansh dumps, etc.) — Phase 5+

This module defines the session DB schema only.

Law 8 (Sovereignty & Transparency):
    All data stays on the local machine. Commander can export or delete
    at any time. Database is a plain SQLite file they own.

See: Master Blueprint v4.0 Section 3 (Tech Stack)
See: Phase 1 Development Guide Week 3, Part B
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):  # type: ignore[misc]
    """Base class for all SQLAlchemy models."""

    pass


class Session(Base):
    """
    A commander session — from game launch to exit.

    Created on first event of a new journal file.
    """

    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    commander_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    ship_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    journal_filename: Mapped[str] = mapped_column(String(128), nullable=False)

    events: Mapped[list["JournalEvent"]] = relationship(
        "JournalEvent",
        back_populates="session",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<Session id={self.id} cmdr={self.commander_name} "
            f"ship={self.ship_type} started={self.start_time}>"
        )


class JournalEvent(Base):
    """
    One journal event from Elite Dangerous.

    Stores the raw JSON line for full replay/audit capability.
    This is the black box recorder for OmniCOVAS.
    """

    __tablename__ = "journal_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sessions.id"), nullable=False, index=True
    )
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    raw_json: Mapped[str] = mapped_column(Text, nullable=False)

    session: Mapped[Session] = relationship("Session", back_populates="events")

    def __repr__(self) -> str:
        return f"<JournalEvent id={self.id} type={self.event_type} ts={self.timestamp}>"
