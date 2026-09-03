---
name: inbox-summary
description: Simuler hvordan AI-innbokser (Gmail Gemini-sammendrag, Apple Intelligence) vil oppsummere et e-postutkast FØR utsendelse — og vurder om hovedbudskap og CTA overlever. Trigger på fraser som "hvordan vil AI oppsummere denne e-posten", "inbox summary", "Gemini-sammendrag", "Apple Intelligence-sammendrag", "hva ser mottakeren i innboksen", "overlever budskapet AI-sammendraget", "simuler innboks", "AI-innboks", "test e-posten mot AI-sammendrag".
version: 1.0.0
---

# AI-innboks-simulering

## Formål

Stadig flere mottakere ser først et **AI-generert sammendrag** av e-posten din — ikke e-posten selv. Apple Intelligence viser én sammendragslinje i innbokslisten (i stedet for preheader), og Gmail/Gemini tilbyr sammendrag av e-poster. Denne skillen simulerer disse sammendragene for et utkast **før utsendelse**, slik at du kan justere e-posten mens det fortsatt er gratis.

**Input**: E-post-HTML eller ren tekst (lim inn utkastet). Be om emnelinje og preheader hvis de ikke følger med — de påvirker vurderingen.

Skillen krever ingen verktøy eller subagenter — den fungerer i Claude-appen så vel som i Claude Code.

---

## Kjerneprinsipp: Vær nøktern, ikke optimistisk

Sammendragene skal lages **lojalt mot hvordan disse systemene faktisk oppfører seg** — ikke slik avsenderen skulle ønske. Det betyr:

- **Korte og faktabaserte.** Apple Intelligence: én linje, typisk 10–20 ord. Gmail: noen få punkter eller 1–3 korte setninger.
- **Ignorerer markedsspråk.** «Fantastiske nyheter!», «Ikke gå glipp av!», utropstegn og superlativer forsvinner. Bare konkret innhold overlever: hva, hvem, når, hvor mye, frist.
- **Ignorerer bilder totalt.** Budskap som kun finnes i bilder (hero-bilde med tekst, GIF med tilbudet) er usynlig for sammendraget.
- **Nøytral, nesten tørr tone.** Sammendraget «selger» ikke. «20 % rabatt på abonnement frem til søndag» — ikke «Utrolig tilbud venter!»
- **Prioriterer det konkrete og tidlige.** Innhold tidlig i e-posten og konkrete fakta (datoer, beløp, frister, handlinger) vektes tyngst. Vage avsnitt bidrar lite.
- **Kan bomme.** Hvis e-posten har flere konkurrerende budskap, kan sammendraget plukke feil. Det er nettopp det denne simuleringen skal avsløre.

Hvis e-posten er tynn på konkret innhold, skal det simulerte sammendraget reflektere det («Nyhetsbrev med produktnyheter og tilbud») — ikke diktes bedre enn det er.

---

## Fremgangsmåte

### 1. Ekstraher tekstinnholdet

Fra HTML: les kun synlig tekst i DOM-rekkefølge (inkludert alt-tekster — men merk deg hvilke budskap som KUN finnes i bilder). Fra ren tekst: bruk som den er. Noter emnelinje og preheader separat.

### 2. Lag simulert Apple Intelligence-sammendrag

Én linje, maks ~120 tegn, faktabasert, nøytral tone, ingen utropstegn. Dette er linjen som **erstatter preheaderen** i innbokslisten på iPhone.

### 3. Lag simulert Gmail/Gemini-sammendrag

Litt lengre: 1–3 korte setninger eller 2–4 kulepunkter. Fanger hovedinnhold + eventuelle konkrete detaljer (frister, beløp, handlinger). Fortsatt nøytralt og komprimert.

### 4. Vurder: overlever budskapet?

Svar eksplisitt på:

- **Kommer hovedbudskapet gjennom?** Er det avsenderen VIL si det samme som sammendraget faktisk sier?
- **Kommer CTA-en gjennom?** Vet mottakeren hva de skal gjøre, ut fra sammendraget alene?
- **Hva forsvinner?** List konkret: budskap som kun finnes i bilder, poeng begravd langt ned, markedsspråk som strippes, sekundærbudskap som stjeler plass.
- **Feiltolkningsrisiko:** Kan sammendraget fremheve feil ting (f.eks. en juridisk fotnote, et sekundærtilbud, avmeldingsinfo)?

### 5. Konkrete forslag til forbedring

Foreslå endringer som gjør sammendraget bedre — typisk:

- **Første avsnitt**: Legg hovedbudskap + CTA i konkret klartekst i første tekstavsnitt (ikke bare i bilde/knapp).
- **Preheader**: Skriv den som en faktasetning som kan stå alene — AI-systemer og eldre klienter bruker begge tidlig tekst.
- **Struktur**: Ett hovedbudskap per e-post; flytt sekundærinnhold ned eller ut. Konkrete fakta (dato, beløp, frist) i løpende tekst, ikke kun i grafikk.
- **Alt-tekster**: Gi innholdsbilder alt-tekst som bærer budskapet.
- **CTA i tekst**: Lenketekst som beskriver handlingen («Bestill gratis befaring») — den kan overleve inn i sammendraget; «Klikk her» gjør det ikke.

Vis gjerne «før → etter»: det simulerte sammendraget slik det blir nå, og slik det ville blitt etter foreslåtte endringer.

---

## Outputformat

```
## Simulert AI-innboks

**Apple Intelligence (1 linje):**
> [simulert sammendrag]

**Gmail / Gemini:**
> [simulert sammendrag]

## Vurdering
- Hovedbudskap gjennom: [ja / delvis / nei — hvorfor]
- CTA gjennom: [ja / delvis / nei — hvorfor]
- Dette forsvinner: [liste]
- Feiltolkningsrisiko: [liste eller «lav»]

## Anbefalte endringer
1. [konkret endring — hva og hvor]
2. ...

## Etter endringene (estimert)
> [nytt simulert Apple Intelligence-sammendrag]
```

---

## Viktige forbehold (nevn kort i svaret)

- Dette er en **simulering** basert på kjent oppførsel — de faktiske systemene endres løpende og er ikke offentlig dokumentert i detalj.
- Apple Intelligence sammendrar per e-post/tråd på enheten; nøyaktig ordlyd vil variere.
- Prinsippet holder likevel: **konkret, tidlig, tekstbasert innhold overlever — markedsspråk og bilder gjør det ikke.**
