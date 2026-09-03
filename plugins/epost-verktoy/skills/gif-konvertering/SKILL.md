---
name: gif-konvertering
description: Konverter en videofil eller bildesekvens til animert GIF og/eller WebP for bruk i e-post. Trigger på fraser som "lag en gif", "konverter til gif", "gif av denne videoen", "animert webp", "gif til nyhetsbrev", "slideshow-gif av disse bildene", "gjør videoen om til gif", "gif-konvertering". Krever ffmpeg (Claude Code / lokalt miljø).
version: 1.0.0
---

# GIF-konvertering for e-post

## Steg 0 — Sjekk at ffmpeg er tilgjengelig

Kjør først `ffmpeg -version` og `ffprobe -version`. Hvis en av dem mangler, **ikke fortsett** — forklar brukeren hvordan de installeres:

- **macOS**: `brew install ffmpeg` (krever [Homebrew](https://brew.sh))
- **Windows**: `winget install ffmpeg` (eller last ned fra [ffmpeg.org](https://ffmpeg.org/download.html))
- **Linux**: `sudo apt install ffmpeg` (Debian/Ubuntu) eller tilsvarende for din distro

Be brukeren installere og prøve igjen. Ikke forsøk alternative verktøy.

---

Konverter en videofil eller bildesekvens til animert GIF og/eller WebP for bruk i e-post.

Støttede inputformater (video): MP4, MOV, MKV, WebM, AVI, FLV og de fleste andre formater ffmpeg støtter.
Støttede inputformater (bilder): JPG, PNG, WebP og de fleste andre bildeformater ffmpeg støtter.

---

## Workflow A — Video til GIF/WebP

1. **Finn videofilen** i gjeldende mappe. Spør brukeren hvis det er flere å velge mellom.
2. **Sjekk videoegenskapene** med ffprobe (bredde, høyde, FPS, varighet, filstørrelse).
3. **Spør om justeringer** hvis ikke spesifisert:
   - Størrelse/skalering (standard: original bredde)
   - FPS (standard: 15)
   - Loop (standard: ja / uendelig)
   - Trimming (standard: ingen — men spør hvis videoen er lang)
   - Format (standard: GIF — spør **ikke** om WebP med mindre brukeren nevner det)
4. Generer palette og konverter.
5. **Rapporter resultatet**: filnavn, filstørrelse og innstillinger brukt.

---

## Workflow B — Bildesekvens til GIF/WebP

1. **Finn bilder** i gjeldende mappe. Vis liste og bekreft rekkefølge med brukeren.
2. **Sjekk bildedimensjoner** med ffprobe — advar hvis bildene har forskjellig størrelse (kreves lik størrelse for transitions).
3. **Spør om justeringer**:
   - Størrelse/skalering (standard: original bredde)
   - Varighet per bilde i sekunder (standard: 2s)
   - FPS (standard: 10 — høyere er unødvendig for slideshow)
   - Transition-type (standard: ingen — se liste nedenfor)
   - Transition-varighet i sekunder (standard: 0.5s)
   - Loop-overgang: fade/slide tilbake til første bilde på slutten? (standard: ja hvis transition er valgt)
   - Format: GIF, WebP, eller begge? (standard: spør — se note om filstørrelse nedenfor)
4. Generer output.
5. **Rapporter resultatet**: filnavn(er), filstørrelse(r) og innstillinger brukt.

> **Note filstørrelse:** GIF med transitions (fade/slide) på fotorealistiske bilder blir typisk svært store (2–3 MB+) pga. 256-fargegrensen. For slike tilfeller anbefal WebP + GIF-fallback via `<picture>`-elementet, der GIF-fallbacken kan være et enkelt slideshow uten transition (`none`). La brukeren bestemme.

---

## ffmpeg-kommandoer — Video

### GIF – Steg 1: Generer palette
```bash
ffmpeg -ss [START] -t [VARIGHET] -i [INPUT] \
  -vf "fps=[FPS],scale=[BREDDE]:-1:flags=lanczos,palettegen=max_colors=256:stats_mode=diff" \
  -frames:v 1 -update 1 \
  -y ./palette.png
```
- Utelat `-ss` og `-t` hvis ingen trimming.
- `scale=[BREDDE]:-1` bevarer proporsjonene. Bruk `scale=-1:-1` for uendret størrelse.

### GIF – Steg 2: Konverter til GIF
```bash
ffmpeg -ss [START] -t [VARIGHET] -i [INPUT] \
  -i ./palette.png \
  -lavfi "fps=[FPS],scale=[BREDDE]:-1:flags=lanczos [x]; [x][1:v] paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle" \
  -loop [LOOP] \
  -y [OUTPUT.gif]
```
- `-loop 0` = uendelig loop, `-loop 1` = spilles én gang.
- Utelat `-ss` og `-t` hvis ingen trimming.

### WebP – Konverter til animert WebP (ett steg)
```bash
ffmpeg -ss [START] -t [VARIGHET] -i [INPUT] \
  -vf "fps=[FPS],scale=[BREDDE]:-1:flags=lanczos" \
  -loop [LOOP] \
  -lossless 0 -compression_level 6 -quality 80 \
  -y [OUTPUT.webp]
```
- `-loop 0` = uendelig loop, `-loop 1` = spilles én gang.
- Utelat `-ss` og `-t` hvis ingen trimming.

---

## ffmpeg-kommandoer — Bildesekvens

### Uten transition (enkelt slideshow)

**GIF – Steg 1: Palette**
```bash
ffmpeg \
  -loop 1 -t [VARIGHET] -i bilde1.jpg \
  -loop 1 -t [VARIGHET] -i bilde2.jpg \
  -loop 1 -t [VARIGHET] -i bilde3.jpg \
  -filter_complex "[0:v][1:v][2:v]concat=n=3:v=1:a=0,fps=[FPS],scale=[BREDDE]:-1:flags=lanczos,palettegen=max_colors=256:stats_mode=diff" \
  -frames:v 1 -update 1 -y ./palette.png
```

**GIF – Steg 2: Konverter**
```bash
ffmpeg \
  -loop 1 -t [VARIGHET] -i bilde1.jpg \
  -loop 1 -t [VARIGHET] -i bilde2.jpg \
  -loop 1 -t [VARIGHET] -i bilde3.jpg \
  -i ./palette.png \
  -filter_complex "[0:v][1:v][2:v]concat=n=3:v=1:a=0,fps=[FPS],scale=[BREDDE]:-1:flags=lanczos[x];[x][3:v]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle" \
  -loop 0 -y [OUTPUT.gif]
```

**WebP (ett steg)**
```bash
ffmpeg \
  -loop 1 -t [VARIGHET] -i bilde1.jpg \
  -loop 1 -t [VARIGHET] -i bilde2.jpg \
  -loop 1 -t [VARIGHET] -i bilde3.jpg \
  -filter_complex "[0:v][1:v][2:v]concat=n=3:v=1:a=0,fps=[FPS],scale=[BREDDE]:-1:flags=lanczos[vout]" \
  -map "[vout]" \
  -loop 0 -lossless 0 -compression_level 6 -quality 80 \
  -y [OUTPUT.webp]
```

---

### Med transition (xfade)

Offset-formel for N bilder med varighet D og transition-tid T:
- `offset_i = i * (D - T)` der i starter på 1
- Eks. 3 bilder, D=2s, T=0.5s: offset 1=1.5, offset 2=3.0, offset 3=4.5 (loop-tilbake)
- For loop-overgang: legg til første bilde som siste input og en ekstra xfade.

**GIF – Steg 1: Palette**
```bash
ffmpeg \
  -loop 1 -t [D] -i bilde1.jpg \
  -loop 1 -t [D] -i bilde2.jpg \
  -loop 1 -t [D] -i bilde3.jpg \
  -loop 1 -t [D] -i bilde1.jpg \
  -filter_complex "
    [0:v]scale=[BREDDE]:-1:flags=lanczos,fps=[FPS][v0];
    [1:v]scale=[BREDDE]:-1:flags=lanczos,fps=[FPS][v1];
    [2:v]scale=[BREDDE]:-1:flags=lanczos,fps=[FPS][v2];
    [3:v]scale=[BREDDE]:-1:flags=lanczos,fps=[FPS][v3];
    [v0][v1]xfade=transition=[TRANSITION]:duration=[T]:offset=[offset1][v01];
    [v01][v2]xfade=transition=[TRANSITION]:duration=[T]:offset=[offset2][v012];
    [v012][v3]xfade=transition=[TRANSITION]:duration=[T]:offset=[offset3][vout];
    [vout]palettegen=max_colors=256:stats_mode=diff
  " \
  -frames:v 1 -update 1 -y ./palette.png
```

**GIF – Steg 2: Konverter**
```bash
ffmpeg \
  -loop 1 -t [D] -i bilde1.jpg \
  -loop 1 -t [D] -i bilde2.jpg \
  -loop 1 -t [D] -i bilde3.jpg \
  -loop 1 -t [D] -i bilde1.jpg \
  -i ./palette.png \
  -filter_complex "
    [0:v]scale=[BREDDE]:-1:flags=lanczos,fps=[FPS][v0];
    [1:v]scale=[BREDDE]:-1:flags=lanczos,fps=[FPS][v1];
    [2:v]scale=[BREDDE]:-1:flags=lanczos,fps=[FPS][v2];
    [3:v]scale=[BREDDE]:-1:flags=lanczos,fps=[FPS][v3];
    [v0][v1]xfade=transition=[TRANSITION]:duration=[T]:offset=[offset1][v01];
    [v01][v2]xfade=transition=[TRANSITION]:duration=[T]:offset=[offset2][v012];
    [v012][v3]xfade=transition=[TRANSITION]:duration=[T]:offset=[offset3][vout];
    [vout][4:v]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle
  " \
  -loop 0 -y [OUTPUT.gif]
```

**WebP – ett steg**
```bash
ffmpeg \
  -loop 1 -t [D] -i bilde1.jpg \
  -loop 1 -t [D] -i bilde2.jpg \
  -loop 1 -t [D] -i bilde3.jpg \
  -loop 1 -t [D] -i bilde1.jpg \
  -filter_complex "
    [0:v]scale=[BREDDE]:-1:flags=lanczos,fps=[FPS][v0];
    [1:v]scale=[BREDDE]:-1:flags=lanczos,fps=[FPS][v1];
    [2:v]scale=[BREDDE]:-1:flags=lanczos,fps=[FPS][v2];
    [3:v]scale=[BREDDE]:-1:flags=lanczos,fps=[FPS][v3];
    [v0][v1]xfade=transition=[TRANSITION]:duration=[T]:offset=[offset1][v01];
    [v01][v2]xfade=transition=[TRANSITION]:duration=[T]:offset=[offset2][v012];
    [v012][v3]xfade=transition=[TRANSITION]:duration=[T]:offset=[offset3][vout]
  " \
  -map "[vout]" \
  -loop 0 -lossless 0 -compression_level 6 -quality 80 \
  -y [OUTPUT.webp]
```

> **Viktig:** Tilpass antall inputs, concat `n=`, xfade-kjeder og palette-input-indeks etter faktisk antall bilder.

---

## Tilgjengelige transitions (xfade)

| Transition | Beskrivelse |
|---|---|
| `fade` | Crossfade — myk overgang |
| `slideleft` | Ny glir inn fra høyre, gammel ut til venstre |
| `slideright` | Ny glir inn fra venstre |
| `slideup` | Ny glir inn nedenfra |
| `slidedown` | Ny glir inn ovenfra |
| `wipeleft` | Tørrende overgang til venstre |
| `wiperight` | Tørrende overgang til høyre |
| `dissolve` | Tilfeldig piksel-dissolve |
| `fadeblack` | Fade via svart |
| `fadewhite` | Fade via hvitt |
| `radial` | Klokkevis roterende overgang |
| `circleopen` | Sirkel åpner seg |
| `circleclose` | Sirkel lukker seg |

---

## Standardverdier

| Parameter | Video | Bildesekvens |
|---|---|---|
| FPS | 15 | 10 |
| Bredde | Original | Original |
| Loop | 0 (uendelig) | 0 (uendelig) |
| Varighet per bilde | — | 2s |
| Transition | — | ingen |
| Transition-tid | — | 0.5s |
| Loop-overgang | — | ja (hvis transition valgt) |
| Format | GIF | spør brukeren |

---

## Inputformat (video)

| Format | Egnethet | Kommentar |
|--------|----------|-----------|
| MOV (ProRes) | Best | Tapsfritt/nær-tapsfritt |
| MP4 (H.264, høy bitrate) | Utmerket | Fungerer svært godt |
| MP4 (H.265/HEVC) | Bra | Litt tregere å prosessere |
| WebM (VP9) | Bra | God kvalitet |
| AVI, MKV, FLV | OK | Fungerer, eldre formater |
| GIF som input | Unngå | Allerede 256 farger |

---

## Tips

- For e-post: hold filen under 1–2 MB. Prøv lavere FPS eller smalere bredde hvis filen blir for stor.
- GIF med fade/slide på foto-innhold kan bli 2–3 MB+. Vurder WebP + enkel GIF-fallback.
- `diff_mode=rectangle` + `bayer`-dithering gir best GIF-komprimering.
- WebP med transitions er ett steg og trenger ikke palette — husk `-map "[vout]"`.

---

## Snippet: `<picture>` med WebP og GIF-fallback

Kilde: [goodemailcode.com](https://www.goodemailcode.com/email-enhancements/picture)

```html
<picture>
  <source srcset="animation.webp" type="image/webp">
  <source srcset="animation.gif" type="image/gif">
  <img src="static.png" alt="Alt Text!" style="">
</picture>
```

- Klienter som støtter WebP (Gmail, Apple Mail) bruker `.webp`.
- Klienter uten WebP-støtte (Outlook desktop) bruker `.gif`.
- `<img>`-taggen er fallback hvis `<picture>` ikke støttes — bruk et statisk bilde.
- Kun det matchende formatet hentes — ingen ekstra båndbredde.

> **Når er WebP verdt det?**
> WebP gir størst gevinst ved fotorealistiske animasjoner, gradienter og fargerike bilder — der GIFs 256-fargegrense gir synlige artefakter. For enkle flatdesign-animasjoner med få farger er gevinsten liten. WebP er typisk 30–70 % mindre enn tilsvarende GIF.

---

## Opprydding

Slett `./palette.png` når konverteringen er ferdig — den er kun et mellomsteg.
