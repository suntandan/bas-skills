# bas-skills — Claude-verktøy for e-postmarkedsførere

Et lite marketplace med Claude Code-skills laget for deg som jobber med e-post og
marketing automation (Agillic, Dynamics, Salesforce Marketing Cloud eller lignende).
Laget av **Bas Kommunikasjon** for workshopen på **Dialogkonferansen 2026**.

## Hva er dette?

En «skill» er en oppskrift Claude følger når du ber om noe bestemt — f.eks.
«sjekk emnelinjen min» eller «lag en GIF av denne videoen». Skillsene her er
verktøy vi bruker selv i e-posthverdagen:

| Skill | Hva den gjør | Virker i Claude.ai-appen? |
|---|---|---|
| **inbox-summary** | Simulerer hvordan AI-innbokser (Apple Intelligence, Gmail/Gemini) vil oppsummere e-posten din før du sender | ✅ Ja |
| **preheader-check** | Sjekker emnelinje + preheader: lengder, avkutting, lekkasje, samspill — og foreslår 3 varianter | ✅ Ja |
| **email-compatibility** | Sjekker e-post-HTML for klientproblemer (Outlook, Gmail, Apple Mail) og tilgjengelighet | ✅ Ja |
| **gif-konvertering** | Konverterer video eller bildesekvens til animert GIF/WebP for e-post | ⚠️ Krever Claude Code + ffmpeg |
| **research** | Sender ut flere parallelle research-agenter og syr sammen en rapport | ⚠️ Best i Claude Code (subagenter) |
| **consensus** | Stiller samme spørsmål til flere uavhengige agenter og stemmer over svaret | ⚠️ Best i Claude Code (subagenter) |
| **debate** | Strukturert multi-agent-debatt som stress-tester en beslutning | ⚠️ Best i Claude Code (subagenter) |

## Installasjon i Claude Code (anbefalt)

Åpne Claude Code i terminalen og kjør:

```
/plugin marketplace add suntandan/bas-skills
/plugin install epost-verktoy@bas-skills
```

Ferdig. Skillsene trigges automatisk når du ber om noe de dekker — prøv f.eks.:

- «Hvordan vil Apple Intelligence oppsummere denne e-posten?» *(lim inn utkastet)*
- «Sjekk emnelinjen og preheaderen min»
- «Hvorfor ser denne e-posten rar ut i Outlook?» *(lim inn HTML)*
- «Lag en GIF av video.mp4 til nyhetsbrevet»

## Installasjon i Claude.ai-appen (uten Claude Code)

Skills kan også lastes opp som «custom skill» på claude.ai (krever betalt plan
med skills-støtte):

1. Last ned dette repoet (grønn **Code**-knapp → **Download ZIP**) og pakk ut.
2. Zip mappen for skillen du vil ha — f.eks. `plugins/epost-verktoy/skills/preheader-check/`
   (zip-en skal inneholde mappen med `SKILL.md` i).
3. På claude.ai: **Settings → Capabilities → Skills → Upload skill** og last opp zip-en.
4. Gjenta per skill du vil bruke.

**Merk for appen:**
- `inbox-summary`, `preheader-check` og `email-compatibility` er laget for å virke
  fullt ut uten verktøy — de fungerer fint i appen.
- `gif-konvertering` krever **ffmpeg** og et lokalt miljø — kun Claude Code.
- `research`, `consensus` og `debate` bruker **subagenter** (parallelle agenter).
  I appen degraderer de til at Claude gjør vinklene selv, sekvensielt — det
  fungerer, men du mister uavhengigheten som er poenget. Bruk dem helst i Claude Code.

## Startprompter

Skillsene over er ferdige verktøy. Vil du bygge dine egne, ligger tre
startprompter klare til nedlasting:

**<https://work.bas.no/dk26/materiell/>**

| Prompt | Bygger |
|---|---|
| `startprompt-preflight` | Et internt verktøy som sjekker e-poster før utsendelse |
| `startprompt-bildeverktoy` | Et canvas-basert bildeverktøy for markedsavdelingen |
| `startprompt-skill` | En skill som pakker inn et CLI-verktøy, som `/gif-konvertering` |

Kildefilene ligger også i [`prompts/`](prompts/) her i repoet.

## Lisens

MIT — se [LICENSE](LICENSE). Bruk, tilpass og del videre.

---

**Bas Kommunikasjon** · Laget for Dialogkonferansen 2026
