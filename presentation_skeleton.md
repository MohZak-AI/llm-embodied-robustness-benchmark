# Presentation Skeleton: LLM Reasoning Failures in Embodied Robustness

## Slide 1: Title Slide
* **Title:** Visual Truth vs. Linguistic Bias: LLM Reasoning Failures in Embodied Robustness
* **Subtitle:** A Comprehensive Text-Proxy Benchmark of Modern Vision-Language Models
* **Speaker:** Mohammed Moulai, Ahmad El abad, Muman
* **Course/Context:** Selected Topics of Data Science, Seminar 2, Winter 2026

## Slide 2: Introduction to the Field
* **The Domain:** Embodied AI and Multimodal Reasoning sets out to have AI understand and interact with the physical world.
* **The Problem:** Modern Vision-Language Models (VLMs) can write brilliant essays, but frequently fail at elementary spatial logic or physical reasoning.
* **Anchor Study:** Based on *Song et al., 2026 — Large Language Model Reasoning Failures (TMLR)*.
* **Our Core Question:** Do models fail because they have "bad vision," or because they have fundamentally biased "reasoning engines"?

## Slide 3: The 14 Papers Benchmarked
*We consolidated findings from 14 leading papers into 54 discrete tests organized around three topics:*
* **Topic 1: Visual Perception** (e.g., *WHOOPS, BlindTest, ROME Benchmarks*)
* **Topic 2: Spatial & Tool-Use Reasoning** (e.g., *SpatialVLM, AlphaMaze, 3D Embodied Environments*)
* **Topic 3: Safety & Long-Term Autonomy** (e.g., *Code as Policies, BadRobot, EgoNormia*)

## Slide 4: Methodology — The "Text-Proxy" Approach
* **How we tested:** Rather than passing standard benchmark images to the models, we translated the exact spatial and physical layouts from the papers into **explicit text queries**. 
* **The "Why":** If a model fails to analyze a spatial scene when fed a perfect text description, we definitively prove the failure lies in the **Reasoning Brain**, completely isolating it from "Vision Encoder" blurriness or issues.

## Slide 5: The Model Roster
*Evaluated exactly 648 benchmark requests across 12 models via OpenRouter API:*
* **New Frontier:** `gpt-5`, `claude-sonnet-4-6`, `gemini-3-1-pro` 
* **Legacy Frontier:** `gpt-4o`, `claude-3-7-sonnet`, `gemini-2-5-pro`
* **Compact/Reasoning:** `gpt-5-mini`, `o3-mini`, `claude-3-5-haiku`
* **Open Source:** `llama-3-3-70b`, `qwen3-next-80b`, `deepseek-r1`

## Slide 6: High-Level Results
* **Overall Pass Rate:** 77.3% (501 / 648 tasks logic-cleared).
* **Top Performer:** `gpt-5-mini` completely dominated the leaderboard with an astonishing **92.6%**, beating massive legacy models.
* **Open Source Catch Up:** `qwen3-next-80b` hit **85.2%**, beating standard industry models like `gpt-4o`.
* **The Hardest Domain:** *Topic 3 (Safety and Autonomy)* plunged to an overall **69.3%** pass rate.

## Slide 7: Discussion Part 1 — The "Commonsense" Override
* **The Concept:** Training bias violently overwrites explicit instructions.
* **The Test Example:** (Zhou et al., ROME) We told 12 models: *"There is a cow fully inside a microwave."* We asked: *"Is the cow inside?".*
* **The Reality Check:** Only **33.3%** of models correctly passed this. 8 of the 12 models reverted to their training priors ("cows don't fit in microwaves") and refused to acknowledge the truth. 

## Slide 8: Discussion Part 2 — Extreme Prompt Sensitivity
* **Semantic Fragility:** Are LLMs actually reasoning spatially, or just matching patterns?
* We recreated prompt variants from *Zhao 2024* & *Liang 2023*. We changed the grammatical sequence of sentences but kept the exact spatial meaning identical.
* **The Outcome:** A horrific **52.4% pass rate** for prompt sensitivity tasks. The models frequently flipped their answers entirely when the sentence structure changed, proving spatial understanding is dangerously brittle. 

## Slide 9: Discussion Part 3 — The Embodied AI Navigation Gap
* Perceiving a scene statically is easy; but moving efficiently is hard.
* Navigation and heuristic overrides (Maze-Nav counting, physical action sequencing) frequently failed miserably across the board.
* As tasks move from "Identification" to "Action", AI logic severely degrades.

## Slide 10: Conclusion & Takeaways
* **Scaling is Not Everything:** The superiority of logic-distilled models (like `gpt-5-mini`) over sheer parameter-count models proves architectural tuning is beating raw size.
* **The Root of Failure:** Our text-proxy strategy confidently asserts that modern Embodied AI failures aren't just vision bottlenecks; they are rooted in crippling linguistic logic bias.
* **Future Application:** For practical deployment of robotics and agents, training protocols must be designed to successfully untangle an AI's linguistic "commonsense" rulebook from its real-time observational capabilities.
