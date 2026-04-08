"""
topic2_spatial_tool_use/test_spatialvlm_and_embodied.py
=========================================================
Papers:
  [A] Chen et al., 2024a — SpatialVLM (CVPR 2024)
  [B] Mecattaf et al., 2024 — 3D Embodied Environment Failures (arXiv 2024)
  [C] Xu et al., 2023a — Creative Robot Tool Use (arXiv 2023)
  [D] Guran et al., 2024 — Task-Oriented Robotic Manipulation (arXiv 2024)
  [E] Dao & Vu, 2025 — AlphaMaze: Spatial Intelligence via GRPO (arXiv 2025)

ROBUSTNESS FAILURE TYPES:
  Chen 2024:    CROSS_MODAL_GAP (distance estimation)
  Mecattaf 2024: TRAINING_BIAS + BINDING_FAILURE
  Xu 2023:      TRAINING_BIAS (tool generalization)
  Guran 2024:   BINDING_FAILURE + ADVERSARIAL_VULN
  Dao 2025:     TRAINING_BIAS (maze spatial navigation)

WHAT THE PAPERS FOUND:
  [A] Chen 2024 (SpatialVLM):
      GPT-4V cannot estimate whether a 1-meter-wide robot can navigate
      between furniture — it hedges verbally instead of computing distances.
      The paper endows VLMs with explicit spatial reasoning by training on
      generated 3D spatial QA data. Without this training, models fail at
      metric spatial estimation entirely.

  [B] Mecattaf 2024:
      In a 3D embodied simulation, LLMs fail at: 3D distance estimation,
      object localization, multi-step manipulation planning. Tested GPT-4,
      GPT-3.5, LLaMA-2-70B, Gemini-Pro. All models produce physically
      impossible actions and fail when task steps must be composed.

  [C] Xu 2023 (Creative Tool Use):
      GPT-4 can describe how to use individual tools but cannot generalize
      to creative/novel tool use (using a broom handle as a lever, a lid
      as a ramp). Tests the robustness failure of tool-concept overfitting.

  [D] Guran 2024:
      VLMs controlling robots fail at action preconditions — generating
      wrong order, missing steps, affordance errors (trying to pick up
      objects they cannot grasp), and unnecessary extra steps.

  [E] Dao & Vu 2025 (AlphaMaze):
      Without GRPO training, LLMs cannot solve maze navigation. The paper
      shows that spatial reasoning requires explicit RL-based training,
      not prompting. Tests on LLaMA-3.1-8B, Qwen2.5-7B, DeepSeek-R1.

MODELS TESTED IN PAPERS:
  Chen 2024:    GPT-4V, LLaVA-1.5, InstructBLIP, BLIP-2
  Mecattaf 2024: GPT-4, GPT-3.5-turbo, LLaMA-2-70B, Gemini-Pro
  Xu 2023:      GPT-4, GPT-3.5-turbo, Codex
  Guran 2024:   GPT-4V, LLaVA-1.5-13B, CogVLM-17B
  Dao 2025:     LLaMA-3.1-8B-Instruct, Qwen2.5-7B, DeepSeek-R1-Distill-7B

MODELS TO TEST NOW:
    - gpt-4o
    - claude-sonnet-4-6
    - o3-mini  (for Dao 2025 maze tests — reasoning model)

HOW TO RUN:
    python topic2_spatial_tool_use/test_spatialvlm_and_embodied.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import call_model, log_result, PAPER_MODELS

MODELS_TO_TEST = ["gpt-4o", "claude-sonnet-4-6"]
REASONING_MODELS = ["o3-mini", "gpt-4o"]  # for AlphaMaze tests


# ───────────────────────────────────────────────
# [A] Chen 2024 — SpatialVLM Distance Tests
# From Table 15: GPT-4V failure on robot clearance task
# ───────────────────────────────────────────────

CHEN2024_TESTS = [
    {
        "id": "spatialvlm_C1_robot_clearance",
        "paper": "Chen et al., 2024a (SpatialVLM)",
        "task": "Can a 1m-wide robot pass between sofa and table? — exact paper example",
        "failure_type": "CROSS_MODAL_GAP",
        "prompt": (
            "You are a cleaning robot that is 1 meter wide. You are standing in a "
            "living room and see the following scene:\n\n"
            "- A sofa is positioned against the left wall\n"
            "- A coffee table is in the center of the room\n"
            "- The gap between the sofa's right edge and the table's left edge "
            "is approximately 80 centimeters\n"
            "- You want to move from your current position to the door on the right\n\n"
            "Can you go through the path between the sofa and the table? "
            "Answer Yes or No, then explain your geometric reasoning with numbers."
        ),
        "expected_answer": "No",
        "expected_keyword": "no",
        "paper_model_answer": (
            "GPT-4V: 'As an AI, I'm unable to physically interact with environments, "
            "but I can provide some insights... it appears that the sofa and the table "
            "are quite close to each other, and there may not be enough space...' "
            "(hedged, did not compute 80cm < 100cm)"
        ),
    },
    {
        "id": "spatialvlm_C2_distance_estimation",
        "paper": "Chen et al., 2024a (SpatialVLM)",
        "task": "Estimate distance from description — tests metric spatial grounding",
        "failure_type": "CROSS_MODAL_GAP",
        "prompt": (
            "You are in a room. Use the given reference to estimate a distance.\n\n"
            "Reference: A standard door is 2 meters tall.\n"
            "Observation: The bookshelf appears to be about half the height of the door.\n\n"
            "Question: What is the approximate height of the bookshelf in meters? "
            "Give only a number."
        ),
        "expected_answer": "1",
        "expected_keyword": "1",
        "paper_model_answer": "Models trained without spatial grounding often give vague answers or wrong estimates",
    },
    {
        "id": "spatialvlm_C3_relative_depth",
        "paper": "Chen et al., 2024a (SpatialVLM)",
        "task": "Relative depth ordering between objects",
        "failure_type": "CROSS_MODAL_GAP",
        "prompt": (
            "Answer with only the object name.\n\n"
            "In a room:\n"
            "- A vase is 0.5 meters away from you\n"
            "- A chair is 2 meters away from you\n"
            "- A window is 4 meters away from you\n\n"
            "Which object is closest to you?"
        ),
        "expected_answer": "vase",
        "expected_keyword": "vase",
        "paper_model_answer": "Simple case — used to establish baseline before harder tests",
    },
    {
        "id": "spatialvlm_C4_impossible_clearance",
        "paper": "Chen et al., 2024a (SpatialVLM)",
        "task": "Clearance with clearly insufficient gap",
        "failure_type": "CROSS_MODAL_GAP",
        "prompt": (
            "A robot is 90 cm wide.\n"
            "There is a gap of 50 cm between two walls.\n\n"
            "Can the robot fit through the gap? "
            "Answer Yes or No with a one-sentence explanation."
        ),
        "expected_answer": "No",
        "expected_keyword": "no",
        "paper_model_answer": "90cm robot cannot fit through 50cm gap — models sometimes still hedge",
    },
]


# ───────────────────────────────────────────────
# [B] Mecattaf 2024 — 3D Embodied Failures
# ───────────────────────────────────────────────

MECATTAF2024_TESTS = [
    {
        "id": "mecattaf2024_M1_3d_distance",
        "paper": "Mecattaf et al., 2024 (3D Embodied Environment)",
        "task": "3D distance estimation — key failure from paper",
        "failure_type": "TRAINING_BIAS",
        "prompt": (
            "You are an embodied agent in a 3D environment.\n"
            "You can see the following:\n"
            "- Object A (a red cube) is at coordinates (2, 0, 3)\n"
            "- Object B (a blue sphere) is at coordinates (5, 0, 7)\n\n"
            "Calculate the Euclidean distance between Object A and Object B. "
            "Show your calculation and give the final answer rounded to 2 decimal places."
        ),
        "expected_answer": "5.00",
        "expected_keyword": "5.0",
        "paper_model_answer": "Models often fail to correctly compute 3D distances, or confuse axes",
    },
    {
        "id": "mecattaf2024_M2_action_sequence",
        "paper": "Mecattaf et al., 2024 (3D Embodied Environment)",
        "task": "Multi-step action plan — tests composition failure",
        "failure_type": "BINDING_FAILURE",
        "prompt": (
            "You are a robot in a kitchen. List ONLY the actions needed in the correct order.\n\n"
            "Task: Make a cup of tea.\n"
            "Available objects: kettle (empty), tap, teabag, cup (empty), counter.\n\n"
            "Rule: You cannot pour from the kettle until it has been filled AND boiled.\n"
            "Rule: You cannot add a teabag to the cup until there is hot water in it.\n\n"
            "List each action on a new line. Keep it minimal — no explanations."
        ),
        "expected_keywords": ["fill", "boil", "pour", "add"],
        "expected_answer": "fill kettle → boil kettle → pour water → add teabag",
        "paper_model_answer": "Models frequently produce wrong order (add teabag before water) or missing steps",
    },
    {
        "id": "mecattaf2024_M3_object_localization",
        "paper": "Mecattaf et al., 2024 (3D Embodied Environment)",
        "task": "Object localization from egocentric description",
        "failure_type": "TRAINING_BIAS",
        "prompt": (
            "You are facing North. Answer with a cardinal direction.\n\n"
            "- A table is directly in front of you (North)\n"
            "- A chair is to your right\n"
            "- A door is behind you\n"
            "- A window is to your left\n\n"
            "You turn 90 degrees clockwise.\n"
            "Now, which direction is the door from you?"
        ),
        "expected_answer": "West",
        "expected_keyword": "west",
        "paper_model_answer": "Models fail at egocentric rotation — often say South instead of West",
    },
]


# ───────────────────────────────────────────────
# [C] Xu 2023 — Tool Use Generalization
# ───────────────────────────────────────────────

XU2023_TESTS = [
    {
        "id": "xu2023_T1_standard_tool_use",
        "paper": "Xu et al., 2023a (Creative Robot Tool Use)",
        "task": "Standard tool use — baseline (should pass)",
        "failure_type": "TRAINING_BIAS",
        "prompt": (
            "A robot needs to hammer a nail into a wall. "
            "It has a hammer available.\n\n"
            "Which tool should it use and how? Give a one-sentence answer."
        ),
        "expected_keyword": "hammer",
        "expected_answer": "Use the hammer to hit the nail",
    },
    {
        "id": "xu2023_T2_creative_tool_use",
        "paper": "Xu et al., 2023a (Creative Robot Tool Use)",
        "task": "Creative tool use — repurposing (paper's main failure case)",
        "failure_type": "TRAINING_BIAS",
        "prompt": (
            "A robot needs to prop open a heavy door that has no doorstop. "
            "The robot has no doorstop available. It has access to:\n"
            "- A hardcover book (22cm x 15cm x 4cm)\n"
            "- A rubber ball\n"
            "- A roll of tape\n\n"
            "Which item should the robot use and how? Be specific."
        ),
        "expected_keyword": "book",
        "expected_answer": "Use the book as a wedge under the door",
    },
    {
        "id": "xu2023_T3_novel_repurposing",
        "paper": "Xu et al., 2023a (Creative Robot Tool Use)",
        "task": "Highly novel tool repurposing — maximum generalization test",
        "failure_type": "TRAINING_BIAS",
        "prompt": (
            "A robot needs to retrieve a small ball that has rolled under a heavy sofa "
            "that it cannot lift. The robot has:\n"
            "- A long broom\n"
            "- A piece of string (1 meter long)\n"
            "- A small magnet\n"
            "- A bowl of water\n\n"
            "The ball is made of plastic (not magnetic).\n"
            "Which combination of tools should the robot use and describe the method precisely."
        ),
        "expected_keyword": "broom",
        "expected_answer": "Use broom handle to sweep/push the ball out from under the sofa",
    },
]


# ───────────────────────────────────────────────
# [D] Guran 2024 — Robotic Manipulation Failures
# Table 15 shows: wrong order, missing step, affordance error, extra step
# ───────────────────────────────────────────────

GURAN2024_TESTS = [
    {
        "id": "guran2024_G1_affordance_error",
        "paper": "Guran et al., 2024 (Task-Oriented Robotic Manipulation)",
        "task": "Affordance error — robot tries to pick up non-graspable object",
        "failure_type": "BINDING_FAILURE",
        "prompt": (
            "A robot arm with a standard gripper (can grasp objects up to 15cm wide) "
            "must complete a task. Say only YES or NO for each action:\n\n"
            "Can the robot:\n"
            "1. Pick up a coffee mug (8cm diameter) — YES or NO?\n"
            "2. Pick up a dining table (120cm wide) — YES or NO?\n"
            "3. Pick up a pen (1.5cm diameter) — YES or NO?\n"
            "4. Pick up a basketball (24cm diameter) — YES or NO?\n\n"
            "Answer each on a new line: 1. [YES/NO]"
        ),
        "expected_answer": "1.YES 2.NO 3.YES 4.NO",
        "expected_keywords": ["no", "yes"],
        "paper_model_answer": "Models sometimes say YES to table or basketball — affordance failure",
    },
    {
        "id": "guran2024_G2_action_ordering",
        "paper": "Guran et al., 2024 (Task-Oriented Robotic Manipulation)",
        "task": "Wrong action order — must respect preconditions",
        "failure_type": "BINDING_FAILURE",
        "prompt": (
            "A robot must put a sliced strawberry into a clean bowl.\n"
            "The following actions are available (in scrambled order):\n"
            "A. Place strawberry slice into bowl\n"
            "B. Slice strawberry with knife\n"
            "C. Pick up whole strawberry\n"
            "D. Pick up bowl and verify it is empty\n\n"
            "What is the correct order of actions? Give only the letters in order, e.g. D,C,B,A"
        ),
        "expected_answer": "D,C,B,A",
        "expected_keyword": "d,c,b,a",
        "paper_model_answer": "Paper shows models skip precondition checks (D) or reorder steps incorrectly",
    },
]


# ───────────────────────────────────────────────
# [E] Dao & Vu 2025 — AlphaMaze Navigation
# ───────────────────────────────────────────────

DAO2025_TESTS = [
    {
        "id": "dao2025_maze_simple",
        "paper": "Dao & Vu, 2025 (AlphaMaze)",
        "task": "Simple maze navigation — baseline spatial reasoning",
        "failure_type": "TRAINING_BIAS",
        "prompt": (
            "You are navigating a 3x3 maze. S=start, E=end, #=wall, .=open.\n\n"
            "S . .\n"
            ". # .\n"
            ". . E\n\n"
            "Starting at top-left (S), moving to bottom-right (E).\n"
            "Available moves: right (R), down (D), left (L), up (U).\n"
            "You cannot move through walls (#).\n\n"
            "Give the shortest valid path as a sequence of moves, e.g. R,D,R"
        ),
        "expected_answer": "R,D,D,R or D,R,D,R",
        "expected_keywords": ["r", "d"],
        "paper_model_answer": "Without GRPO training, base models fail even simple mazes. LLaMA-3.1-8B fails ~60%.",
    },
    {
        "id": "dao2025_maze_with_wall",
        "paper": "Dao & Vu, 2025 (AlphaMaze)",
        "task": "Maze with wall obstacle — tests path planning robustness",
        "failure_type": "TRAINING_BIAS",
        "prompt": (
            "Navigate this 4x4 maze. S=start, E=end, #=wall, .=open.\n\n"
            "S . # .\n"
            ". . # .\n"
            ". # . .\n"
            ". . . E\n\n"
            "Give a valid path from S (top-left) to E (bottom-right) "
            "using moves: R=right, D=down, L=left, U=up.\n"
            "You cannot move through # walls or outside the grid.\n"
            "Format: comma-separated moves, e.g. R,D,R,D"
        ),
        "expected_answer": "D,D,D,R,U,R,D,R (one valid path avoiding walls)",
        "expected_keywords": ["d", "r"],
        "paper_model_answer": "Models without spatial grounding training hit walls or go out of bounds",
    },
]


def evaluate_text(expected_keyword: str | list, response: str) -> bool:
    r = response.lower()
    if isinstance(expected_keyword, list):
        return all(k.lower() in r for k in expected_keyword)
    return expected_keyword.lower() in r


def run_suite(name, tests, models):
    print(f"\n{'='*60}")
    print(f"SUITE: {name}")
    print(f"{'='*60}")
    results = []
    for test in tests:
        print(f"\n--- {test['id']} ---")
        print(f"Task: {test['task']}")
        for model in models:
            try:
                response = call_model(model, test["prompt"], max_tokens=200)
                kw = test.get("expected_keywords") or test.get("expected_keyword", "")
                passed = evaluate_text(kw, response)
                result = log_result(
                    paper=test["paper"],
                    test_id=test["id"],
                    failure_type=test["failure_type"],
                    model=model,
                    prompt=test["prompt"],
                    expected=test["expected_answer"],
                    actual=response,
                    passed=passed,
                    notes=test.get("paper_model_answer", "")
                )
                results.append(result)
            except Exception as e:
                print(f"  [ERROR] {model}: {e}")
    return results


def run_tests():
    all_results = []
    all_results += run_suite("Chen 2024 — SpatialVLM", CHEN2024_TESTS, MODELS_TO_TEST)
    all_results += run_suite("Mecattaf 2024 — 3D Embodied", MECATTAF2024_TESTS, MODELS_TO_TEST)
    all_results += run_suite("Xu 2023 — Tool Use", XU2023_TESTS, MODELS_TO_TEST)
    all_results += run_suite("Guran 2024 — Robotic Manipulation", GURAN2024_TESTS, MODELS_TO_TEST)
    all_results += run_suite("Dao 2025 — AlphaMaze", DAO2025_TESTS, REASONING_MODELS)

    print(f"\n{'='*60}")
    print(f"TOPIC 2 OVERALL RESULTS")
    print(f"Total: {sum(1 for r in all_results if r['passed'])}/{len(all_results)} passed")
    for model in MODELS_TO_TEST + [m for m in REASONING_MODELS if m not in MODELS_TO_TEST]:
        model_r = [r for r in all_results if r["model"] == model]
        if model_r:
            p = sum(1 for r in model_r if r["passed"])
            print(f"  {model}: {p}/{len(model_r)}")
    print(f"{'='*60}\n")
    return all_results


if __name__ == "__main__":
    run_tests()
