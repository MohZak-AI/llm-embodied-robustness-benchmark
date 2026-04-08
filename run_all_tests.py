"""
run_all_tests.py
================
Master runner for all Group 7 LLM robustness tests.
Collects results from all 3 topics and saves to JSON report.

Usage:
    python run_all_tests.py
    python run_all_tests.py --output results/my_run.json
    python run_all_tests.py --topic 1     # run only topic 1
"""

import sys, json, argparse, os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_all(output_path: str = None, topic_filter: int = None):
    all_results = []
    timestamp = datetime.now().isoformat()

    print("\n" + "="*70)
    print("GROUP 7 — EMBODIED LLM ROBUSTNESS TEST SUITE")
    print("Survey: Song et al., 2026 (TMLR) — Section 5")
    print(f"Run time: {timestamp}")
    print("="*70)

    if topic_filter in (None, 1):
        print("\n[TOPIC 1] Visual Perception (Section 5.2)")
        try:
            from topic1_visual_perception.test_whoops import run_tests as t1a
            from topic1_visual_perception.test_blindtest import run_tests as t1b
            from topic1_visual_perception.test_spatial_relations import run_tests as t1c
        except ModuleNotFoundError:
            from test_whoops import run_tests as t1a
            from test_blindtest import run_tests as t1b
            from test_spatial_relations import run_tests as t1c
        all_results += t1a()
        all_results += t1b()
        all_results += t1c()

    if topic_filter in (None, 2):
        print("\n[TOPIC 2] Spatial and Tool-Use (Section 5.3)")
        try:
            from topic2_spatial_tool_use.test_spatialvlm_and_embodied import run_tests as t2
        except ModuleNotFoundError:
            from test_spatialvlm_and_embodied import run_tests as t2
        all_results += t2()

    if topic_filter in (None, 3):
        print("\n[TOPIC 3] Safety and Autonomy (Section 5.3)")
        try:
            from topic3_safety_autonomy.test_safety_autonomy import run_tests as t3
        except ModuleNotFoundError:
            from test_safety_autonomy import run_tests as t3
        all_results += t3()

    # ── Summary ──────────────────────────────────────────
    total = len(all_results)
    passed = sum(1 for r in all_results if r["passed"])

    print("\n" + "="*70)
    print("FINAL SUMMARY")
    print(f"Total tests: {total} | Passed: {passed} | Failed: {total - passed}")

    # Per-model breakdown
    models = sorted(set(r["model"] for r in all_results))
    print("\nPer-model results:")
    for model in models:
        model_r = [r for r in all_results if r["model"] == model]
        p = sum(1 for r in model_r if r["passed"])
        print(f"  {model:30s} {p:3d}/{len(model_r)}")

    # Per-failure-type breakdown
    failure_types = sorted(set(r["failure_type"] for r in all_results))
    print("\nPer-failure-type results:")
    for ft in failure_types:
        ft_r = [r for r in all_results if r["failure_type"] == ft]
        p = sum(1 for r in ft_r if r["passed"])
        print(f"  {ft:30s} {p:3d}/{len(ft_r)}")

    print("="*70)

    # ── Save ─────────────────────────────────────────────
    report = {
        "metadata": {
            "survey": "Song et al., 2026 — LLM Reasoning Failures (TMLR)",
            "group": 7,
            "topic": "Embodied Reasoning × Robustness",
            "timestamp": timestamp,
            "total_tests": total,
            "total_passed": passed,
        },
        "results": all_results
    }

    if not output_path:
        os.makedirs("results", exist_ok=True)
        output_path = f"results/group7_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    else:
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\nResults saved to: {output_path}")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, default=None, help="Output JSON path")
    parser.add_argument("--topic", type=int, default=None, choices=[1, 2, 3],
                        help="Run only a specific topic (1, 2, or 3)")
    args = parser.parse_args()
    run_all(args.output, args.topic)
