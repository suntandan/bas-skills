---
name: consensus
description: Stochastic consensus skill. Use when the user wants a reliable answer by polling multiple independent agents — filtering hallucinations and surfacing what's consistently true. Trigger on phrases like "er dette riktig", "hva er svaret på", "kan du dobbeltsjekke", "hva mener agentene", "stem over", "konsensus", "stochastic consensus", "poll agents", "filter hallucinations", "get multiple opinions". Also trigger when a factual question has enough uncertainty that a single answer feels unreliable, or when the user wants to know how confident they can be in a claim.
version: 2.0.0
tools: Agent, Write, Bash
---

# Consensus / Stochastic Sampling Skill

## Purpose

Run the same question through N independent agents with slightly varied framing. Aggregate by frequency: what appears consistently across agents is likely true; what appears only once is likely noise or hallucination.

**Key principle:** Agents never see each other's responses. Independence is everything. This is redundancy + voting, not debate.

**Analogy:** Asking 10 independent witnesses what they saw. The consistent descriptions are reliable; the outliers are noise.

---

## Step 1 — Parse Parameters

Extract from the user's message:

| Parameter | Default | Description |
|---|---|---|
| `QUESTION` | *(required)* | The question or decision to analyze |
| `N` | `5` | Number of agents (more = more reliable, max 10) |
| `AGGREGATOR_MODEL` | `opus` | Model for the aggregator/judge |
| `AGENT_MODEL` | `sonnet` | Model for the individual agents |

If `QUESTION` is missing, ask the user before proceeding.

### Lagring

Spør brukeren før agentene spawnes:

> "Hvor vil du lagre consensus-rapporten? Standard er `./research/` — trykk Enter for å bruke det, eller oppgi en annen sti."

Bruk `./research/` som fallback. Generer filnavn fra spørsmålet: lowercase, mellomrom til bindestreker, dato-prefix og `-consensus`-suffiks.
Eksempel: `2026-04-16-dobbel-opt-in-consensus.md`

Hent dato med: `date '+%Y-%m-%d'`

**Example invocations:**
- `/consensus Er dobbel opt-in riktig for nyhetsbrevet vårt?`
- `/consensus Rank these three options: [A, B, C] n:7`
- `/consensus [question] n:10 agent:haiku aggregator:opus`

Before starting, tell the user:
> "Running consensus: [N] independent agents on [AGENT_MODEL], aggregated by [AGGREGATOR_MODEL]"

---

## Step 2 — Generate Framing Variations

Before spawning agents, create N slightly different framings of the same question. Variations should:
- Ask for the same underlying answer
- Approach from slightly different angles (direct, analytical, practical, critical, comparative...)
- NOT lead the agent toward a specific answer

**Example for "Er dobbel opt-in riktig for nyhetsbrevet vårt?":**
1. "What are the key factors that determine whether double opt-in is the right choice for an email newsletter?"
2. "When would you recommend double opt-in for email signups, and when would you recommend single opt-in?"
3. "What are the strengths and weaknesses of double opt-in as a signup strategy?"
4. "A marketing team is designing a newsletter signup flow. Evaluate double opt-in as an option."
5. "What does the evidence say about double opt-in's effect on list quality and deliverability?"

Tell the user the framing variations you're using before spawning.

---

## Step 3 — Spawn N Independent Agents (parallel)

Spawn **all N agents in a single message** (parallel tool calls). Agents must never see each other's responses.

For each agent use:
- `subagent_type: "general-purpose"`
- `model: AGENT_MODEL`

Agent prompt template:
```
You are an independent analyst. Answer the following question as directly and accurately as possible.

Question: [FRAMING VARIATION i]

Return:
## Answer
[Your direct answer — be specific, not vague]

## Key Points
[3-5 bullet points supporting your answer]

## Confidence
[low / medium / high] — [one sentence explaining why]

## Caveats
[Any important exceptions, edge cases, or conditions that would change your answer]

Write in Norwegian (bokmål).
```

---

## Step 4 — Aggregate Results

After all N agents respond, spawn one aggregator agent:
- `subagent_type: "general-purpose"`
- `model: AGGREGATOR_MODEL`

Aggregator prompt:
```
You have received [N] independent responses to the following question:

Question: [ORIGINAL QUESTION]

Responses:
Agent 1: [full output]
Agent 2: [full output]
...
Agent N: [full output]

Your task is to aggregate these responses by consensus — not by averaging, but by identifying what is consistently true across independent sources.

## Consensus Answer
What answer appears most consistently across agents? State it clearly. If agents genuinely disagree, describe the split.

## High-Confidence Points
Points that appeared in [N-1] or more responses — treat these as reliable.

## Low-Confidence Points
Points that appeared in only 1-2 responses — flag these as potential noise or hallucination.

## Outliers
Any answer that diverges significantly from the others. Note it — outliers can be wrong, but occasionally they surface a genuinely important minority view.

## Consensus Strength
[strong / moderate / weak] — How much did agents agree? 
- Strong: N-1 or more agents converged on the same answer
- Moderate: Clear majority, some variation in details
- Weak: Agents were genuinely split — no clear consensus

## Final Verdict
Your synthesized, authoritative answer to the original question. Be direct.

Write in Norwegian (bokmål).
```

---

## Step 5 — Save and Present

1. Save the complete consensus report to the resolved file path using the `Write` tool.
2. Present to the user:
   - **Consensus answer** (prominently)
   - **Consensus strength** signal
   - **High-confidence points** (appeared in most agents)
   - **Low-confidence points / outliers** (appeared in few agents — treat with skepticism)
   - **Metadata**: "[N] agents | [AGENT_MODEL] → [AGGREGATOR_MODEL]"
3. Note: "Rapport lagret til `[filepath]`"
4. Offer to show the raw individual agent responses if the user wants to inspect them.

---

## Quality Checklist

Before finishing, verify:
- [ ] All N agents ran in parallel (single message)
- [ ] Each agent received a different framing variation
- [ ] No agent saw another agent's response
- [ ] Aggregator received ALL agent outputs
- [ ] High-confidence and low-confidence points are clearly distinguished
- [ ] Consensus strength is honestly assessed (don't inflate weak consensus)

---

## Anti-Patterns to Avoid

- **Never** let agents see each other's responses — this becomes `/debate`, not `/consensus`
- **Never** use identical framings for all agents — slight variation is essential for stochastic sampling
- **Never** treat a weak consensus as a strong one — be honest about disagreement
- **Never** dismiss outliers without noting them — occasional outliers surface important edge cases
- **Watch for uniform high confidence** — if all agents are highly confident and agree instantly, the question may be too easy for consensus to add value
