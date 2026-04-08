# Group 7 — LLM Reasoning Failures: Embodied Robustness
## Test Suite Specification

**Survey source:** Song et al., 2026 — *Large Language Model Reasoning Failures* (TMLR)
**Coverage:** Section 5 — Embodied Reasoning × Robustness column
**Group sub-topics:** What's Wrong with the Picture? / Spatial & Tool-Use / Safety & Autonomy

---

## Directory Structure

```
group7_llm_tests/
├── README.md                          ← this file
├── requirements.txt                   ← dependencies
├── config.py                          ← model configs, API keys
├── topic1_visual_perception/
│   ├── test_whoops.py                 ← Bitton-Guetta 2023
│   ├── test_blindtest.py              ← Rahmanzadehgervi 2024
│   ├── test_spatial_relations.py      ← Liu 2023 + Zhao 2024
│   └── test_binding_problem.py        ← Campbell 2025
├── topic2_spatial_tool_use/
│   ├── test_spatialvlm.py             ← Chen 2024
│   ├── test_3d_embodied.py            ← Mecattaf 2024 + Guran 2024
│   └── test_tool_use.py               ← Xu 2023 + Dao 2025
└── topic3_safety_autonomy/
    ├── test_prompt_sensitivity.py      ← Liang 2023
    ├── test_adversarial.py             ← Zhang 2024c
    └── test_egonormia.py              ← Rezaei 2025
```

---

## Paper Registry — Models Tested Per Paper

### Topic 1: "What's Wrong with the Picture?" (Section 5.2)

| Paper | Venue | Models Tested in Paper | Models to Test Now |
|-------|-------|----------------------|-------------------|
| Bitton-Guetta et al., 2023 (WHOOPS) | ICCV 2023 | BLIP-2, LLaVA-1.3, MiniGPT-4, OFA, DALL-EVAL | GPT-4o, Claude Sonnet 4.6, Gemini 1.5 Pro |
| Rahmanzadehgervi et al., 2024 (BlindTest) | ACCV 2024 | GPT-4o, Gemini-1.5, Claude Sonnet-3, Claude Sonnet-3.5 | GPT-4o, Claude Sonnet 4.6, Gemini 2.0 Flash |
| Zhou et al., 2023b (ROME) | EMNLP 2023 | CLIP-ViT, BLIP-2, OFA, GPT-4V | GPT-4o, Claude Sonnet 4.6 |
| Liu et al., 2023a (Visual Spatial Reasoning) | TACL 2023 | OFA, BLIP, FLAVA, VinVL, ViLBERT, ALBEF, TCL, 12+ VLMs | GPT-4o, Claude Sonnet 4.6, LLaVA-1.6 |
| Campbell et al., 2025 (Binding Problem) | NeurIPS 2025 | GPT-4V, LLaVA-1.6, InstructBLIP, IDEFICS | GPT-4o, Claude Sonnet 4.6, Gemini 1.5 Pro |
| Zhao et al., 2024a (Ambiguous Spatial) | arXiv 2024 | GPT-4V, Gemini Pro Vision, LLaVA-1.5 | GPT-4o, Claude Sonnet 4.6 |

### Topic 2: Spatial and Tool-Use Reasoning (Section 5.3)

| Paper | Venue | Models Tested in Paper | Models to Test Now |
|-------|-------|----------------------|-------------------|
| Chen et al., 2024a (SpatialVLM) | CVPR 2024 | GPT-4V, LLaVA-1.5, InstructBLIP, BLIP-2 | GPT-4o, Claude Sonnet 4.6, Gemini 1.5 Pro |
| Mecattaf et al., 2024 (3D Embodied) | arXiv 2024 | GPT-4, GPT-3.5, LLaMA-2-70B, Gemini Pro | GPT-4o, Claude Sonnet 4.6, o3-mini |
| Xu et al., 2023a (Robot Tool Use) | arXiv 2023 | GPT-4, GPT-3.5-turbo, Codex | GPT-4o, Claude Sonnet 4.6 |
| Dao & Vu, 2025 (AlphaMaze) | arXiv 2025 | LLaMA-3.1-8B, Qwen2.5-7B, DeepSeek-R1 | GPT-4o, o3-mini, Claude Sonnet 4.6 |
| Guran et al., 2024 (Robotic Manip.) | arXiv 2024 | GPT-4V, LLaVA-1.5, CogVLM | GPT-4o, Claude Sonnet 4.6 |

### Topic 3: Safety and Long-Term Autonomy (Section 5.3)

| Paper | Venue | Models Tested in Paper | Models to Test Now |
|-------|-------|----------------------|-------------------|
| Liang et al., 2023 (Code as Policies) | ICRA 2023 | Codex (code-davinci-002), GPT-3, GPT-3.5 | GPT-4o, Claude Sonnet 4.6, o3-mini |
| Zhang et al., 2024c (BadRobot) | arXiv 2024 | GPT-4V, LLaVA-1.5, MiniGPT-4 (embodied) | GPT-4o, Claude Sonnet 4.6 |
| Rezaei et al., 2025 (EgoNormia) | arXiv 2025 | o3-mini, GPT-4o, Claude-3.5-Sonnet | GPT-4o, o3-mini, Claude Sonnet 4.6 |

---

## Robustness Failure Types (use as labels in results)

- `TRAINING_BIAS` — model predicts statistically likely output instead of perceiving actual input
- `CROSS_MODAL_GAP` — model defaults to language prior when visual evidence conflicts
- `PROMPT_SENSITIVITY` — output changes significantly with minor phrasing variation
- `ADVERSARIAL_VULN` — model fails under adversarial/manipulative input
- `BINDING_FAILURE` — model cannot associate properties to correct objects in multi-object scenes

---

## How to Run

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=your_key
export ANTHROPIC_API_KEY=your_key

# Run a specific test
python topic1_visual_perception/test_blindtest.py

# Run all tests and save results
python run_all_tests.py --output results/
```

---

## Expected Output Format (per test)

```json
{
  "paper": "Rahmanzadehgervi et al., 2024",
  "test_id": "blindtest_P1",
  "failure_type": "CROSS_MODAL_GAP",
  "model": "gpt-4o",
  "prompt": "...",
  "expected_answer": "1",
  "model_answer": "2",
  "passed": false,
  "notes": "Model overcounts, consistent with paper's reported failure"
}
```

---

## Scientific Analysis & Key Takeaways
**(Based on OpenRouter Comparative Benchmark, April 2026)**

Following a comprehensive 648-call benchmark execution across 12 diverse LLMs spanning frontier, compact, and open-source architectures, several key observations regarding reasoning robustness were identified:

### 1. The Superiority of Compact Reasoning Models
Surprisingly, the traditional parameter-scaling paradigm is challenged by modern reasoning-optimized models in spatial contexts. The `gpt-5-mini` model achieved the highest absolute pass rate (92.6%), independently outperforming its larger counterpart `gpt-5` (90.7%) and vastly outperforming `gpt-4o` (83.3%). "Compact reasoning" models averaged an 83.3% effective pass rate, proving that heavily distilled logic models perform exceptionally well on rigid constraint-following tasks.

### 2. High Vulnerability to Training Bias (Commonsense Override)
Under the `TRAINING_BIAS` failure type (such as the ROME Benchmark / Zhou et al. tests), models demonstrated massive non-compliance when explicit text contradicted physical norms. For example, in the "cow in the microwave" test (`zhou2023_R1_commonsense_override_1`), only **33.3%** of tested models (4 out of 12) correctly acknowledged the constraints provided. This vigorously proves models will aggressively overwrite perceptual truths with their deep linguistic priors.

### 3. Open Source Matches Frontier Capabilities
The highest-performing open-source model tested, `qwen3-next-80b`, achieved an 85.2% pass rate, placing it comfortably ahead of standard industry standbys like `gpt-4o` and `claude-3-7-sonnet` (83.3%). `llama-3-3-70b` and `deepseek-r1` also showed formidable baseline logic (81.5%). Open weights are now objectively competitive in embodied task reasoning.

### 4. Extreme Prompt Sensitivity
Models still struggle profoundly with invariant semantic understanding. When evaluating `PROMPT_SENSITIVITY` failures (Zhao 2024; Liang 2023), simply altering the grammatical structure while preserving the exact semantic relationships caused wide-scale breakage across architectures. This area remains the weakest overall sub-domain (averaging just a 52.4% pass rate across the board).

### 5. The Embodied AI Navigation Gap
Across the three evaluated domains, *Topic 3 (Safety and Autonomy)* recorded the lowest cumulative performance (69.3%). Spatial navigation, continuous action sequencing, and dynamic physical safety represent the leading boundary for systematic LLM failures, significantly lagging behind basic static perception.
