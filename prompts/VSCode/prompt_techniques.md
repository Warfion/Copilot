# Prompt Techniques Toolkit

## Purpose
A collection of four reusable prompt strategies designed to extract higher-quality, more structured responses from any LLM or Copilot surface. Each technique shapes the interaction pattern — from guided Q&A to role-based teaching — so the model delivers focused, actionable output instead of generic answers.

Best used with: GitHub Copilot Chat, Microsoft 365 Copilot, any LLM chat interface

---

## Technique 1 — Guided Q&A Discovery

### When to use
You have a broad goal (e.g., choose a technology, design an architecture, pick a strategy) but are unsure which details matter most. Let the model interview you instead of guessing what to specify upfront.

### Prompt

```
I want to [GOAL — e.g., "choose a database for my project" / "design a CI/CD pipeline" / "pick a frontend framework"].

Before making any recommendation, ask me a series of yes/no questions — one at a time — that will help you understand my constraints, preferences, and context. After each answer, decide whether you have enough information or need to ask more.

Once you are confident, provide a single clear recommendation with a brief justification tied to my answers.
```

### Why it works
Forces the model to gather context before committing to an answer, reducing hallucination and generic advice.

---

## Technique 2 — Pros & Cons Comparison

### When to use
You already know roughly what you want but need to evaluate trade-offs between multiple approaches before committing.

### Prompt

```
What are a few different ways I can implement [GOAL — e.g., "authentication in a Next.js app" / "state management in React" / "infrastructure as code for Azure"]?

For each approach:
1. Give a one-sentence summary of how it works.
2. List 3–5 **pros**.
3. List 3–5 **cons**.
4. State when this approach is the best fit (workload size, team skill, timeline).

End with a comparison table and your recommended default choice for a [CONTEXT — e.g., "small team shipping fast" / "enterprise with compliance requirements"].
```

### Why it works
Structures the response around decision-making criteria rather than a single opinion, making it easier to justify your choice to stakeholders.

---

## Technique 3 — Stepwise Chain of Thought

### When to use
You are learning something new or working through a complex, multi-step task and want to stay in control of the pace — reviewing and validating each step before moving on.

### Prompt

```
Help me [GOAL — e.g., "set up a Kubernetes cluster from scratch" / "refactor this module to use dependency injection" / "write integration tests for my API"].

Go one step at a time. For each step:
1. Explain what we are doing and why.
2. Provide the exact action, command, or code.
3. Wait for me to confirm before proceeding.

Do not move to the next step until I give the keyword **"next"**.

Begin.
```

### Why it works
Prevents the model from racing ahead with assumptions. Each checkpoint lets you verify correctness, catch mistakes early, and ask follow-up questions in context.

---

## Technique 4 — Role-Based Interactive Teaching

### When to use
You want to learn a concept or technology through hands-on exercises rather than passive explanation. The model adopts an instructor persona and adapts to your skill level in real time.

### Prompt

```
You are a skilled instructor who makes complex topics easy to understand. You design short, fun exercises so your students learn by doing.

You are teaching me [TOPIC — e.g., "Rust ownership and borrowing" / "Kubernetes networking" / "advanced Git workflows"].

Rules:
- Move one concept at a time.
- After explaining a concept, give me a small exercise or quiz question.
- Wait for my answer before moving on.
- If I give the wrong answer, do not reveal the solution — give me a hint and let me try again.
- After I answer correctly, briefly reinforce why the answer is correct, then move to the next concept.

Begin with the first concept.
```

### Why it works
Mimics active-recall learning — the most effective study method. Hints instead of answers keep you engaged and build genuine understanding.

---

## Quick Reference

| # | Technique | Best for | Key mechanic |
|---|-----------|----------|--------------|
| 1 | Guided Q&A | Decisions with unknown constraints | Model interviews you first |
| 2 | Pros & Cons | Evaluating multiple approaches | Structured trade-off analysis |
| 3 | Stepwise | Complex multi-step tasks | "next" keyword pacing |
| 4 | Role Teaching | Learning new concepts | Interactive exercises with hints |

---

*Source: [Nice Prompts.txt](Nice%20Prompts.txt) • Video reference: https://www.youtube.com/watch?v=H3M95i4iS5c*
