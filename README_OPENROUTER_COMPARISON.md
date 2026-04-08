# OpenRouter Comparative Benchmark Report

Generated: 2026-04-07T18:16:24.122610

## Scope

This report runs the full Group 7 robustness suite (54 tasks) across a mixed set of frontier, compact, and open-source models through OpenRouter.

Models evaluated:
- `gpt-4o` -> `openai/gpt-4o`
- `gpt-5` -> `openai/gpt-5.4`
- `gpt-5-mini` -> `openai/gpt-5.4-mini`
- `o3-mini` -> `openai/o3-mini`
- `claude-sonnet-4-6` -> `anthropic/claude-sonnet-4.6`
- `claude-3-7-sonnet` -> `anthropic/claude-3.7-sonnet`
- `claude-3-5-haiku` -> `anthropic/claude-3.5-haiku`
- `gemini-2-5-pro` -> `google/gemini-2.5-pro`
- `gemini-3-1-pro` -> `google/gemini-3.1-pro-preview`
- `llama-3-3-70b` -> `meta-llama/llama-3.3-70b-instruct`
- `qwen3-next-80b` -> `qwen/qwen3-next-80b-a3b-instruct`
- `deepseek-r1` -> `deepseek/deepseek-r1`

## High-Level Results

- Logged results: **648**
- Passed: **501**
- Failed: **147**
- Expected call volume (54 tests x 12 models): **648**
- Coverage ratio: **100.0%**
- Raw JSON: `results/openrouter_comparison_20260407_181624.json`

## Per-Model Statistics

| Model | Passed | Logged | Expected | Pass Rate (logged) | Coverage | Effective Pass |
|---|---:|---:|---:|---:|---:|---:|
| `gpt-5-mini` | 50 | 54 | 54 | 92.6% | 100.0% | 92.6% |
| `gpt-5` | 49 | 54 | 54 | 90.7% | 100.0% | 90.7% |
| `claude-3-5-haiku` | 46 | 54 | 54 | 85.2% | 100.0% | 85.2% |
| `qwen3-next-80b` | 46 | 54 | 54 | 85.2% | 100.0% | 85.2% |
| `gpt-4o` | 45 | 54 | 54 | 83.3% | 100.0% | 83.3% |
| `claude-sonnet-4-6` | 45 | 54 | 54 | 83.3% | 100.0% | 83.3% |
| `claude-3-7-sonnet` | 45 | 54 | 54 | 83.3% | 100.0% | 83.3% |
| `llama-3-3-70b` | 44 | 54 | 54 | 81.5% | 100.0% | 81.5% |
| `deepseek-r1` | 44 | 54 | 54 | 81.5% | 100.0% | 81.5% |
| `o3-mini` | 39 | 54 | 54 | 72.2% | 100.0% | 72.2% |
| `gemini-3-1-pro` | 36 | 54 | 54 | 66.7% | 100.0% | 66.7% |
| `gemini-2-5-pro` | 12 | 54 | 54 | 22.2% | 100.0% | 22.2% |

## New vs Older Model Comparison

| Pair | Common Tests | Newer Pass Rate | Older Pass Rate | Delta |
|---|---:|---:|---:|---:|
| `gpt-5` vs `gpt-4o` | 54 | 90.7% | 83.3% | +7.4% |
| `claude-sonnet-4-6` vs `claude-3-7-sonnet` | 54 | 83.3% | 83.3% | +0.0% |
| `gemini-3-1-pro` vs `gemini-2-5-pro` | 54 | 66.7% | 22.2% | +44.4% |

## Group Averages

| Group | Avg Effective Pass | Avg Pass (logged) | Avg Coverage |
|---|---:|---:|---:|
| `new_frontier` | 80.2% | 80.2% | 100.0% |
| `legacy_frontier` | 63.0% | 63.0% | 100.0% |
| `compact_reasoning` | 83.3% | 83.3% | 100.0% |
| `open_source` | 82.7% | 82.7% | 100.0% |

## Topic-Level Performance

| Topic | Passed | Logged | Pass Rate |
|---|---:|---:|---:|
| Topic 1 (Visual Perception) | 235 | 288 | 81.6% |
| Topic 2 (Spatial and Tool-Use) | 133 | 168 | 79.2% |
| Topic 3 (Safety and Autonomy) | 133 | 192 | 69.3% |

## Failure-Type Performance

| Failure Type | Passed | Logged | Pass Rate |
|---|---:|---:|---:|
| `ADVERSARIAL_VULN` | 41 | 48 | 85.4% |
| `BINDING_FAILURE` | 113 | 132 | 85.6% |
| `CROSS_MODAL_GAP` | 121 | 156 | 77.6% |
| `PROMPT_SENSITIVITY` | 44 | 84 | 52.4% |
| `TRAINING_BIAS` | 182 | 228 | 79.8% |

## Hardest Tests Across Models

| Test ID | Passed | Logged | Pass Rate |
|---|---:|---:|---:|
| `liang2023_PS1_phrasing_A` | 0 | 12 | 0.0% |
| `liang2023_PS1_phrasing_B` | 1 | 12 | 8.3% |
| `liu2023_SR5_counting_position` | 2 | 12 | 16.7% |
| `liu2023_SR4_navigation` | 3 | 12 | 25.0% |
| `zhou2023_R1_commonsense_override_1` | 4 | 12 | 33.3% |
| `mecattaf2024_M3_object_localization` | 4 | 12 | 33.3% |
| `mecattaf2024_M1_3d_distance` | 5 | 12 | 41.7% |
| `liang2023_PS3_missing_feedback` | 5 | 12 | 41.7% |
| `blindtest_P1_complex_lines` | 6 | 12 | 50.0% |
| `mecattaf2024_M2_action_sequence` | 7 | 12 | 58.3% |
| `liang2023_PS4_implicit_precondition` | 7 | 12 | 58.3% |
| `guran2024_G2_action_ordering` | 8 | 12 | 66.7% |

## Interpretation

- **Improvement signal:** compare pairwise deltas; positive delta indicates newer model outperforms the older model on overlapping successful calls.
- **Robustness caution:** a high logged pass rate with low coverage can mask provider unavailability/rate limits.
- **Failure concentration:** low-pass tests indicate persistent weaknesses in compositional planning, spatial binding, and prompt sensitivity.
- **Scientific takeaway:** this is a live systems benchmark; results combine capability and reliability (availability + correctness).
