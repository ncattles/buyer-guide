# Evals — Future Architecture

**Reference:** [Demystifying Evals for AI Agents — Anthropic Engineering](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

This doc captures eval architecture gaps identified against Anthropic's framework. These are not immediate priorities — computation cost and complexity are real tradeoffs — but worth revisiting as the pipeline matures.

---

## What the pipeline has today

- **Code-based graders (C1–C14):** Schema validation, binary assertions on contract shape and required fields. Fast, deterministic, cheap.
- **Transcript/trace:** `research_log.json` records every search query and Playwright fetch with price, stock, page title, and screenshot. This is the prerequisite for most of the improvements below.
- **Stage-boundary contracts:** Every stage produces a validated JSON output. A bad output cannot silently corrupt the next stage.

These map to what the article calls *regression evals* — they maintain near-100% pass rates and catch format/contract degradation.

---

## Gaps

### 1. No capability evals

Current evals test *format*, not *process quality*. None assert that the pipeline achieved its actual purpose.

A capability eval for this pipeline: run a known category where the correct answer is a product that editorial sources systematically miss (the Micro Center problem), and assert the pipeline finds it.

Requires: a small set of "known answer" test fixtures — categories where the right winner has already been verified manually.

**Cost:** Low. Code-based, runs fast. The hard part is building the ground-truth fixture set.

---

### 2. No model-based graders

Some quality signals can't be code-checked:
- Is the scoring rationale coherent given the spec flags?
- Did Track A's retailer list reflect genuine discovery or just obvious names?
- Is the community sentiment classification defensible given the sources cited?

A model-based grader evaluates these with a rubric. The article recommends calibrating model graders against human graders before trusting them.

**Cost:** High. Non-deterministic, slower, and costs tokens per eval run. Worth it only for quality signals that matter and can't be formalized into schema rules.

---

### 3. No multi-trial / determinism measurement

The pipeline runs once per request with no way to measure consistency. The article's `pass^k` metric (all k trials agree) would quantify how deterministic scoring actually is — does the same request on the same day produce the same top pick?

Relevant here because: prices change, stock changes, research agents are non-deterministic by nature. The schema enforces process; it doesn't enforce outcome stability.

**Cost:** High. Running the full pipeline 3–5x per eval case multiplies Playwright fetches, API calls, and time.

---

### 4. No simulated intake agent

Testing intake currently requires a human to answer every question. A fixture-based simulated user (category, budget, city, filters pre-seeded) would allow full pipeline runs in CI without human interaction.

The article recommends "a second LLM to simulate the user" for conversational agents.

**Cost:** Medium. One-time build cost; cheap to run after.

---

## Priority order if revisiting

1. **Capability evals** — highest leverage, lowest cost. Directly tests the stated goal of the tool (find what editorial sources miss). Requires building known-answer fixtures.
2. **Simulated intake agent** — enables fully automated end-to-end CI runs. Medium build cost.
3. **Model-based graders** — for quality signals that schema can't catch. High cost; defer until capability evals are saturating.
4. **Multi-trial / pass^k** — for determinism measurement. Expensive; only worth it if consistency becomes a known problem.

---

## Note on cost

Every improvement here adds API calls, Playwright fetches, or both. The pipeline is already expensive per run. These improvements are additive — each one compounds the cost. The right time to invest is when the pipeline is stable enough that eval quality is the limiting factor, not when the process itself is still being refined.
