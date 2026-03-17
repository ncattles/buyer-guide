---
name: skill-designer
description: "Use this skill before building, refactoring, or significantly changing any skill. Triggers include: 'I want to build a skill for X', 'should this be an agent', 'how should I structure this', 'is this the right design', 'should I refactor', 'where should this logic live', 'is my skill getting too big', or any question about the architecture of a skill system. This skill asks the five design questions that prevent the most common skill mistakes: wrong abstraction, wrong location, premature complexity, and no way to know if it worked."
---

# Skill Designer — Architecture Review Before You Build

Run this before writing a single line of skill content. The goal is to make the right structural decisions upfront so you don't accumulate complexity through iteration.

---

## The Five Design Questions

Work through all five before proceeding to build.

### Question 1: What is the single job?

State it in one sentence. Subject → verb → output.

**Examples:**
- "Research and rank products, then generate a PDF buyer's guide."
- "Log mistakes so they aren't repeated."
- "Evaluate whether an app idea is worth building."

**If you can't state it in one sentence, it's probably two skills.** Split it before you build it. A skill that does research AND generates documents AND maintains quality standards is three jobs — which is why buyers-guide.skill grew to 741 lines.

**Red flags:**
- The sentence needs "and also" to be complete
- The skill needs to be read both before tasks AND after tasks
- Different sections of the skill have different trigger conditions

---

### Question 2: What are the distinct phases of work?

List every meaningfully different stage of what the skill does. Each phase is a candidate for its own reference file.

**Example — buyers-guide:**
1. Understand the request (workflow orchestration)
2. Research products (research methodology — Track A–F)
3. Rank and score (business logic — rules, scoring)
4. Generate the document (document generation — template, components)

**If a phase is large enough to have its own sub-rules, sources, and examples, it should be its own file** that SKILL.md reads on demand — not embedded inline.

**Target structure:**
```
skill-name/
├── SKILL.md              (orchestration + pointers — under 300 lines)
└── references/
    ├── phase-1.md        (read when doing phase 1)
    ├── phase-2.md        (read when doing phase 2)
    └── phase-3.md        (read when doing phase 3)
```

SKILL.md tells Claude *when* to read each reference file. Claude reads only what's needed for the current step — not everything upfront.

---

### Question 3: Where does each rule belong?

Every rule should live at the point in the workflow where it's needed — not accumulated in a list at the end of the file.

**Wrong:** 36 Critical Rules at line 700 of a 741-line file.

**Right:** Rule about Price History row lives inside the Step 4 ranking section and the Component 8 product card description — the two places where it's actually applied.

**Test:** For each rule, ask — "When in the workflow does Claude need to know this?" Put it there. If a rule applies in multiple places, put it in the reference file for that phase. A rule at the bottom of a long file is a rule that will be forgotten.

**Accumulated rules at the end of a file are a code smell.** Each one represents a past failure that was patched rather than designed. When you find yourself adding Rule 37, ask whether the workflow step that caused the failure needs redesigning, not just another rule appended to a list.

---

### Question 4: Skill or agent?

Answer these questions:

**Is the work sequential or parallel?**
- Sequential (one step depends on the previous) → skill is fine
- Parallel (multiple independent tasks at once) → agent is better

**Does the reviewer need to be independent from the doer?**
- Same context is fine → skill is fine
- Independent evaluation catches more errors → agent is better

**Is self-review a core quality mechanism?**
- If yes → reconsider. Self-review has a hard ceiling. An agent doing research cannot miss products it's already committed to; a skill can. If quality matters, plan for evals instead of self-review.

**What environment are you in?**
- Claude.ai → agents run sequentially in the same context (limited benefit)
- Claude Code / API → true parallel subagents available (full agent benefit)

**Rule of thumb:** If you find yourself building elaborate self-review mechanisms (multiple audit steps, scenario simulations, checklists), that energy is better spent building 5 eval test cases. Evals catch real failures. Self-review catches known failure patterns.

---

### Question 5: How will you know if it worked?

This is the most important question and the most commonly skipped.

**Define success before you build:**
- What does a correct output look like for this skill?
- What does a wrong output look like?
- What are the 3–5 most important things that must not go wrong?

**Write at least 3 test prompts before writing the skill.** These become your eval set. Run the finished skill against them. If the output is wrong on any test case, the skill isn't done.

**For buyers-guide specifically:** A test prompt of "best prebuilt PC with RTX 5080 and 9800X3D under $3,000" should return a guide that includes Micro Center options. If it doesn't, Track A research is insufficient regardless of what the skill says.

**Evals > self-review, always.** A skill that has been tested against 5 real prompts and passes all of them is more trustworthy than a skill with a 5-step self-review audit that has never been run on a real prompt.

---

## Common Architecture Mistakes

**Mistake 1: One file doing three jobs**
Signs: File has multiple trigger conditions, different sections apply at different times, file exceeds 400 lines.
Fix: Split into orchestration layer + phase reference files.

**Mistake 2: Rules accumulated at the end**
Signs: "Critical Rules" section with 20+ items, rules have numbers, rules reference other rules by number.
Fix: Embed each rule in the workflow step where it applies. Delete the list.

**Mistake 3: Self-review substituting for evals**
Signs: Multi-step audit process, scenario simulations, checklists for declaring "no gaps found."
Fix: Write 5 test prompts. Run the skill. Check the output.

**Mistake 4: Building the wrong abstraction**
Signs: Skill keeps growing to handle edge cases, companion files needed to explain companion files, skill description is a paragraph long.
Fix: Return to Question 1. Restate the single job. Everything outside that job is a different skill.

**Mistake 5: Patching instead of redesigning**
Signs: Each session adds rules/steps/checks, the skill gets longer but not better, the same class of mistake keeps recurring.
Fix: Stop adding. Refactor the workflow step that keeps failing. A new rule at line 700 won't be read when the failure happens at step 3.

---

## Decision Output

After working through all five questions, produce:

1. **The single-sentence job statement**
2. **The proposed file structure** (with line count estimates)
3. **Where each major rule or logic block lives** in the new structure
4. **Skill or agent verdict** with reasoning
5. **The 3 test prompts** you'll use to verify it works

Present this to the user before writing any skill content. Confirm the design is right before building.
