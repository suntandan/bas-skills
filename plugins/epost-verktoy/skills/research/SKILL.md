---
name: research
description: Fan-out / fan-in deep research skill. Use this skill whenever the user wants to explore a topic in depth — even if they don't use the word "research". Trigger on phrases like "finn ut om", "hva vet vi om", "kan du se på", "deep dive", "undersøk", "sammenlign", "hva er forskjellen på", "hvilke alternativer finnes", "research", "parallel research", "researcher-agenter". Also trigger when the user asks about a tool, platform, competitor, technology, or industry context that would benefit from structured multi-angle investigation.
version: 2.0.0
tools: Agent, WebSearch, WebFetch, Write, Bash
---

# Research Skill — Fan-out / Fan-in

## Purpose

Run N parallel researcher agents on a topic, synthesize findings into a structured Norwegian report, and save it to a Markdown file.

---

## Step 1 — Parse Parameters

Extract from the user's message:

| Parameter | Default | Description |
|---|---|---|
| `TOPIC` | *(required)* | The subject to research |
| `N` | `3` | Number of parallel researchers (max 5) |
| `RESEARCHER_MODEL` | `sonnet` | Model for researchers (`haiku`, `sonnet`, `opus`) |
| `SYNTHESIZER_MODEL` | `opus` | Model for synthesizer (`haiku`, `sonnet`, `opus`) |

If `TOPIC` is missing, ask the user before proceeding. Use defaults for everything else unless specified.

**Example invocations:**
- `/research sammenlign e-postplattformer for mellomstore bedrifter` → N=3, researchers=sonnet, synthesizer=opus
- `/research hva gjør konkurrentene i nyhetsbrevene sine n:4`
- "Kan du undersøke hvordan dark mode fungerer i Outlook med 5 forskere?"

---

## Step 2 — Ask Where to Save

Before spawning agents, ask the user:

> "Hvor vil du lagre research-rapporten? Standard er `./research/` — trykk Enter for å bruke det, eller oppgi en annen sti."

Use `./research/` as fallback if the user doesn't specify or says "standard"/"default".

Generate a filename from the topic: lowercase, spaces to hyphens, date-prefixed.
Example: `2026-04-16-sammenlign-epostplattformer.md`

Get today's date with: `date '+%Y-%m-%d'`

---

## Step 3 — Determine Research Angles

Before spawning agents, decide on **N distinct, non-overlapping angles** tailored to the specific topic. The goal is to cover what would actually be most useful to know — not just what's generically available.

Think: *What kind of question is this?* Then pick the angle pattern that fits:

**Platform / tool evaluation** (e.g. "plattform A vs plattform B", "skal vi bytte ESP?")
- Funksjoner og kapabiliteter
- Begrensninger og kjente problemer
- Pris, lisensmodell og skalerbarhet
- Kundestøtte, community og modenhet
- Migreringskost og integrasjonsmuligheter

**E-post / teknisk** (e.g. "dark mode i Outlook", "CSS-støtte i Gmail")
- Nåværende støtte og kjente bugs
- Workarounds og beste praksis
- Klientspesifikke særheter
- Fremtidsplaner og standardisering
- Praktiske eksempler og testresultater

**Kundes bransje / marked** (e.g. "forsikringsbransjen i Norge", "spillmarkedet")
- Markedsstruktur og nøkkelaktører
- Regulatoriske krav og compliance
- Kommunikasjons- og kanalstrender
- Konkurrentenes tilnærming
- Forbrukertrender og preferanser

**Konkurranselandskap** (e.g. "hva gjør konkurrentene til X?")
- Hvem er aktørene og hva tilbyr de
- Prising og posisjonering
- Styrker og svakheter per aktør
- Differensieringsmuligheter
- Trender som påvirker landskapet

**Generell / åpen** — hvis temaet ikke passer noen av over, utled vinkler organisk fra hva som ville vært mest verdifullt å vite. Unngå generiske "fundamentals / pros / cons"-vinkler med mindre de faktisk er relevante.

Tell the user which angles you're using before spawning.

---

## Step 4 — Fan-out (Parallel Researchers)

Spawn **all N agents in a single message** (parallel tool calls) — never sequentially.

For each researcher agent:
- `subagent_type: "general-purpose"`
- `model: RESEARCHER_MODEL`

Each researcher prompt:
```
You are a focused research agent. Your specific research angle is: [ANGLE]

Topic: [TOPIC]

Instructions:
1. Use WebSearch and WebFetch to find current, authoritative sources
2. Search for at least 3-5 relevant sources
3. Extract key facts, insights, examples, and data points
4. Note any conflicting information or debates in the field
5. Return your findings as structured markdown with these sections:
   ## Key Findings
   ## Supporting Evidence & Sources
   ## Notable Debates / Open Questions
   ## Relevance to [TOPIC]

Be thorough but focused on your assigned angle. Do not stray into other angles.
Cite specific URLs or sources where possible.
Write in Norwegian (bokmål).
```

---

## Step 5 — Fan-in (Synthesizer)

After **all** researcher agents have returned, spawn a single synthesizer agent:
- `subagent_type: "general-purpose"`
- `model: SYNTHESIZER_MODEL`

Synthesizer prompt:
```
You are a research synthesizer. You have received findings from [N] parallel research agents on the topic: [TOPIC]

Here are their reports:

---
[RESEARCHER 1 ANGLE]: [RESEARCHER 1 OUTPUT]
---
[RESEARCHER 2 ANGLE]: [RESEARCHER 2 OUTPUT]
---
[... repeat for all researchers ...]
---

Your task is to synthesize all findings into one coherent, well-structured research report in Norwegian (bokmål).

Use this structure:

# [TOPIC] — Forskningsrapport

> [1-2 setninger som oppsummerer rapporten og dens formål]

## Sammendrag
3-5 kulepunkter med de viktigste funnene.

## Bakgrunn og kontekst
Grunnlag for å forstå temaet.

## Funn per tema
Organiser funnene tematisk (ikke per forsker). Sammenlign og kontraster der forskerne fant ulik eller komplementær informasjon. Bruk Mermaid-diagrammer der det gir visuell verdi — f.eks. sammenligninger, relasjoner, tidslinje. Ikke bruk Mermaid bare for å bruke det.

## Nøkkelinnsikter
Tverrgående innsikter som fremkommer av å kombinere vinklene.

## Konklusjoner og anbefalinger
Hva bør leseren vite, gjøre eller beslutte basert på denne forskningen?

## Kilder og referanser
List opp alle siterte kilder fra forskernes rapporter.

---

Write analytically, not just descriptively. Highlight where evidence is strong vs. uncertain. Format for easy scanning — use headers, bullet points, and tables where helpful.
```

---

## Step 6 — Save and Present

1. Save the synthesized report to the resolved file path using the `Write` tool.
2. Present the report to the user in the conversation.
3. Note: "Rapport lagret til `[filepath]`" and mention which models were used.
4. Offer to dive deeper on any section.

---

## Quality Checklist

- [ ] User was asked where to save (or fallback used)
- [ ] All N researcher agents ran in parallel (single message)
- [ ] Each researcher had a distinct, non-overlapping angle suited to the topic type
- [ ] Researchers wrote in Norwegian
- [ ] Synthesizer received ALL researcher outputs
- [ ] Final report is in Norwegian with all required sections
- [ ] Mermaid used where it adds value (not forced)
- [ ] Report saved to file
- [ ] Sources are listed and traceable
