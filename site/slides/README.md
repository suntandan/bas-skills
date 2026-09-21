# slides/

DK26-presentasjonen som frittstående statisk side. Publiseres på
`work.bas.no/dk26/slides/` — last opp hele `slides/`-mappa som den er.

Kilden ligger i Claude Design («DK26 design review», fila `DK26 Slides.dc.html`).
Her er den pakket om så den virker uten Claude Design-editoren, og uten nett.

## Før presentasjonen

Rediger `deck-config.js`:

```js
window.DK26 = {
  "wifiPassord": "GanskeVanskelig",                     // vises på slide 1 og 13
  "urlPrompt": "https://work.bas.no/dk26/materiell/",
  "urlRapport": "https://work.bas.no/dk26/rapport/",    // QR på slide 16
  "urlRepo": "https://github.com/suntandan/bas-skills",
  "visThumbnails": false                                // stripa til venstre
};
```

Så:

```bash
python3 bygg.py
```

Tomme felter degraderer pent: passordet vises som `[fylles inn]`, og et QR-felt
uten url står bare tomt (slik originalen er satt opp).

## Bygging

`bygg.py` lager `index.html` fra `src/DK26 Slides.dc.html`. Fem ting endres,
alt annet er kilden uendret:

1. **React, ReactDOM og Babel** hentes fra `vendor/` i stedet for unpkg.
   dc-runtime har en krok for dette — `window.__resources` — så vi slipper å
   patche `support.js`.
2. **Fontene** (Press Start 2P, IBM Plex Mono, Satoshi) hentes fra `fonts/`
   i stedet for Google Fonts og Fontshare.
3. **`deck-config.js`** lastes, så wifi-passord og url-er er faste verdier
   i stedet for «Åpne felter» i editoren.
4. **QR-kodene** er ferdige PNG-er i `assets/` i stedet for kall til
   `api.qrserver.com` mens du står på scenen.
5. **Thumbnail-stripa** til venstre skrus av via `visThumbnails`, og
   `snarveier.js` legges inn (gir `T`-snarveien).

Til sammen: null eksterne forespørsler ved visning. Verifisert i Chrome —
alle 16 requestene går til egen origin.

QR-generering krever `qrcode`:

```bash
python3 -m pip install qrcode pillow
```

## Lokal forhåndsvisning

```bash
cd .. && python3 -m http.server 8788   # → http://localhost:8788/slides/
```

Piltaster / PgUp / PgDn / mellomrom navigerer, `R` nullstiller, tall hopper.
`T` viser/skjuler thumbnail-stripa. Slide 14 har en 4-minutters timer du
klikker for å starte.

## Thumbnail-stripa

`T` slår stripa av og på mens du står i decket. Det er en øktbryter —
utgangspunktet ved hver sidelast settes av `visThumbnails` i
`deck-config.js`, som er `false`. Snarveien ligger i `snarveier.js`.

Trykker du `T` av vane rett før du går på: stripa kommer tilbake ved neste
last, så sett heller `visThumbnails` og bygg.

`deck-stage.js` har et `no-rail`-attributt for dette, men det virker ikke
herfra: `x-import` gjør bindestreker om til camelCase, så `no-rail` kommer
fram som `norail` og treffer aldri `hasAttribute('no-rail')`. Vi bruker i
stedet innstillingen `deck-stage.railVisible` i localStorage, som
`_enableRail()` leser ved oppstart. `bygg.py` skriver den ved hver sidelast,
så den er ikke avhengig av hva som ligger igjen i nettleseren.

## Hente kilden på nytt fra Claude Design

Når decket er endret i editoren, hent ned disse og kjør `python3 bygg.py`:

| Fra prosjektet | Hit |
|---|---|
| `DK26 Slides.dc.html` | `src/DK26 Slides.dc.html` |
| `deck-stage.js` | `deck-stage.js` |
| `support.js` | `support.js` |

`deck-config.js` og `snarveier.js` er våre egne og hentes ikke ned.

`bygg.py` stopper med en tydelig feilmelding hvis kilden har endret form slik
at et av de fire inngrepene ikke treffer.

Hvis `support.js` oppgraderes kan React/Babel-versjonene ha endret seg. Da må
`CDN`-tabellen øverst i `bygg.py` og filene i `vendor/` oppdateres — sjekk
`REACT_URL`, `REACT_DOM_URL` og `BABEL_URL` i `support.js`.

## Fonter

`fonts/fonts.css` og `.woff2`-filene er generert fra Google Fonts og Fontshare,
kun `latin` + `latin-ext`. De er ikke håndredigert. For å hente dem på nytt,
se commit-historikken for skriptet, eller last ned på nytt fra:

- `https://fonts.googleapis.com/css2?family=Press+Start+2P&family=IBM+Plex+Mono:wght@400;600&display=swap`
- `https://api.fontshare.com/v2/css?f[]=satoshi@500,700,900&display=swap`

## Merknader

- `assets/bas-logo-hvit.png` er generert lokalt fra `bas-logo-svart.png`
  (samme form, hvit fyll, bevart alfa). Decket bruker den alltid med
  `filter:invert(1)`, så resultatet er identisk med originalen.
- `assets/poster.jpg` og `bas-logo-svart.png` er kopiert fra
  `~/bas/projects/dk26-ws/`.
- Print-materiellet (A4-arket og A5-kortene) ligger i samme Claude
  Design-prosjekt under `print/`, og er ikke en del av denne mappa.
