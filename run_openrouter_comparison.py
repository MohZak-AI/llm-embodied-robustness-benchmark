import json
import os
from collections import defaultdict
from datetime import datetime

from config import MODELS

import test_whoops as whoops
import test_blindtest as blindtest
import test_spatial_relations as spatial_relations
import test_spatialvlm_and_embodied as spatial_tool
import test_safety_autonomy as safety


COMPARISON_MODELS = [
    "gpt-4o",
    "gpt-5",
    "gpt-5-mini",
    "o3-mini",
    "claude-sonnet-4-6",
    "claude-3-7-sonnet",
    "claude-3-5-haiku",
    "gemini-2-5-pro",
    "gemini-3-1-pro",
    "llama-3-3-70b",
    "qwen3-next-80b",
    "deepseek-r1",
]

GROUPS = {
    "new_frontier": ["gpt-5", "claude-sonnet-4-6", "gemini-3-1-pro"],
    "legacy_frontier": ["gpt-4o", "claude-3-7-sonnet", "gemini-2-5-pro"],
    "compact_reasoning": ["gpt-5-mini", "claude-3-5-haiku", "o3-mini"],
    "open_source": ["llama-3-3-70b", "qwen3-next-80b", "deepseek-r1"],
}


def infer_topic(test_id: str) -> int:
    if test_id.startswith(("whoops_", "blindtest_", "liu2023_", "campbell2025_", "zhao2024_")):
        return 1
    if test_id.startswith(("spatialvlm_", "mecattaf2024_", "xu2023_", "guran2024_", "dao2025_")):
        return 2
    return 3


def expected_test_ids() -> list[str]:
    ids = []
    ids += [t["id"] for t in whoops.WHOOPS_TEXT_PROXY_TESTS]
    ids += [t["id"] for t in blindtest.BLINDTEST_CASES]
    ids += [t["id"] for t in spatial_relations.LIU2023_TESTS]
    ids += [t["id"] for t in spatial_relations.CAMPBELL2025_TESTS]
    ids += [t["id"] for t in spatial_relations.ZHAO2024_TESTS]
    ids += [t["id"] for t in spatial_relations.ZHOU2023_TESTS]
    ids += [t["id"] for t in spatial_tool.CHEN2024_TESTS]
    ids += [t["id"] for t in spatial_tool.MECATTAF2024_TESTS]
    ids += [t["id"] for t in spatial_tool.XU2023_TESTS]
    ids += [t["id"] for t in spatial_tool.GURAN2024_TESTS]
    ids += [t["id"] for t in spatial_tool.DAO2025_TESTS]
    ids += [t["id"] for t in safety.LIANG2023_TESTS]
    ids += [t["id"] for t in safety.ZHANG2024_TESTS]
    ids += [t["id"] for t in safety.REZAEI2025_TESTS]
    return ids


def configure_models(models: list[str]):
    missing = [m for m in models if m not in MODELS]
    if missing:
        raise ValueError(f"Missing model keys in config.MODELS: {missing}")

    whoops.MODELS_TO_TEST = models.copy()
    blindtest.MODELS_TO_TEST = models.copy()
    spatial_relations.MODELS_TO_TEST = models.copy()
    spatial_tool.MODELS_TO_TEST = models.copy()
    spatial_tool.REASONING_MODELS = models.copy()
    safety.MODELS_TO_TEST = models.copy()
    safety.ALL_MODELS = models.copy()


def pairwise_compare(results: list[dict], model_a: str, model_b: str) -> dict:
    by_a = {r["test_id"]: r for r in results if r["model"] == model_a}
    by_b = {r["test_id"]: r for r in results if r["model"] == model_b}
    common = sorted(set(by_a.keys()) & set(by_b.keys()))
    if not common:
        return {
            "common_tests": 0,
            "a_pass": 0,
            "b_pass": 0,
            "a_rate": 0.0,
            "b_rate": 0.0,
            "delta": 0.0,
        }

    a_pass = sum(1 for t in common if by_a[t]["passed"])
    b_pass = sum(1 for t in common if by_b[t]["passed"])
    a_rate = a_pass / len(common)
    b_rate = b_pass / len(common)
    return {
        "common_tests": len(common),
        "a_pass": a_pass,
        "b_pass": b_pass,
        "a_rate": a_rate,
        "b_rate": b_rate,
        "delta": a_rate - b_rate,
    }


def summarize(results: list[dict], models: list[str], expected_ids: list[str]) -> dict:
    unique_expected = sorted(set(expected_ids))
    expected_per_model = len(unique_expected)

    by_model = {}
    for m in models:
        model_results = [r for r in results if r["model"] == m]
        passed = sum(1 for r in model_results if r["passed"])
        logged = len(model_results)
        by_model[m] = {
            "passed": passed,
            "logged": logged,
            "expected": expected_per_model,
            "pass_rate_logged": (passed / logged) if logged else 0.0,
            "coverage": (logged / expected_per_model) if expected_per_model else 0.0,
            "effective_rate": (passed / expected_per_model) if expected_per_model else 0.0,
        }

    by_topic = defaultdict(lambda: defaultdict(lambda: {"passed": 0, "logged": 0}))
    for r in results:
        t = infer_topic(r["test_id"])
        by_topic[t][r["model"]]["logged"] += 1
        by_topic[t][r["model"]]["passed"] += int(r["passed"])

    by_failure = defaultdict(lambda: defaultdict(lambda: {"passed": 0, "logged": 0}))
    for r in results:
        f = r["failure_type"]
        by_failure[f][r["model"]]["logged"] += 1
        by_failure[f][r["model"]]["passed"] += int(r["passed"])

    test_stats = defaultdict(lambda: {"passed": 0, "logged": 0})
    for r in results:
        test_stats[r["test_id"]]["logged"] += 1
        test_stats[r["test_id"]]["passed"] += int(r["passed"])
    hardest = sorted(
        [
            {
                "test_id": t,
                "passed": s["passed"],
                "logged": s["logged"],
                "failures": s["logged"] - s["passed"],
                "pass_rate": (s["passed"] / s["logged"]) if s["logged"] else 0.0,
            }
            for t, s in test_stats.items()
        ],
        key=lambda x: (x["pass_rate"], -x["failures"]),
    )

    group_stats = {}
    for g, members in GROUPS.items():
        vals = [by_model[m] for m in members if m in by_model]
        if not vals:
            group_stats[g] = {"avg_effective": 0.0, "avg_logged": 0.0, "avg_coverage": 0.0}
            continue
        group_stats[g] = {
            "avg_effective": sum(v["effective_rate"] for v in vals) / len(vals),
            "avg_logged": sum(v["pass_rate_logged"] for v in vals) / len(vals),
            "avg_coverage": sum(v["coverage"] for v in vals) / len(vals),
        }

    return {
        "overall": {
            "results_logged": len(results),
            "passed": sum(1 for r in results if r["passed"]),
            "failed": sum(1 for r in results if not r["passed"]),
            "expected_calls": expected_per_model * len(models),
            "expected_per_model": expected_per_model,
        },
        "by_model": by_model,
        "by_topic": {str(k): dict(v) for k, v in by_topic.items()},
        "by_failure": {k: dict(v) for k, v in by_failure.items()},
        "hardest_tests": hardest[:12],
        "group_stats": group_stats,
        "pairwise": {
            "gpt5_vs_gpt4o": pairwise_compare(results, "gpt-5", "gpt-4o"),
            "claude46_vs_claude37": pairwise_compare(results, "claude-sonnet-4-6", "claude-3-7-sonnet"),
            "gemini31_vs_gemini25": pairwise_compare(results, "gemini-3-1-pro", "gemini-2-5-pro"),
        },
    }


def write_readme(path: str, models: list[str], summary: dict, json_path: str):
    lines = []
    lines.append("# OpenRouter Comparative Benchmark Report")
    lines.append("")
    lines.append(f"Generated: {datetime.now().isoformat()}")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(
        f"This report runs the full Group 7 robustness suite ({summary['overall']['expected_per_model']} tasks) "
        "across a mixed set of frontier, compact, and open-source models through OpenRouter."
    )
    lines.append("")
    lines.append("Models evaluated:")
    for m in models:
        lines.append(f"- `{m}` -> `{MODELS[m].get('openrouter_model_id', MODELS[m]['model_id'])}`")
    lines.append("")

    overall = summary["overall"]
    lines.append("## High-Level Results")
    lines.append("")
    lines.append(f"- Logged results: **{overall['results_logged']}**")
    lines.append(f"- Passed: **{overall['passed']}**")
    lines.append(f"- Failed: **{overall['failed']}**")
    lines.append(
        f"- Expected call volume ({overall['expected_per_model']} tests x {len(models)} models): "
        f"**{overall['expected_calls']}**"
    )
    lines.append(f"- Coverage ratio: **{overall['results_logged'] / overall['expected_calls']:.1%}**")
    lines.append(f"- Raw JSON: `{json_path}`")
    lines.append("")

    lines.append("## Per-Model Statistics")
    lines.append("")
    lines.append("| Model | Passed | Logged | Expected | Pass Rate (logged) | Coverage | Effective Pass |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for m, s in sorted(summary["by_model"].items(), key=lambda kv: kv[1]["effective_rate"], reverse=True):
        lines.append(
            f"| `{m}` | {s['passed']} | {s['logged']} | {s['expected']} | {s['pass_rate_logged']:.1%} | {s['coverage']:.1%} | {s['effective_rate']:.1%} |"
        )
    lines.append("")

    lines.append("## New vs Older Model Comparison")
    lines.append("")
    pair_labels = {
        "gpt5_vs_gpt4o": ("gpt-5", "gpt-4o"),
        "claude46_vs_claude37": ("claude-sonnet-4-6", "claude-3-7-sonnet"),
        "gemini31_vs_gemini25": ("gemini-3-1-pro", "gemini-2-5-pro"),
    }
    lines.append("| Pair | Common Tests | Newer Pass Rate | Older Pass Rate | Delta |")
    lines.append("|---|---:|---:|---:|---:|")
    for key, (newer, older) in pair_labels.items():
        p = summary["pairwise"][key]
        lines.append(
            f"| `{newer}` vs `{older}` | {p['common_tests']} | {p['a_rate']:.1%} | {p['b_rate']:.1%} | {p['delta']:+.1%} |"
        )
    lines.append("")

    lines.append("## Group Averages")
    lines.append("")
    lines.append("| Group | Avg Effective Pass | Avg Pass (logged) | Avg Coverage |")
    lines.append("|---|---:|---:|---:|")
    for g, s in summary["group_stats"].items():
        lines.append(
            f"| `{g}` | {s['avg_effective']:.1%} | {s['avg_logged']:.1%} | {s['avg_coverage']:.1%} |"
        )
    lines.append("")

    lines.append("## Topic-Level Performance")
    lines.append("")
    lines.append("| Topic | Passed | Logged | Pass Rate |")
    lines.append("|---|---:|---:|---:|")
    topic_names = {"1": "Topic 1 (Visual Perception)", "2": "Topic 2 (Spatial and Tool-Use)", "3": "Topic 3 (Safety and Autonomy)"}
    for t in ["1", "2", "3"]:
        entries = summary["by_topic"].get(t, {})
        passed = sum(v["passed"] for v in entries.values())
        logged = sum(v["logged"] for v in entries.values())
        rate = (passed / logged) if logged else 0.0
        lines.append(f"| {topic_names[t]} | {passed} | {logged} | {rate:.1%} |")
    lines.append("")

    lines.append("## Failure-Type Performance")
    lines.append("")
    lines.append("| Failure Type | Passed | Logged | Pass Rate |")
    lines.append("|---|---:|---:|---:|")
    for ft, entries in sorted(summary["by_failure"].items()):
        passed = sum(v["passed"] for v in entries.values())
        logged = sum(v["logged"] for v in entries.values())
        rate = (passed / logged) if logged else 0.0
        lines.append(f"| `{ft}` | {passed} | {logged} | {rate:.1%} |")
    lines.append("")

    lines.append("## Hardest Tests Across Models")
    lines.append("")
    lines.append("| Test ID | Passed | Logged | Pass Rate |")
    lines.append("|---|---:|---:|---:|")
    for t in summary["hardest_tests"]:
        lines.append(f"| `{t['test_id']}` | {t['passed']} | {t['logged']} | {t['pass_rate']:.1%} |")
    lines.append("")

    lines.append("## Interpretation")
    lines.append("")
    lines.append("- **Improvement signal:** compare pairwise deltas; positive delta indicates newer model outperforms the older model on overlapping successful calls.")
    lines.append("- **Robustness caution:** a high logged pass rate with low coverage can mask provider unavailability/rate limits.")
    lines.append("- **Failure concentration:** low-pass tests indicate persistent weaknesses in compositional planning, spatial binding, and prompt sensitivity.")
    lines.append("- **Scientific takeaway:** this is a live systems benchmark; results combine capability and reliability (availability + correctness).")

    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")


def main():
    if not os.getenv("OPENROUTER_API_KEY"):
        raise RuntimeError("OPENROUTER_API_KEY is required for this comparison runner")

    configure_models(COMPARISON_MODELS)
    expected_ids = expected_test_ids()

    print("\n" + "=" * 72)
    print("OPENROUTER COMPARATIVE ROBUSTNESS RUN")
    print("=" * 72)
    print(f"Models: {COMPARISON_MODELS}")
    print(f"Expected tests per model: {len(set(expected_ids))}")
    print("=" * 72)

    results = []
    results += whoops.run_tests()
    results += blindtest.run_tests()
    results += spatial_relations.run_tests()
    results += spatial_tool.run_tests()
    results += safety.run_tests()

    os.makedirs("results", exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = f"results/openrouter_comparison_{stamp}.json"
    readme_path = "README_OPENROUTER_COMPARISON.md"

    summary = summarize(results, COMPARISON_MODELS, expected_ids)
    payload = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "runner": "run_openrouter_comparison.py",
            "models": COMPARISON_MODELS,
            "expected_test_ids": sorted(set(expected_ids)),
        },
        "summary": summary,
        "results": results,
    }

    with open(json_path, "w") as f:
        json.dump(payload, f, indent=2)

    write_readme(readme_path, COMPARISON_MODELS, summary, json_path)
    print(f"\nComparison JSON saved to: {json_path}")
    print(f"Comparison README saved to: {readme_path}")


if __name__ == "__main__":
    main()
