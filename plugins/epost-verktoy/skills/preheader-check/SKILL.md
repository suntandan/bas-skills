---
name: preheader-check
description: Analyser emnelinje + preheader + «over folden»-innhold for et e-postutkast: lengdegrenser per klient, avkuttingssimulering, samspill emne/preheader og alternative varianter. Trigger på fraser som "sjekk emnelinjen", "preheader-sjekk", "er emnelinjen for lang", "hvordan ser dette ut i innboksen", "avkutting", "emne og preheader", "subject line check", "forhåndsvisningstekst", "over folden", "foreslå emnelinjer".
version: 1.0.0
---

# Emnelinje- og preheader-sjekk

## Formål

Vurdere hvordan emnelinje + preheader + første synlige innhold fremstår i innbokslisten på tvers av klienter og flater — **før utsendelse**. Skillen krever ingen verktøy eller subagenter og fungerer i Claude-appen så vel som i Claude Code.

**Input**: Emnelinje og preheader (og gjerne e-post-HTML eller første del av innholdet). Mangler noe: spør. Hvis HTML er delt, hent preheaderen derfra (typisk en skjult div øverst i `<body>`) og sjekk hva som faktisk er første synlige tekst.

---

## 1. Lengdegrenser per klient

Bruk disse som arbeidsverdier (omtrentlige — varierer med skjermbredde, fontstørrelse og faktiske tegn; tegn ≠ piksler, så «WWW» tar mer plass enn «iii»):

### Emnelinje (synlige tegn før avkutting)

| Klient / flate | Ca. grense |
|---|---|
| Gmail desktop | ~70 tegn |
| Gmail mobil | ~35–40 tegn |
| Apple Mail / iOS Mail | ~40–60 tegn (mobil i nedre del) |
| Outlook desktop | ~55–60 tegn |
| Outlook mobil | ~35–40 tegn |

**Tommelfingerregel:** Hovedbudskapet må stå i de **første ~35 tegnene** — det er alt du er garantert på mobil, og over halvparten av åpningene skjer der.

### Preheader / forhåndsvisningstekst

| Klient / flate | Ca. synlig |
|---|---|
| Gmail desktop | ~90–110 tegn (emne + preheader deler én linje) |
| Gmail mobil | ~40–90 tegn (1–2 linjer) |
| iOS Mail | ~2 linjer (~90 tegn) — **merk: Apple Intelligence kan erstatte preheaderen med et AI-sammendrag** |
| Outlook | ~35–75 tegn |

Merk også: hvis preheaderen er kortere enn plassen, fyller klienter på med neste synlige tekst i e-posten — ofte «Vises ikke riktig? Se i nettleser», menylenker eller alt-tekster.

## 2. Avkuttingssimulering

Vis emne og preheader avkuttet ved relevante grenser, slik at brukeren SER hva som overlever:

```
Emne (35 tegn / mobil):   "Nå kan du booke sommerens akti…"
Emne (60 tegn / desktop): "Nå kan du booke sommerens aktiviteter — medlemmer f…"
Preheader (40 tegn):      "Frist 15. juni. Se hele programmet og m…"
Preheader (90 tegn):      "Frist 15. juni. Se hele programmet og meld deg på i dag — plassene fylle…"
```

Tell tegn nøyaktig (inkludert mellomrom). Flagg hvis hovedpoenget eller CTA-en havner etter kuttet. Flagg emoji-bruk (tar visuell plass, kan falle bort eller vises ulikt per klient) og ALL CAPS/overdreven tegnsetting (spam-signal).

## 3. Preheader: bevisst satt eller lekkasje?

Sjekk om preheaderen faktisk er **bevisst**:

- **Lekkasje-symptomer**: «Vises ikke riktig? Klikk her», «Se i nettleser», «Unsubscribe», menypunkter, alt-tekst fra logo — dette betyr at ingen preheader er satt, og klienten viser første tilgjengelige tekst.
- **Fiks**: Legg en skjult preheader-div først i `<body>`:
  ```html
  <div style="display:none;max-height:0;overflow:hidden;mso-hide:all;">
    Preheader text here&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
  </div>
  ```
  `&nbsp;&zwnj;`-repetisjonen («padding») hindrer at etterfølgende innhold lekker inn etter preheaderen.
- Sjekk også at «Se i nettleser»-lenken o.l. ligger **etter** preheader-diven i HTML-en.

## 4. Samspill emne + preheader

De to leses som én enhet i innbokslisten. Vurder:

- **Fortsetter preheaderen emnet**, eller gjentar den det? Gjentakelse er bortkastet plass.
- **Komplementær-mønsteret**: Emne = krok/hovedbudskap, preheader = utdyping, konkretisering eller CTA.
- **Frontlasting**: Står det viktigste først i begge, slik at avkutting rammer minst mulig?
- **Ærlighet**: Lover emnet noe innholdet ikke leverer? (Skader tillit og fremtidig åpningsrate.)
- **AI-innboks-robusthet**: På iOS kan preheaderen erstattes av et AI-sammendrag av selve e-posten — emnet må derfor kunne stå alene, og hovedbudskapet må også finnes i e-postens tekst. (For full simulering: bruk skillen `inbox-summary`.)

## 5. «Over folden»

Hvis HTML/innhold er delt: vurder hva som er synlig i første skjermbilde (mobil, ~600 px høyde) etter åpning:

- Er hovedbudskapet synlig som **tekst** (ikke kun i bilde — bilder kan være blokkert)?
- Er første CTA synlig eller rett under folden?
- Henger emne → preheader → første overskrift sammen som én fortelling?

## 6. Foreslå 3 alternative varianter

Lever alltid tre alternative emne+preheader-par med ulik vinkling, f.eks.:

1. **Konkret/faktabasert** — tall, frist eller tilbud først
2. **Nytteorientert** — hva mottakeren får/oppnår
3. **Nysgjerrighet/relasjon** — men aldri clickbait som innholdet ikke innfrir

For hver variant: oppgi tegnlengde på emne og preheader, og vis 35-tegns mobilavkutting av emnet.

---

## Outputformat

```
## Innboks-sjekk

**Slik ser det ut:**
[avkuttingssimulering per flate]

## Funn
- Emnelengde: [X tegn — vurdering]
- Preheader: [bevisst/lekkasje — vurdering]
- Samspill: [vurdering]
- Over folden: [vurdering, hvis innhold delt]

## 3 alternative varianter
1. Emne (XX tegn): "..." / Preheader (XX tegn): "..."
   Mobil-kutt: "..."
2. ...
3. ...

## Anbefaling
[hvilken variant og hvorfor — eller behold original med disse justeringene]
```

Vær konkret og tell tegn nøyaktig. Alle grenser er omtrentlige — si det, men ikke gjem anbefalingen bak forbehold.
