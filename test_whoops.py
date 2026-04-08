"""
topic1_visual_perception/test_whoops.py
========================================
Paper: Bitton-Guetta et al., 2023
Title: Breaking Common Sense: WHOOPS! A Vision-and-Language Benchmark
       of Synthetic and Compositional Images
Venue: ICCV 2023
arXiv: 2303.07274

ROBUSTNESS FAILURE TYPE: TRAINING_BIAS + CROSS_MODAL_GAP

WHAT THE PAPER FOUND:
    Models hallucinate plausible captions instead of detecting anomalies.
    BLIP-2 sees a person skating on wooden parquet floor (not ice) and
    captions it "a person is skating on an ice rink" — substituting the
    statistically likely context for the actual visual content.

MODELS TESTED IN PAPER:
    - BLIP-2 (Salesforce, 2023)
    - LLaVA-1.3 (Liu et al., 2023)
    - MiniGPT-4 (Zhu et al., 2023)
    - OFA (Wang et al., 2022)
    - DALL-EVAL baseline

MODELS TO TEST NOW (current equivalents):
    - gpt-4o          (best current VLM, successor to GPT-4V)
    - claude-sonnet-4-6 (Anthropic current)

TEST APPROACH:
    Text-only proxy tests (for when you don't have WHOOPS images).
    These use written scene descriptions that violate commonsense —
    the same reasoning failure manifests in text if the model relies
    on statistical co-occurrence rather than reading the actual description.

    For full reproduction: download WHOOPS dataset from
    https://whoops-benchmark.github.io and pass image paths to call_model().

HOW TO RUN:
    python topic1_visual_perception/test_whoops.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import call_model, log_result, PAPER_MODELS

PAPER = "Bitton-Guetta et al., 2023 (WHOOPS)"
MODELS_TO_TEST = ["gpt-4o", "claude-sonnet-4-6"]


# ─────────────────────────────────────────────────────
# TEST CASES
# Each case includes: prompt, expected answer, and the
# commonsense violation the model should detect.
# ─────────────────────────────────────────────────────

WHOOPS_TEXT_PROXY_TESTS = [
    {
        "id": "whoops_T1_skating_parquet",
        "description": "Person skating on wooden floor (not ice) — BLIP-2 failure case from paper",
        "failure_type": "TRAINING_BIAS",
        "prompt": (
            "Look at this scene description carefully and answer:\n\n"
            "A person is wearing ice skates and gliding across a surface. "
            "The surface beneath them is clearly wooden parquet flooring — "
            "you can see the wood grain pattern and the seams between floorboards. "
            "There is no ice present.\n\n"
            "Question: What is unusual or wrong with this scene? "
            "Be specific about what you observe in the description."
        ),
        "expected_keyword": "wood",
        "expected_answer": "Ice skates on wooden floor — no ice present",
        "paper_model_failure": "BLIP-2 captioned this as 'skating on an ice rink', ignoring the wooden floor"
    },
    {
        "id": "whoops_T2_fish_climbing_tree",
        "description": "Fish in a tree — tests commonsense violation detection",
        "failure_type": "TRAINING_BIAS",
        "prompt": (
            "Describe what is physically wrong or impossible about this scene:\n\n"
            "A large salmon is perched high up in the branches of an oak tree, "
            "its fins wrapped around a thick branch. The tree is in full leaf and "
            "is rooted in dry ground in a suburban backyard. The fish appears healthy "
            "and alert, as if it has always lived in trees.\n\n"
            "What makes this scene anomalous?"
        ),
        "expected_keyword": "fish",
        "expected_answer": "Fish cannot climb trees / fish live in water not trees",
        "paper_model_failure": "VLMs sometimes generate 'realistic' captions ignoring the impossibility"
    },
    {
        "id": "whoops_T3_umbrella_sun_indoors",
        "description": "Umbrella used indoors with bright sun — context violation",
        "failure_type": "TRAINING_BIAS",
        "prompt": (
            "What is the commonsense violation in this scene?\n\n"
            "A person sits at a desk inside a closed office room with no windows. "
            "They are holding an open umbrella above their head to protect from "
            "bright sunshine. The ceiling is solid concrete. There is no rain "
            "or water present anywhere in the room.\n\n"
            "Identify the specific anomaly."
        ),
        "expected_keyword": "indoors",
        "expected_answer": "Umbrella used indoors against sunshine with solid ceiling — sun cannot reach indoors",
        "paper_model_failure": "Models may generate 'person using umbrella' without flagging the impossibility"
    },
    {
        "id": "whoops_T4_caption_bias",
        "description": "Direct test of whether model substitutes expected vs actual scene",
        "failure_type": "CROSS_MODAL_GAP",
        "prompt": (
            "I will describe two scenes. For each one, tell me exactly what you see "
            "described — do NOT add information not present in the description.\n\n"
            "Scene A: A chef in a kitchen holds a spatula over a stovetop.\n"
            "Scene B: A chef in a kitchen holds a spatula over a bathtub filled with water.\n\n"
            "What is different between Scene A and Scene B? "
            "What would a model that relies on statistical patterns predict for Scene B instead?"
        ),
        "expected_keyword": "bathtub",
        "expected_answer": "Scene B has a bathtub not a stovetop — model might predict stovetop due to kitchen-chef-spatula pattern",
        "paper_model_failure": "Tests the model's awareness of its own training-data bias"
    },
]

WHOOPS_IMAGE_TESTS = [
    {
        "id": "whoops_IMG1_skating_parquet",
        "description": "WHOOPS image: ice skates on wooden floor — requires WHOOPS dataset",
        "failure_type": "TRAINING_BIAS",
        "image_placeholder": "whoops_images/skating_parquet.jpg",
        "prompt": (
            "Look at this image carefully. What is wrong or unusual about what you see? "
            "Describe any physical impossibility, commonsense violation, or anomaly. "
            "Be specific — do not describe what the scene 'should' look like, "
            "describe only what you actually observe in the image."
        ),
        "expected_keyword": "floor",
        "expected_answer": "Person skating on wooden/parquet floor — no ice",
        "paper_model_failure": "BLIP-2 responded: 'a person is skating on an ice rink'"
    },
]


def evaluate_response(response: str, expected_keyword: str) -> bool:
    return expected_keyword.lower() in response.lower()


def run_tests():
    print(f"\n{'='*60}")
    print(f"PAPER: {PAPER}")
    print(f"Testing: {MODELS_TO_TEST}")
    print(f"Original paper models: {PAPER_MODELS['whoops_bitton2023']}")
    print(f"{'='*60}\n")

    all_results = []

    for test in WHOOPS_TEXT_PROXY_TESTS:
        print(f"\n--- {test['id']} ---")
        print(f"Testing: {test['description']}")

        for model in MODELS_TO_TEST:
            try:
                response = call_model(model, test["prompt"])
                passed = evaluate_response(response, test["expected_keyword"])
                result = log_result(
                    paper=PAPER,
                    test_id=test["id"],
                    failure_type=test["failure_type"],
                    model=model,
                    prompt=test["prompt"],
                    expected=test["expected_answer"],
                    actual=response,
                    passed=passed,
                    notes=test["paper_model_failure"]
                )
                all_results.append(result)
            except Exception as e:
                print(f"  [ERROR] {model}: {e}")

    print(f"\n{'='*60}")
    print(f"WHOOPS RESULTS SUMMARY")
    total = len(all_results)
    passed = sum(1 for r in all_results if r["passed"])
    print(f"Passed: {passed}/{total}")
    print(f"NOTE: Failures = model reproduces the same bias as reported in paper")
    print(f"{'='*60}\n")

    return all_results


if __name__ == "__main__":
    run_tests()
