"""
topic1_visual_perception/test_spatial_relations.py
====================================================
Papers:
  [A] Liu et al., 2023a — Visual Spatial Reasoning (TACL 2023)
  [B] Zhao et al., 2024a — Ambiguous Spatial Demonstrations (arXiv 2024)
  [C] Campbell et al., 2025 — The Binding Problem in VLMs (NeurIPS 2025)
  [D] Zhou et al., 2023b — ROME Benchmark (EMNLP 2023)

ROBUSTNESS FAILURE TYPES:
  Liu 2023:     TRAINING_BIAS + CROSS_MODAL_GAP
  Zhao 2024:    CROSS_MODAL_GAP + PROMPT_SENSITIVITY
  Campbell 2025: BINDING_FAILURE
  Zhou 2023b:   TRAINING_BIAS

WHAT THE PAPERS FOUND:
  [A] Liu 2023: VLMs tested on Spatial-Map, Maze-Nav, Spatial-Grid fall
      below random chance on spatial reasoning. Despite visual input, VLMs
      underperform their pure LLM backbones on spatial tasks — adding vision
      hurts. Tested 18 models including OFA, BLIP, FLAVA, VinVL, ViLBERT.

  [B] Zhao 2024: VLMs cannot learn spatial reasoning from visual demonstrations.
      The same spatial task presented with different visual examples yields
      inconsistent outputs — high prompt/example sensitivity.

  [C] Campbell 2025: When multiple objects are present, VLMs cannot reliably
      bind properties (color, size, shape) to the correct object. A scene
      with "a small red cube and a large blue sphere" triggers errors in which
      property belongs to which object. Tested GPT-4V, LLaVA-1.6-34B,
      InstructBLIP, IDEFICS-80B.

  [D] Zhou 2023b (ROME): Models reason using commonsense world knowledge
      rather than actual visual spatial content.

MODELS TESTED IN PAPERS:
  Liu 2023:     OFA, BLIP, FLAVA, VinVL, ViLBERT, ALBEF, TCL (+12 more)
  Zhao 2024:    GPT-4V, Gemini-Pro-Vision, LLaVA-1.5-13B
  Campbell 2025: GPT-4V, LLaVA-1.6-34B, InstructBLIP-Vicuna-13B, IDEFICS-80B
  Zhou 2023b:   CLIP-ViT-L/14, BLIP-2, OFA, GPT-4V

MODELS TO TEST NOW:
    - gpt-4o
    - claude-sonnet-4-6

HOW TO RUN:
    python topic1_visual_perception/test_spatial_relations.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import call_model, log_result, PAPER_MODELS

MODELS_TO_TEST = ["gpt-4o", "claude-sonnet-4-6"]


# ───────────────────────────────────────────────
# [A] Liu et al., 2023 — Spatial Relation Tests
# ───────────────────────────────────────────────

LIU2023_TESTS = [
    {
        "id": "liu2023_SR1_above_below",
        "paper": "Liu et al., 2023a (Visual Spatial Reasoning)",
        "task": "Basic above/below spatial relation",
        "failure_type": "TRAINING_BIAS",
        "prompt": (
            "Answer with only 'above' or 'below'.\n\n"
            "In an image, a cat is sitting on a shelf. "
            "A dog is lying on the floor directly beneath the shelf.\n\n"
            "Is the cat above or below the dog?"
        ),
        "expected_answer": "above",
    },
    {
        "id": "liu2023_SR2_left_right_unusual",
        "paper": "Liu et al., 2023a (Visual Spatial Reasoning)",
        "task": "Less frequent spatial relation (left/right with unusual pairing)",
        "failure_type": "TRAINING_BIAS",
        "prompt": (
            "Answer with only 'left' or 'right'.\n\n"
            "In the image: a banana is placed to the RIGHT of a hammer.\n"
            "The hammer is in the center of the image.\n\n"
            "Is the banana to the left or right of the hammer?"
        ),
        "expected_answer": "right",
    },
    {
        "id": "liu2023_SR3_inside_outside",
        "paper": "Liu et al., 2023a (Visual Spatial Reasoning)",
        "task": "Counter-intuitive inside/outside relation",
        "failure_type": "TRAINING_BIAS",
        "prompt": (
            "Answer with only 'inside' or 'outside'.\n\n"
            "A house is depicted inside a bottle — the miniature house "
            "is fully enclosed within the glass walls of the bottle.\n\n"
            "Is the house inside or outside the bottle?"
        ),
        "expected_answer": "inside",
    },
    {
        "id": "liu2023_SR4_navigation",
        "paper": "Liu et al., 2023a (Visual Spatial Reasoning — Maze-Nav)",
        "task": "Navigation task from Maze-Nav benchmark",
        "failure_type": "CROSS_MODAL_GAP",
        "prompt": (
            "Answer with the direction: north, south, east, or west.\n\n"
            "You are at position (3, 3) on a 5x5 grid (1-indexed, top-left is (1,1)).\n"
            "Your destination is position (3, 1).\n"
            "There are no obstacles.\n\n"
            "In which direction should you move to get closer to your destination? "
            "(North = row decreases, South = row increases)"
        ),
        "expected_answer": "north",
    },
    {
        "id": "liu2023_SR5_counting_position",
        "paper": "Liu et al., 2023a (Visual Spatial Reasoning — Spatial-Grid)",
        "task": "Object counting within position constraint",
        "failure_type": "CROSS_MODAL_GAP",
        "prompt": (
            "Answer with only a number.\n\n"
            "A 4x4 grid contains shapes in these positions:\n"
            "- Row 1: circle, square, circle, triangle\n"
            "- Row 2: square, circle, triangle, circle\n"
            "- Row 3: triangle, square, circle, square\n"
            "- Row 4: circle, triangle, square, circle\n\n"
            "How many circles are in the grid?"
        ),
        "expected_answer": "6",
    },
]


# ───────────────────────────────────────────────
# [B] Campbell et al., 2025 — Binding Problem
# ───────────────────────────────────────────────

CAMPBELL2025_TESTS = [
    {
        "id": "campbell2025_B1_two_object_binding",
        "paper": "Campbell et al., 2025 (Binding Problem in VLMs)",
        "task": "Bind color property to correct object among two objects",
        "failure_type": "BINDING_FAILURE",
        "prompt": (
            "Answer with only the object name.\n\n"
            "A scene contains exactly two objects:\n"
            "- A small red cube on the left\n"
            "- A large blue sphere on the right\n\n"
            "Which object is blue?"
        ),
        "expected_answer": "sphere",
    },
    {
        "id": "campbell2025_B2_size_binding",
        "paper": "Campbell et al., 2025 (Binding Problem in VLMs)",
        "task": "Bind size property to correct object",
        "failure_type": "BINDING_FAILURE",
        "prompt": (
            "Answer with only the object name.\n\n"
            "A scene contains:\n"
            "- A large metal cylinder in the center\n"
            "- A small wooden cube in the corner\n"
            "- A medium glass sphere on the table\n\n"
            "Which object is made of wood?"
        ),
        "expected_answer": "cube",
    },
    {
        "id": "campbell2025_B3_four_object_binding",
        "paper": "Campbell et al., 2025 (Binding Problem in VLMs)",
        "task": "Binding with four objects — high failure rate in paper",
        "failure_type": "BINDING_FAILURE",
        "prompt": (
            "Answer with only the color.\n\n"
            "A scene contains four objects:\n"
            "- A red teapot on the top shelf\n"
            "- A blue mug on the second shelf\n"
            "- A green plate on the third shelf\n"
            "- A yellow bowl on the bottom shelf\n\n"
            "What color is the object on the second shelf?"
        ),
        "expected_answer": "blue",
    },
    {
        "id": "campbell2025_B4_property_swap",
        "paper": "Campbell et al., 2025 (Binding Problem in VLMs)",
        "task": "Swapped properties — tests whether model binds or defaults to priors",
        "failure_type": "BINDING_FAILURE",
        "prompt": (
            "Answer with only the object and its color.\n\n"
            "IMPORTANT: Read carefully. In this unusual scene:\n"
            "- The banana is purple (not yellow)\n"
            "- The grape is yellow (not purple)\n\n"
            "What color is the banana in this scene?"
        ),
        "expected_answer": "purple",
    },
]


# ───────────────────────────────────────────────
# [C] Zhao 2024 — Prompt/Example Sensitivity
# ───────────────────────────────────────────────

ZHAO2024_TESTS = [
    {
        "id": "zhao2024_S1_consistent_framing",
        "paper": "Zhao et al., 2024a (Ambiguous Spatial Demonstrations)",
        "task": "Same spatial task, framing variant A",
        "failure_type": "PROMPT_SENSITIVITY",
        "prompt": (
            "Answer with only 'left' or 'right'.\n\n"
            "Example 1: A book is to the LEFT of a lamp.\n"
            "Example 2: A cup is to the LEFT of a plate.\n\n"
            "Now: A pencil is to the [LEFT/RIGHT] of a ruler. "
            "The pencil is positioned before the ruler in the horizontal sequence.\n\n"
            "Where is the pencil relative to the ruler?"
        ),
        "expected_answer": "left",
        "comparison_id": "zhao2024_S1_reframed",
    },
    {
        "id": "zhao2024_S1_reframed",
        "paper": "Zhao et al., 2024a (Ambiguous Spatial Demonstrations)",
        "task": "Same spatial task, framing variant B (should give same answer)",
        "failure_type": "PROMPT_SENSITIVITY",
        "prompt": (
            "Answer with only 'left' or 'right'.\n\n"
            "Study these examples:\n"
            "- The lamp is to the RIGHT of the book.\n"
            "- The plate is to the RIGHT of the cup.\n\n"
            "Question: A ruler is to the RIGHT of a pencil. "
            "Where is the pencil relative to the ruler?"
        ),
        "expected_answer": "left",
        "comparison_id": "zhao2024_S1_consistent_framing",
    },
]


# ───────────────────────────────────────────────
# [D] Zhou et al., 2023b — ROME Benchmark
# ───────────────────────────────────────────────

ZHOU2023_TESTS = [
    {
        "id": "zhou2023_R1_commonsense_override_1",
        "paper": "Zhou et al., 2023b (ROME)",
        "task": "Test if model relies on commonsense over explicit spatial text",
        "failure_type": "TRAINING_BIAS",
        "prompt": (
            "Answer with only 'yes' or 'no'.\n\n"
            "In this scene, there is a normal-sized cow standing fully INSIDE a generic household microwave.\n\n"
            "Is the cow inside the microwave in the scene provided?"
        ),
        "expected_answer": "yes",
    },
    {
        "id": "zhou2023_R2_commonsense_override_2",
        "paper": "Zhou et al., 2023b (ROME)",
        "task": "Counterfactual physical positioning",
        "failure_type": "TRAINING_BIAS",
        "prompt": (
            "Answer with only the object name.\n\n"
            "In this image, an elephant is resting gently ON TOP of a fragile egg, without breaking it.\n\n"
            "What object is the elephant resting on?"
        ),
        "expected_answer": "egg",
    },
]


def evaluate(expected: str, response: str) -> bool:
    return expected.lower() in response.lower()


def run_tests():
    all_results = []
    all_suites = [
        ("Liu 2023 — Spatial Relations", LIU2023_TESTS),
        ("Campbell 2025 — Binding Problem", CAMPBELL2025_TESTS),
        ("Zhao 2024 — Prompt Sensitivity", ZHAO2024_TESTS),
        ("Zhou 2023b — ROME", ZHOU2023_TESTS),
    ]

    for suite_name, tests in all_suites:
        print(f"\n{'='*60}")
        print(f"SUITE: {suite_name}")
        print(f"{'='*60}")

        for test in tests:
            print(f"\n--- {test['id']} ---")
            print(f"Task: {test['task']}")

            for model in MODELS_TO_TEST:
                try:
                    response = call_model(model, test["prompt"], max_tokens=80)
                    passed = evaluate(test["expected_answer"], response)
                    result = log_result(
                        paper=test["paper"],
                        test_id=test["id"],
                        failure_type=test["failure_type"],
                        model=model,
                        prompt=test["prompt"],
                        expected=test["expected_answer"],
                        actual=response,
                        passed=passed,
                    )
                    all_results.append(result)
                except Exception as e:
                    print(f"  [ERROR] {model}: {e}")

    # Special analysis: compare zhao2024 framing pairs
    print(f"\n{'='*60}")
    print("PROMPT SENSITIVITY ANALYSIS (Zhao 2024)")
    print("Same question, different framing — should both give 'left'")
    for model in MODELS_TO_TEST:
        v1 = next((r for r in all_results
                   if r["test_id"] == "zhao2024_S1_consistent_framing"
                   and r["model"] == model), None)
        v2 = next((r for r in all_results
                   if r["test_id"] == "zhao2024_S1_reframed"
                   and r["model"] == model), None)
        if v1 and v2:
            consistent = v1["passed"] == v2["passed"]
            print(f"  {model}: variant_A={v1['model_answer'][:20]!r} | "
                  f"variant_B={v2['model_answer'][:20]!r} | "
                  f"consistent={'YES' if consistent else 'NO — SENSITIVITY FAILURE'}")

    print(f"\nTotal passed: {sum(1 for r in all_results if r['passed'])}/{len(all_results)}")
    return all_results


if __name__ == "__main__":
    run_tests()
