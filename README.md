# eval-dashboard

Accuracy / cost / latency scoring for agent runs.

A lightweight harness for tracking how an agent performs over time across the three numbers that actually decide whether it's production-ready: is it right, what does it cost, and how fast is it.

## How it works

1. **Record** — log each agent run with its task, accuracy score, cost, and latency.
2. **Store** — append-only JSON log (`eval_results.json`), so history is never overwritten.
3. **Report** — aggregate view: per-agent averages, trend over time, worst-performing task categories.

## Usage

```bash
python eval_dashboard.py --record --agent support-agent --task "refund question" --accuracy 0.95 --cost 0.002 --latency 1.5
python eval_dashboard.py --report
```

## Why this exists

"It works in the demo" isn't an eval. This is the smallest possible harness that turns agent testing into numbers you can track across versions, so a regression shows up as a number dropping instead of a vibe changing.

## Stack

Python · JSON-backed storage, no external dependencies
