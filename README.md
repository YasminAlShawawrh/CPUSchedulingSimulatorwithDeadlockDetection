# CPU Scheduling Simulator with Deadlock Detection

A simulation of a CPU scheduling system using Priority Scheduling with Round Robin, combined with deadlock detection and recovery mechanisms.

The system models:
- Process execution (CPU and I/O bursts)
- Resource allocation and release
- Deadlock detection and handling
- Performance metrics (waiting time, turnaround time)

---

## Table of contents

- [Overview](#overview)
- [Features](#features)
- [Input format](#input-format)
- [Scheduling algorithm](#scheduling-algorithm)
- [Deadlock handling](#deadlock-handling)
- [Key Functions](#key-functions)
- [Example scenarios](#example-scenarios)
- [Limitations](#Limitations)
- [Future improvements](#future-improvements)

---

## Overview

This project simulates a single CPU system that executes multiple processes with:
- Arrival times
- Priorities
- CPU and I/O bursts
- Resource requests and releases

The simulation:
1. Schedules processes using Priority and Round Robin
2. Manages resource allocation
3. Detects deadlocks
4. Recovers from deadlocks
5. Computes performance metrics

---

## Features

- Priority-based Round Robin scheduling
- Time-based CPU simulation
- Resource management (R[i], F[i])
- Deadlock detection
- Deadlock recovery (process abortion)
- Waiting time and turnaround time calculation
- Multiple test scenarios (with and without deadlock)

---

## Input format

Each process is defined in a text file:

PID    Arrival Time    Priority    CPU/IO Sequence

Example:
0 0 1 CPU {R[1], 50, F[1]}
1 5 1 CPU {20} IO{30} CPU{20, R[2], 30, F[2], 10}

### Meaning:
- `R[i]` → Request resource
- `F[i]` → Release resource
- Numbers → CPU execution time
- `IO{x}` → I/O burst

---

## Scheduling algorithm

### Priority + Round Robin

- Processes sorted by:
  - Arrival Time
  - Priority
- Same-priority processes handled using **Round Robin**
- Time quantum = **10 units**

 Behavior:
- Preemption occurs after time quantum
- Processes re-enter ready queue if not finished
- I/O bursts move processes temporarily out of CPU

---

## Deadlock handling

### Detection

- Monitors resource allocation
- Detects if processes are stuck waiting

 Logic:
- If multiple processes wait for unavailable resources → deadlock

---

### Recovery

- Abort one process
- Release its resources
- Reinsert process later with updated arrival time

Example (from output):
- Deadlock detected on `R[1]`
- Process aborted and rescheduled later :contentReference[oaicite:1]{index=1}  

---

## Key Functions

### `parse_process_file()`
- Reads and parses input file
- Converts bursts into structured format

---

### `simulate_priority_round_robin()`
- Main scheduler
- Handles:
  - Process selection
  - Execution
  - I/O transitions
  - Metrics calculation

---

### `round_robin_scheduling()`
- Handles equal-priority processes
- Applies time quantum

---

### `detect_deadlock()`
- Checks resource contention
- Identifies deadlock conditions

---

### `handle_deadlock()`
- Aborts process
- Releases resources
- Restarts scheduling

---

##  Example scenarios

### Without Deadlock
- Processes execute normally
- CPU and I/O alternate correctly

### With Deadlock
- Multiple processes request same resources
- System detects and resolves deadlock


## Limitations

- Single CPU only
- No graphical Gantt chart
- Basic deadlock recovery (process termination)
- No synchronization needed (single-threaded)

---

## Future improvements

- Add Gantt chart visualization
- Implement advanced deadlock recovery
- Support multiple CPUs
- Add more scheduling algorithms
- Build a graphical interface

---


