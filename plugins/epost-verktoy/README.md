# epost-verktoy

Claude Code-plugin med syv skills for e-postmarkedsføring. Del av
[bas-skills](https://github.com/suntandan/bas-skills)-marketplacet fra
Bas Kommunikasjon.

## Skills

- **inbox-summary** — Simulerer AI-innboks-sammendrag (Apple Intelligence,
  Gmail/Gemini) av et e-postutkast før utsendelse, og vurderer om hovedbudskap
  og CTA overlever.
- **preheader-check** — Analyserer emnelinje + preheader + «over folden»:
  lengdegrenser per klient, avkuttingssimulering, lekkasjesjekk og tre
  alternative varianter.
- **email-compatibility** — Sjekker e-post-HTML for kjente klientproblemer
  (Outlook Word-motor, OLK align-bug, Gmail-begrensninger, Apple Mail) og
  tilgjengelighet. Svarer også på «hvorfor ser dette rart ut i Outlook?».
- **gif-konvertering** — Video eller bildesekvens → animert GIF/WebP for e-post,
  med palette-optimalisering, transitions og `<picture>`-fallback. Krever ffmpeg.
- **research** — Fan-out/fan-in: N parallelle researcher-agenter + synthesizer,
  lagrer rapport til `./research/`.
- **consensus** — Samme spørsmål til N uavhengige agenter, aggregert etter
  frekvens: det konsistente er sannsynligvis sant, outliers er støy.
- **debate** — Strukturert multi-agent-debatt over K runder med dommer til slutt.

## Installasjon

```
/plugin marketplace add suntandan/bas-skills
/plugin install epost-verktoy@bas-skills
```

## Krav

- `gif-konvertering`: ffmpeg/ffprobe i PATH (skillen forklarer installasjon hvis de mangler).
- `research`, `consensus`, `debate`: bruker subagenter — best i Claude Code.
- Resten virker uten verktøy, også i Claude.ai-appen som opplastet custom skill.

## Lisens

MIT © Bas Kommunikasjon
