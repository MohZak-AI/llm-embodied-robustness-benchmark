# Presentation Speaker Script
**For: Visual Truth vs. Linguistic Bias: LLM Reasoning Failures in Embodied Robustness**
*Speakers: Mohammed Moulai, Ahmad El abad, Muman*

---

### [Slide 1: Title Slide]
**Speaker 1:**
"Hello everyone, and welcome to our Seminar 2 presentation on Selected Topics in Data Science. Today, my team—Ahmad, Muman, and myself—will be diving into one of the most pressing issues in modern AI: *Visual Truth versus Linguistic Bias*. We've conducted a massive empirical benchmark of 12 top-tier AI models to uncover why state-of-the-art vision models still fail at basic physical reasoning."

### [Slide 2: Introduction to the Field]
**Speaker 1:**
"Let's start by looking at the core problem. Modern AI models are incredible at writing code and generating essays. But when you ask them to interact with physical space—a field known as Embodied AI—they frequently make elementary mistakes. Our core anchor study by Song et al. outlines these failures. The question we wanted to answer today is: Do these models fail because their *vision* is blurry, or because their internal *logic* is fundamentally biased?"

### [Slide 3: The 14 Papers Benchmarked]
**Speaker 2:**
"To answer that, we didn't just run one test. We consolidated findings from 14 leading research papers and built a single, unified benchmark suite of 54 discrete tests. We organized these into three major topics: First, Visual Perception. Second, Spatial and Tool-Use. And third, Safety and Autonomy. This allowed us to test everything from basic object identification to complex maze navigation."

### [Slide 4: Methodology — The "Text-Proxy" Approach]
**Speaker 2:**
"Our methodology is where things get interesting. Normally, you'd test these models using images. Instead, we used a **'Text-Proxy' approach**. We extracted the exact physical layout of the test scenes and fed them to the models purely as explicitly detailed text. Why? Because if an AI fails to analyze a spatial puzzle when given a perfect text description, it unequivocally proves that the failure isn't a 'blurry camera' issue—the failure is deeply embedded inside the AI's core reasoning engine itself."

### [Slide 5: The Model Roster]
**Speaker 3:**
"Armed with this text-proxy suite, we executed 648 benchmark requests across 12 models. We tested the biggest new frontier models like `gpt-5` and `claude-sonnet-4.6`, legacy behemoths like `gpt-4o`, compact reasoning models like `gpt-5-mini`, and top-tier open-source weights like `llama-3` and `qwen3`."

### [Slide 6: High-Level Results]
**Speaker 3:**
"Looking at the high-level results across all 648 tasks, the models achieved a 77.3% overall pass rate. But the true shock was the top performer: *`gpt-5-mini`* dominated the leaderboard with an astonishing 92.6% pass rate, crushing the much larger, older models. We also saw Open Source catching up brilliantly, with `qwen3` hitting over 85%, while tasks in the Safety and Autonomy category dragged the global average down heavily, sitting at just a 69% pass rate."

### [Slide 7: Deep Dive on Topic 1 (Visual Perception)]
**Speaker 1:**
"Let's dive deeper into Topic 1: Visual Perception. This tested basic static logic and counting. Our top models here were the reasoning engines: `gpt-5-mini` and `claude-haiku`. The reason these specific models won is because they strictly evaluate the rules of the prompt you give them, rather than relying on their vast, messy 'world knowledge' which often tricks larger models into making bad assumptions."

### [Slide 8: Deep Dive on Topic 2 (Spatial & Tool-Use)]
**Speaker 2:**
"For Topic 2, we tested dynamic environments—think 3-dimensional maze navigation and distance tracking. Unlike Topic 1, the massive `gpt-5` took first place here with a perfect 100% score. Tracking a complex, multi-step algorithmic path through a 3D maze requires huge matrices of mathematical logic, which is an area where having massive parametric size still provides a structural advantage."

### [Slide 9: Deep Dive on Topic 3 (Safety & Autonomy)]
**Speaker 3:**
"Topic 3 was our toughest domain: Safety and Autonomy. We tested adversarial overrides and strict action boundaries. We actually got a massive 5-way tie at the top here, sitting at an 81% pass rate. The models that succeeded here used what we call 'System 2' thinking—they literally paused their output to explicitly trace the safety boundaries and suppressed their reflex to just 'generate an answer'."

### [Slide 10: Discussion Part 1 — The "Commonsense" Override]
**Speaker 1:**
"To really understand these failures, let's look at a specific flaw we proved: The Commonsense Override from the ROME benchmarks. We told the models, explicitly: *'There is a cow entirely inside a microwave. Is the cow inside?'* Only 33% of the models passed this. The vast majority reverted to their training bias—their brains screamed *'Cows don't fit in microwaves!'*—and they literally refused to acknowledge the truth of the text. They let their bias overwrite reality."

### [Slide 11: Discussion Part 2 — Extreme Prompt Sensitivity]
**Speaker 2:**
"We also discovered Extreme Prompt Sensitivity. We tested variants where we just swapped the grammar of a sentence, but kept the exact physical meaning identical. The models suffered a horrific 52% pass rate on these. They frequently flipped their answers entirely just because the grammatical structure changed. This proves that much of modern AI's spatial understanding is actually just linguistic pattern-matching—it's dangerously brittle."

### [Slide 12: Discussion Part 3 — The Embodied AI Navigation Gap]
**Speaker 3:**
"Finally, we observed the Embodied Navigation Gap. We found that the moment a test shifted from passively *identifying* an object to actively *navigating or sequencing actions* around it, AI logic severely degraded. A model might know what an apple is, but it cannot reliably calculate the physical steps required to safely reach it without collateral damage."

### [Slide 13: Conclusion & Takeaways]
**Speaker 1:**
"To wrap up, our study yielded three major conclusions. First, Scaling is Not Everything; highly-distilled reasoning models frequently beat sheer mass in spatial logic. Second, by using text-proxies, we proved beyond a doubt that Embodied AI failures are rooted in crippling linguistic bias—not just poor vision nodes. And lastly, if we ever want to deploy safe robots in the real world, we must train them to completely untangle their 'commonsense assumptions' from what their sensors are actively telling them. Thank you for listening!"
