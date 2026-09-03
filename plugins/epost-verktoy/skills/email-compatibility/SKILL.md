---
name: email-compatibility
description: Sjekk e-post-HTML for kompatibilitetsproblemer på tvers av e-postklienter (Outlook, Gmail, Apple Mail m.fl.) og tilgjengelighet. Trigger på fraser som "sjekk denne e-posten", "hvorfor ser dette rart ut i Outlook", "kompatibilitetssjekk", "vil dette fungere i Gmail", "e-posten ser feil ut", "cross-client", "render-problemer", "outlook-bug", "sjekk HTML-en for klientproblemer", "tilgjengelighet i e-post".
version: 1.0.0
---

# E-postklient-kompatibilitet

## Formål

Analysere e-post-HTML for kjente klientproblemer og foreslå konkrete fikser. To hovedmoduser:

1. **Full sjekk**: «Sjekk denne e-post-HTML-en for klientproblemer» — gå systematisk gjennom sjekklisten under og rapporter funn med alvorlighetsgrad og fiks.
2. **Diagnose**: «Hvorfor ser dette rart ut i Outlook?» — bruk kunnskapen under til å identifisere den mest sannsynlige årsaken, og foreslå fiks.

Rapportér alltid: **hva** som er problemet, **hvilke klienter** det rammer, og **konkret fiks** (kodeeksempel).

---

## Outlook for Windows (Word-renderingsmotor)

Outlook 2007–2021 og Microsoft 365 for Windows bruker Words HTML-motor — den største kilden til render-problemer.

- **Ignorerer `max-width`** — bruk «ghost tables» for fast bredde:
  ```html
  <!--[if true]><table role="presentation" style="width:640px" align="center"><tr><td><![endif]-->
    <!-- responsive content with max-width -->
  <!--[if true]></td></tr></table><![endif]-->
  ```
- **Knapper/CTA-er**: To etablerte teknikker:
  - **MSO padding-hack** (anbefalt, enklest å vedlikeholde): `mso-font-width` + `mso-text-raise` på skjulte `<i>`-elementer inni lenken — gir klikkbar flate uten VML.
  - **VML** (klassisk «bulletproof button», f.eks. fra buttons.cm): `<v:roundrect>` i en `<!--[if mso]>`-blokk. Fungerer, men VML-knapper er tyngre å vedlikeholde og lenken i VML-laget må holdes i sync med HTML-lenken. VML trengs fortsatt for **bakgrunnsbilder** i Outlook (`<v:rect>` + `<v:fill>`).
- **Ingen støtte for**: CSS `float` (bruk `align`-attributt), `margin` (upålitelig), bakgrunnsbilder uten VML, border-radius, animert GIF (viser kun første frame — sørg for at frame 1 fungerer som statisk bilde).
- **Egendefinerte fonter**: Outlook faller tilbake til Times New Roman hvis font-stacken feiler. Legg inn fallback via `<!--[if mso]><style>`-blokk med `mso-generic-font-family` / `mso-font-alt`, og alltid websikker fallback i font-stacken.
- **120 DPI-skalering**: Enkelte Outlook-oppsett skalerer til 120 DPI — ikke stol på pikselperfekt justering; bruk prosenter inni tabeller der mulig.
- **Skjule innhold for Outlook**: `<!--[if !mso]><!--> ... <!--<![endif]-->`. Vise kun i Outlook: `<!--[if mso]> ... <![endif]-->`.

## Outlook for Mac (Microsoft 365 / «OLK»)

Egen motor (WebKit-basert) — ikke det samme som Outlook Windows.

- **Align-buggen**: OLK **stripper `align`-attributter på `<table>`** — en tabell med `align="right"` blir en full bredde-blokk i stedet for å flyte til høyre. Fiks: bruk **begge** mekanismene samtidig:
  ```html
  <table align="right" role="presentation" style="border-spacing: 0; float: right;">
  ```
  `align="right"` dekker Outlook Windows (som ignorerer CSS float); `float: right` i `style` dekker OLK (som ignorerer `align`).

## Gmail

- **Stripper `<style>`-blokker i noen kontekster** (ikke-Google Workspace, videresendte/embedded visninger) — alle kritiske stiler **må være inlinet**.
- **Skriver om CSS-klassenavn** — bruk aldri klassenavn til layout; kun til hover-states og media queries.
- **Ingen `@font-face`** — egendefinerte fonter strippes; alltid websikker fallback i font-stacken.
- **`<style>` kun i `<head>`** — `<style>` i `<body>` fjernes.
- **Klipper e-poster over ~102 KB** («[Message clipped]») — hold HTML-størrelsen under dette.

## Apple Mail / iOS Mail

Den snilleste motoren (WebKit, god CSS-støtte), men:

- **Auto-linking**: Datoer, adresser og telefonnumre gjøres om til blå lenker. Fiks: `<meta name="format-detection" content="telephone=no,date=no,address=no,email=no,url=no">`
- **Reformattering**: Legg til `<meta name="x-apple-disable-message-reformatting">`.
- **Dark mode**: Apple Mail støtter `prefers-color-scheme` og kan selv invertere farger. Ta et bevisst valg: enten full dark mode-støtte (`color-scheme: light dark` + `@media (prefers-color-scheme: dark)` + `[data-ogsc]`-overrides for Outlook-appen), eller bevisst light-only. Halvveis støtte gir de styggeste resultatene.

## Generelle regler (alle klienter)

- `display:block` på hvert `<img>` — hindrer fantom-mellomrom under bilder.
- Spacing med `padding` på `<td>`, aldri `margin` — margin er upålitelig på tvers av klienter.
- `role="presentation"` på alle layout-tabeller.
- Font-stacker slutter alltid på websikker fallback (`'Custom Font', Arial, sans-serif`).
- **Ingen** JavaScript, flexbox, CSS Grid eller CSS custom properties (`var()`) i layout.
- `width` og `border="0"` på alle `<img>`; `cellpadding="0" cellspacing="0" border="0"` på alle layout-tabeller.

---

## Klient-targeting i CSS (avansert)

Til å vise/skjule innhold per klient — mest brukt for interaktive teknikker med statisk fallback:

| Klient | Selektor | Mekanisme |
|---|---|---|
| WebKit-klienter (Apple Mail, iOS, Outlook Mac) | `@media screen and (-webkit-min-device-pixel-ratio: 0)` | Media query kun WebKit matcher |
| Gmail | `u + .body .klasse` | Gmail wrapper innholdet med en `<u>` før `.body` |
| Outlook.com / M365 web (ny) + Outlook-apper | `[owa] .klasse` | `owa`-attributt på `<html>` |
| Outlook.com (gammel) | `#converted-body .klasse` | Wrapper-div |
| Outlook på iOS | `[class~="x_klasse"]` | Skriver om klassenavn med `x_`-prefiks |
| Samsung Mail | `#MessageViewBody .klasse` | Wrapper-id |
| Comcast / Zimbra | `body.MsgBody .klasse` | Klasse på `<body>` |
| Outlook Windows | `<!--[if mso]>` / `<!--[if !mso]><!-->` | Conditional comments (HTML, ikke CSS) |

Referanser: [howtotarget.email](https://howtotarget.email) (klientselektorer), [caniemail.com](https://www.caniemail.com) (CSS-støtte per klient), [goodemailcode.com](https://www.goodemailcode.com) (velprøvde mønstre).

---

## Tilgjengelighet (sjekkes alltid i full sjekk)

- `role="article"` med `aria-roledescription="email"` på ytterste innholdswrapper, og `aria-label="E-post fra [avsendernavn]"`.
- `lang` og `dir` på `<html>` (f.eks. `lang="no" dir="ltr"`), `xml:lang` på `<body>` for Outlook Windows.
- **Alt-tekst** på hvert `<img>` — beskrivende for innholdsbilder, `alt=""` for dekorative.
- **Overskriftshierarki** — `<h1>`–`<h3>` i logisk rekkefølge, ikke hopp over nivåer.
- `font-size: max(16px, 1rem)` på `role="article"`-wrapperen — tekst skalerer med brukerens innstillinger.
- `user-scalable=yes` i viewport-meta — aldri hindre zooming.
- **Beskrivende lenketekst** — aldri «Klikk her» eller «Les mer» alene.
- **Fargekontrast** — WCAG AA-minimum: 4,5:1 for normal tekst, 3:1 for stor tekst.

---

## Rapportformat (full sjekk)

```
## Kompatibilitetsrapport

### Kritisk (vil se ødelagt ut)
- [problem] — rammer [klienter] — fiks: [konkret endring med kodeeksempel]

### Bør fikses (degradert opplevelse)
- ...

### Tilgjengelighet
- ...

### OK
- [ting som allerede er riktig gjort — kort]
```

Vær konkret: pek på linje/element i HTML-en brukeren delte, ikke bare generelle råd.
