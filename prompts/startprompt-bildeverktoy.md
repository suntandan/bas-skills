# Startprompt: bygg et canvas-basert bildeverktøy (som Rikstoto Kampanjebilder)

Lim inn i Claude Code i en tom mappe. Bytt ut det som står i «⟨⟩». Mønsteret
passer for alle verktøy der en ikke-teknisk bruker skal legge tekst, merker
og grafikk oppå et bilde og laste ned resultatet: kampanjebilder, SoMe-kort,
webinar-thumbnails, produktbanner.

---

## Prompt

Vi skal bygge et lite internt verktøy der ⟨markedsavdelingen⟩ kan laste opp
et bilde, legge på ⟨tekst, datomerke og dekorative elementer⟩, dra dem på
plass, og laste ned resultatet i ⟨e-postvennlige bredder⟩.

**Stack**: ⟨Vite + React + TypeScript + Tailwind v4⟩. Ingen router, ingen
state-bibliotek — `useState` holder. **Ingen backend.** All bildebehandling
skjer i nettleseren; kundens bilder skal aldri lastes opp noe sted.
Produksjonsbygget er ren statisk `dist/` som kan legges på ⟨kundens egen
webserver⟩.

### Ufravikelige designprinsipper

1. **Én tegnefunksjon, to bruksområder.** `drawLayer(ctx, layer, w, h)` er
   eneste sted som vet hvordan et lag ser ut. Både preview-canvaset og
   eksporten kaller den samme løkken. Dette er prosjektets #1 invariant:
   i det øyeblikket noen tegner noe utenom `drawLayer`, begynner eksporten
   å avvike fra det brukeren så — og det oppdages først hos mottakeren.
2. **Normaliserte koordinater.** Alt geometrisk (`x`, `y`, `width`,
   `fontSize`, padding, borderWidth) lagres som brøk 0–1 av basisbildets
   bredde, ikke i piksler. Da overlever et oppsett både at preview-canvaset
   endrer størrelse og at eksporten skjer i vilkårlig bredde. Skriv enheten
   i en doc-kommentar på hvert felt — «fraction of base image width» — ellers
   sniker piksler seg inn igjen ved neste lagtype.
3. **Lagtyper som diskriminert union.** `type Layer = TextLayer | PillLayer |
   ImageLayer`, alle med `type`-felt. Å legge til en ny type skal treffe
   nøyaktig fire steder: unionen, en gren i `drawLayer`, en konstruktør, og
   et skjema i egenskapspanelet. Dokumenter de fire stedene i CLAUDE.md.
4. **Hit-testing bruker samme geometri som tegningen.** Klikk-treff og
   markeringsramme utledes av samme bbox-funksjon som `drawLayer` tegner
   etter — ikke en parallell beregning. To sett geometri driver alltid fra
   hverandre.
5. **Eksport er synkron med det som er lastet.** Bildelag tegnes fra en
   modulnivå-cache av `HTMLImageElement`. `drawLayer` er synkron og hopper
   over bilder som ikke er ferdig lastet; eksporten venter derfor på alle
   bitmaps *før* den tegner. Ellers får du tomme hull i filen brukeren laster
   ned, uten feilmelding.
6. **Direkte manipulasjon skal føles riktig.** Pointer events med
   `setPointerCapture` (ikke mouse events), canvas skalert etter
   `devicePixelRatio`, og snapping mot kanter, senter og et valgfritt rutenett
   med synlige hjelpelinjer. Terskel i visningspiksler, ikke normaliserte
   enheter — snapping skal kjennes like «sterk» uansett zoom.

### Struktur

- `types.ts` (unionen) → `layers.ts` (`drawLayer`, konstruktører, bbox,
  hit-test, bildecache) → `utils/export.ts` → komponentene.
- Panelene: opplasting/bibliotek, lagliste, egenskapspanel. `layers[0]` er
  nederst i stabelen; laglisten viser rekkefølgen reversert så det øverste
  laget står først — det er den eneste vendingen, og den hører hjemme i
  visningen, ikke i datamodellen.
- **Assets oppdages automatisk** med `import.meta.glob` over
  `src/assets/⟨backgrounds⟩/` og `src/assets/⟨elements⟩/`. Slipp en fil i
  mappa, restart dev-serveren, den er i biblioteket. Ingen manuell
  registrering — det er alltid den listen som blir utdatert.
- **Maler** som genererer bakgrunn + ferdige lag i ett kall gir mest verdi
  for målgruppen. Start med ⟨to–tre⟩ ekte oppsett, ikke et generisk
  mal-rammeverk.

### Fremgangsmåte

Foreslå en faseplan før du koder.

- **Fase 1**: datamodell, `drawLayer` for én lagtype, preview og eksport.
  Verifiser mot et ekte bilde at eksporten i ⟨600 px⟩ er pikselidentisk med
  preview før noe annet bygges.
- **Fase 2**: interaksjon — markering, drag, snapping, tastatur.
- **Fase 3**: resten av lagtypene, maler, assets-bibliotek, eksportpresets.

Ikke start på fase 2 før eksporten stemmer. Alt jeg må korrigere underveis
som handler om arkitektur, skriv inn i CLAUDE.md med en gang.

---

## Avklar før du starter

- **Bredder og format**: hvilke eksportbredder trenger kanalen faktisk?
  ⟨290/600/1200⟩ for e-post. PNG beholder kvalitet, JPEG med ~0.92 er som
  regel riktig standardvalg — sett det, ikke spør brukeren hver gang.
- **Fonter**: brandfonten må hostes lokalt (`public/fonts/`) og lisensen må
  dekke det. Systemfont-fallback gir feil bokstavbredder og dermed feil
  linjebrekk i eksporten — avklar lisensen før, ikke etter.
- **Brand-assets**: skaff logoer, dekorelementer og fargekoder først. Verktøy
  som ser «nesten riktig» ut i profil blir ikke brukt.
- **Språk**: ⟨norsk⟩ i grensesnittet, engelsk i koden. Bestem det i første
  commit — blandede identifikatorer er ikke verdt å rydde opp i senere.
