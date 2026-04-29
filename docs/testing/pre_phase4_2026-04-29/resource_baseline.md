# Section 8 — Resource / Performance Baseline

**Status:** NOT RUN
**Reason:** Manual monitoring test requires running app in interactive mode and observing resource usage. This verification playbook is executed in a server environment without GUI support.

## Test Intent

Capture baseline CPU, memory, and event latency metrics before Phase 4 combat features add load.

---

## Deferred Measurement Checklist

Three scenarios to measure:

### Scenario A: Idle App, No Elite

- [ ] App running, no events
- [ ] Record CPU %
- [ ] Record Memory MB
- [ ] Idle for 5 minutes, observe drift

### Scenario B: App + Elite Running

- [ ] Elite Dangerous running (borderless fullscreen)
- [ ] OmniCOVAS running, connected
- [ ] Record CPU %
- [ ] Record Memory MB
- [ ] Idle for 5 minutes

### Scenario C: App + Elite + Overlay Visible + Replay/Load

- [ ] Elite running with OmniCOVAS overlay visible
- [ ] Phase 2 replay running (events streaming)
- [ ] Record CPU %
- [ ] Record Memory MB
- [ ] Duration: 10 minutes
- [ ] Record WebSocket reconnects (should be 0)
- [ ] Record any latency warnings in logs

---

## Resource Budget Targets

From `resource_budget.yaml`:

| Metric | Target | Tolerance |
|--------|--------|-----------|
| Idle CPU | <15% | ±5% |
| Active CPU (overlay visible) | <40% | ±10% |
| Memory (base) | <200 MB | ±50 MB |
| Memory (with Elite) | <300 MB | ±50 MB |
| Event latency | <100 ms | ±20 ms |
| WebSocket reconnects | 0 per session | 1 is warning |

---

## Suggested Log Files

Save monitoring output to:
- `logs/resource_idle.txt` — Task Manager snapshot or PowerShell monitoring
- `logs/resource_elite_running.txt` — Resource usage while Elite plays
- `logs/resource_overlay_replay.txt` — Resource usage during replay stress

## Notes for Manual Tester

### Monitoring Methods

**Option 1: Task Manager (GUI)**
1. Open Task Manager (Ctrl+Shift+Esc)
2. Columns → Add: CPU %, Memory, Disk writes/sec
3. Watch `omnicovas.exe` rows
4. Take screenshots or copy data to log file

**Option 2: PowerShell (Automated)**
```powershell
# Monitor for 10 minutes, sample every 5 seconds
$outputFile = "logs/resource_overlay_replay.txt"
Get-Process omnicovas | Select-Object Name, CPU, WorkingSet |
  Out-File $outputFile
foreach ($i in 1..120) {
  Start-Sleep -Seconds 5
  Get-Process omnicovas | Select-Object Name, CPU, WorkingSet |
    Out-File $outputFile -Append
}
```

**Option 3: Windows Performance Monitor**
1. perfmon.exe
2. Add counters for process "omnicovas.exe": CPU %, Memory
3. Monitor for full test duration
4. Export data

### Scenario A: Idle App (5 minutes)

```
Time (HH:MM:SS) | CPU % | Memory MB | Notes
00:00:00        | 0.5   | 120       | App just started
00:01:00        | 0.2   | 125       | Stable
00:02:00        | 0.1   | 125       | Idle
00:03:00        | 0.3   | 126       | Background task?
00:04:00        | 0.1   | 125       | Stable
00:05:00        | 0.2   | 126       | Final snapshot
```

**Expected:** CPU idle <0.5%, memory stable ±1 MB

### Scenario B: App + Elite (5 minutes)

```
Time (HH:MM:SS) | CPU % | Memory MB | Notes
00:00:00        | 15    | 150       | Elite just started
00:01:00        | 8     | 160       | Elite running
00:02:00        | 5     | 165       | Stable
00:03:00        | 6     | 165       | Game loop
00:04:00        | 7     | 165       | Stable
00:05:00        | 5     | 166       | Final snapshot
```

**Expected:** CPU <15%, memory <300 MB

### Scenario C: App + Elite + Replay (10 minutes)

```
Time (HH:MM:SS) | CPU % | Memory MB | Latency ms | WebSocket reconnects
00:00:00        | 25    | 180       | 45         | 0
00:01:00        | 30    | 185       | 55         | 0
00:02:00        | 28    | 188       | 60         | 0
... (continue sampling every 60s)
00:10:00        | 32    | 192       | 65         | 0
```

**Expected:**
- CPU: 20–40% (replay adds load)
- Memory: <300 MB, no climbing
- Latency: <100 ms consistently
- Reconnects: 0

---

## Phase 4 Dependency

Phase 4 will add combat event processing, threat scoring, and overlay alerts. If baseline already exceeds budget, Phase 4 optimizations will be required. If baseline is clean, Phase 4 has headroom.

---

**Mark as PASS or FAIL in manual_test_verdict.md after performing this test.**

Attach captured data to: `logs/resource_*.txt` (not in git)
