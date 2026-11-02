#!/usr/bin/env python3
"""
Eval Dashboard — Score Agent Performance

Tracks agent runs with accuracy, cost, and latency metrics.
Stores results in JSON and displays a summary dashboard.

Usage:
    python eval_dashboard.py --record --agent support-agent --task "refund question" --accuracy 0.95 --cost 0.002 --latency 1.5
    python eval_dashboard.py --report
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

DATA_FILE = Path(__file__).parent / "eval_results.json"


def load_results() -> list:
    """Load all eval results."""
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE) as f:
        return json.load(f)


def save_results(results: list):
    """Save eval results."""
    with open(DATA_FILE, "w") as f:
        json.dump(results, f, indent=2)


def record_run(agent: str, task: str, accuracy: float, cost: float, latency: float, notes: str = ""):
    """Record a single agent evaluation run."""
    results = load_results()
    entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": agent,
        "task": task,
        "accuracy": round(accuracy, 4),
        "cost": round(cost, 6),
        "latency": round(latency, 2),
        "notes": notes,
    }
    results.append(entry)
    save_results(results)
    print(f"[+] Recorded: {agent} | {task} | acc={accuracy} | cost=${cost} | lat={latency}s")


def generate_report() -> dict:
    """Generate summary statistics from all results."""
    results = load_results()
    if not results:
        return {"message": "No eval results yet"}

    agents = {}
    for r in results:
        a = r["agent"]
        if a not in agents:
            agents[a] = {"runs": 0, "total_acc": 0, "total_cost": 0, "total_lat": 0}
        agents[a]["runs"] += 1
        agents[a]["total_acc"] += r["accuracy"]
        agents[a]["total_cost"] += r["cost"]
        agents[a]["total_lat"] += r["latency"]

    report = {
        "total_runs": len(results),
        "agents": {},
    }
    for a, stats in agents.items():
        report["agents"][a] = {
            "runs": stats["runs"],
            "avg_accuracy": round(stats["total_acc"] / stats["runs"], 4),
            "total_cost": round(stats["total_cost"], 4),
            "avg_latency": round(stats["total_lat"] / stats["runs"], 2),
        }

    # Overall stats
    report["overall"] = {
        "avg_accuracy": round(sum(r["accuracy"] for r in results) / len(results), 4),
        "total_cost": round(sum(r["cost"] for r in results), 4),
        "avg_latency": round(sum(r["latency"] for r in results) / len(results), 2),
    }
    return report


def print_report():
    """Print the eval dashboard report."""
    report = generate_report()

    if "message" in report:
        print(report["message"])
        return

    print("=" * 60)
    print("EVAL DASHBOARD — Agent Performance Report")
    print("=" * 60)
    print(f"\nTotal runs: {report['total_runs']}")
    print(f"\nOverall: avg_accuracy={report['overall']['avg_accuracy']} | "
          f"total_cost=${report['overall']['total_cost']} | "
          f"avg_latency={report['overall']['avg_latency']}s")

    print(f"\n{'Agent':<25} {'Runs':<6} {'Avg Acc':<10} {'Total Cost':<12} {'Avg Lat':<10}")
    print("-" * 60)
    for agent, stats in report["agents"].items():
        print(f"{agent:<25} {stats['runs']:<6} {stats['avg_accuracy']:<10} "
              f"${stats['total_cost']:<11} {stats['avg_latency']:<10}s")

    print("\nRecent runs:")
    results = load_results()
    for r in results[-5:]:
        print(f"  {r['timestamp'][:19]} | {r['agent']:<20} | {r['task']:<30} | acc={r['accuracy']}")


def main():
    parser = argparse.ArgumentParser(description="Eval Dashboard")
    parser.add_argument("--record", action="store_true", help="Record a new eval run")
    parser.add_argument("--report", action="store_true", help="Show the report")
    parser.add_argument("--agent", help="Agent name")
    parser.add_argument("--task", help="Task description")
    parser.add_argument("--accuracy", type=float, help="Accuracy score (0-1)")
    parser.add_argument("--cost", type=float, help="Cost in dollars")
    parser.add_argument("--latency", type=float, help="Latency in seconds")
    parser.add_argument("--notes", default="", help="Notes")
    args = parser.parse_args()

    if args.report:
        print_report()
    elif args.record:
        if not all([args.agent, args.task, args.accuracy is not None, args.cost is not None, args.latency is not None]):
            print("[-] --record requires --agent, --task, --accuracy, --cost, --latency")
            return
        record_run(args.agent, args.task, args.accuracy, args.cost, args.latency, args.notes)
    else:
        print("Use --record or --report")


if __name__ == "__main__":
    main()