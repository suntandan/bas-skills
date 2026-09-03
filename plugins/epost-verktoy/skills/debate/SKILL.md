---
name: debate
description: Multi-agent debate / stochastic consensus skill. Use when the user wants to explore a question from multiple angles, stress-test a decision, or find the answer that survives scrutiny. Trigger on phrases like "debatt", "konsensus", "hva er best", "er X bedre enn Y", "bør vi velge", "stochastic consensus", "multi-agent debate", "argue from multiple angles", "debate", "structured debate", "hvilken tilnærming", "hva tenker agentene". Also trigger when the user faces a non-obvious decision or trade-off that would benefit from independent reasoning from multiple perspectives.
version: 2.0.0
tools: Agent, Write, Bash
---

# Debate / Stochastic Consensus Skill

## Purpose

Run a structured multi-agent debate where N agents independently form positions, then iteratively update them after seeing each other's reasoning. A judge synthesizes the final consensus verdict.

**Key insight:** This is NOT a pro/con debate. All agents are truth-seeking. The debate emerges from agents cross-checking each other's reasoning and updating when they find compelling arguments. "Stochastic consensus" = the answer that survives across agents and rounds.

---

## Step 1 — Parse Parameters

Extract from the user's message:

| Parameter | Default | Description |
|---|---|---|
| `QUESTION` | *(required)* | The question or topic being debated |
| `N` | `3` | Number of debater agents (max 5) |
| `K` | `2` | Number of debate rounds (max 4) |
| `DEBATER_MODEL` | `sonnet` | Single model for all debaters (`haiku`, `sonnet`, `opus`) |
| `MODELS` | *(unset)* | Per-agent models — overrides DEBATER_MODEL (see below) |
| `JUDGE_MODEL` | `opus` | Model for the judge (`haiku`, `sonnet`, `opus`) |

If `QUESTION` is missing, ask the user before proceeding.

### Lagring

Spør brukeren før debatten starter:

> "Hvor vil du lagre debatt-rapporten? Standard er `./research/` — trykk Enter for å bruke det, eller oppgi en annen sti."

Bruk `./research/` som fallback. Generer filnavn fra spørsmålet: lowercase, mellomrom til bindestreker, dato-prefix og `-debate`-suffiks.
Eksempel: `2026-04-16-ukentlig-vs-maanedlig-nyhetsbrev-debate.md`

Hent dato med: `date '+%Y-%m-%d'`

### Multi-model mode

If the user specifies `models:` with a comma-separated list, assign one model per debater. N is inferred from the list length.

| Syntax | Example | Result |
|---|---|---|
| `debater:sonnet` | All agents use sonnet | Single-model mode |
| `models:haiku,sonnet,opus` | Agent 1=haiku, Agent 2=sonnet, Agent 3=opus | Multi-model mode |

**Multi-model tip:** Different models bring genuinely different "personalities":
- `haiku` — fast, direct, sometimes overconfident
- `sonnet` — balanced, practical, good at nuance
- `opus` — slower, more thorough, better at spotting flaws

When multi-model mode is active, include the model name in debater labels (e.g. "Debater 1 (haiku)") so the user can track which model argued what.

**Example invocations:**
- `/debate Er emoji i emnefeltet verdt det for merkevaren vår?`
- `/debate Er ukentlig eller månedlig nyhetsbrev best for engasjement? n:4 k:3`
- `/debate [question] models:haiku,sonnet,opus judge:opus`
- `/debate [question] n:5 k:2 debater:haiku judge:opus`

Before starting, tell the user:
> "Starting debate: [N] agents ([model list or single model]), [K] rounds, judge=[JUDGE_MODEL]"

---

## Step 2 — Round 0: Independent Positions (parallel)

Spawn **all N agents in a single message** (parallel tool calls). Each agent must NOT see the others' views.

For each debater agent use:
- `subagent_type: "general-purpose"`
- `model: MODELS[i]` (multi-model mode) or `DEBATER_MODEL` (single-model mode)

Debater Round 0 prompt:
```
You are Debater [i] of [N] in a structured multi-agent consensus debate.

Question: [QUESTION]

This is Round 0. You must form your position INDEPENDENTLY — do not assume what others might say.

Return exactly this structure:

## Position
[Your answer in 1-3 sentences]

## Reasoning
[3-5 bullet points explaining your key arguments and evidence]

## Confidence
[low / medium / high] — [1-2 sentences explaining why]

## What Would Change My Mind
[What evidence, logic, or argument would cause you to update your position]

Write in Norwegian (bokmål).
```

After all Round 0 responses arrive, show the user a brief summary table:

| Debater | Position (short) | Confidence |
|---------|-----------------|------------|
| Agent 1 | ... | medium |
| Agent 2 | ... | high |
| Agent 3 | ... | low |

---

## Step 3 — Rounds 1 to K: Update Based on Others' Views

For each round k from 1 to K, spawn **all N agents in a single message** (parallel).

For each debater agent use:
- `subagent_type: "general-purpose"`
- `model: MODELS[i]` (multi-model mode) or `DEBATER_MODEL` (single-model mode)

Debater Round k prompt:
```
You are Debater [i] of [N] in a structured multi-agent consensus debate.

Question: [QUESTION]
This is Round [k] of [K].

--- All agents' positions from Round [k-1] ---
Debater 1: [full Round k-1 output from Agent 1]
Debater 2: [full Round k-1 output from Agent 2]
...
Debater N: [full Round k-1 output from Agent N]
---

Your position from Round [k-1]:
[Agent i's Round k-1 output]

Now carefully review the other agents' reasoning. Then return:

## Updated Position
[Your current answer — updated or unchanged]

## What Changed (and Why)
[Did you update your view? If yes: what argument convinced you and why. If no: explain why the others' arguments were not sufficient to change your mind]

## Strongest Argument from Another Agent
[Quote or paraphrase the strongest argument from any other agent — even if you disagree with it]

## Current Confidence
[low / medium / high] — [brief explanation]

Write in Norwegian (bokmål).
```

After each round, show the user a consensus signal:

**Round [k] Consensus Signal:**
- Converging: [X/N agents hold similar positions]
- Diverging: [Y/N agents hold different positions]
- Confidence trend: [rising / falling / stable]

If all N agents converge on the same position before K rounds are complete, stop early and note: "Early consensus reached after [k] rounds."

---

## Step 4 — Judge: Final Verdict

After the final debate round, spawn a single judge agent:
- `subagent_type: "general-purpose"`
- `model: JUDGE_MODEL`

Judge prompt:
```
You are the judge in a structured multi-agent debate. Your role is to synthesize the debate and deliver a final verdict.

Question: [QUESTION]

Complete debate transcript ([K] rounds, [N] agents):

=== ROUND 0 ===
Debater 1: [full output]
Debater 2: [full output]
...

=== ROUND 1 ===
Debater 1: [full output]
Debater 2: [full output]
...

[... all rounds ...]

Your task:

## Consensus Verdict
Was consensus reached? How strong is it? What is the consensus answer?

## Strongest Arguments
Which arguments (across all agents and rounds) were most compelling and why?

## Remaining Disagreements
What points of genuine disagreement persist, and why might reasonable agents still disagree?

## Quality of Reasoning
Did agents update their views based on evidence/logic, or did they dig in regardless? Were any updates too quick (sycophantic)?

## Final Answer & Confidence
Your authoritative final answer to the question, with a confidence level (low / medium / high) and a brief justification. Be direct — this is your verdict, not a summary.

Write in Norwegian (bokmål).
```

---

## Step 5 — Save and Present

1. Save the complete debate report to the resolved file path using the `Write` tool.

   The file should contain:
   - Header: `# Debatt: [QUESTION]`
   - Metadata: dato, modeller, antall runder
   - Posisjonsutvikling per agent per runde (tabell)
   - Konsensus-signal-utvikling (Runde 0 → Runde K)
   - Dommerens fulle konklusjon

2. Present the report to the user in the conversation.
3. Note: "Rapport lagret til `[filepath]`" and mention which models and rounds were used.
4. Offer to share the full raw debate transcript if the user wants to read individual agent responses.

---

## Quality Checklist

Before finishing, verify:
- [ ] Round 0 spawned all N agents in parallel (single message)
- [ ] Each subsequent round also spawned all N agents in parallel
- [ ] Each agent received ALL other agents' previous-round outputs
- [ ] Consensus signal was computed and shown after each round
- [ ] Judge received the complete transcript across all rounds
- [ ] Final output includes verdict, strongest arguments, and remaining disagreements

---

## Anti-Patterns to Avoid

- **Never** allow agents to see others' positions in Round 0 — independence is critical
- **Never** run debate rounds sequentially when they should be parallel
- **Never** let the judge produce a verdict without the full transcript
- **Never** stop early just because opinions differ — check for genuine convergence
- **Watch for sycophancy**: if all agents immediately agree in Round 1 without substantive reasoning, note this as a weak debate signal
