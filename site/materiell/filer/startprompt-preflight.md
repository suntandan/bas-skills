# Startprompt: bygg din egen e-post-preflight

Lim inn i Claude Code (eller tilsvarende) i en tom mappe. Bytt ut det som
står i «⟨⟩». Prompten er et utgangspunkt — den viktigste jobben er de fire
avklaringene nederst, gjør dem før du lar agenten skrive kode.

---

## Prompt

Vi skal bygge et internt verktøy som sjekker markedsførings-e-poster før
utsendelse. Målgruppen er markedsførere, ikke utviklere.

**Flyt**: brukeren sender en testutsendelse fra sitt eget e-postverktøy til
`<prosjekt>@⟨domene⟩`. En inbound-webhook tar imot e-posten, en
valideringsmotor analyserer HTML-en, og en rapportside viser funnene ved
siden av en forhåndsvisning. Klikk på et funn → elementet spotlightes i
forhåndsvisningen. Auto-svar på e-post med lenke til rapporten.

**Stack**: ⟨Next.js App Router + Postgres (Drizzle) + Vercel⟩,
inbound/outbound e-post via ⟨Postmark⟩, innlogging via ⟨Clerk⟩.

### Ufravikelige designprinsipper

1. **Motoren er ren.** `analyzeEmail(input) → findings` har ingen DB-kall og
   ingen sideeffekter. Alt I/O ligger utenfor. Da kan hele katalogen testes
   med vanlige unit-tester uten database.
2. **Regler er plugins.** Hver sjekk er én fil som eksporterer en regel med
   id, alvorsgrad og en `run(ctx)`. To faser: `static` (ren HTML/CSS) og
   `resource` (trenger nettverk — bilder, lenker; SSRF-sikret fetch med
   timeout og størrelsesgrense).
3. **Lokatorkontrakten.** Et funn peker på et element som `{sel, idx}` =
   `querySelectorAll(sel)[idx]`. Dette fungerer KUN hvis forhåndsvisningen
   rendrer nøyaktig samme prosesserte HTML som motoren analyserte. Aldri la
   preview og analyse se ulik HTML — det er den enkeltbeslutningen som gjør
   «klikk funn → se element» mulig.
4. **Tre lag sikkerhet mot upålitelig e-post-HTML**: (a) sanitering som
   fjerner `script`/`on*`/`base`/meta-refresh, (b) preview i iframe med
   `sandbox="allow-same-origin"` — aldri `allow-scripts`, (c) CSP +
   `noindex` + `no-referrer` på HTML-routen.
5. **Trafikklys, ingen score.** `error` (stopper utsendelse) / `warn`
   («sjekk dette») / `info`. Et tall fra 0–100 inviterer til å optimalisere
   tallet i stedet for e-posten.
6. **Funn-tekster skrives for målgruppen.** Forklar hvorfor det er et
   problem og hva man gjør, ikke bare hva som er galt. Heuristiske sjekker
   sier «bør sjekkes», aldri skråsikkert — falske positiver koster tillit
   raskere enn manglende funn koster nytte.

### Valideringskatalog — start her

MVP: `structure` (tabell-layout, bredde, DOCTYPE), `images` (alt-tekst,
filstørrelse, bilde-kun-e-post), `links` (døde lenker, `javascript:`,
tomme href), `unsubscribe` (avmeldingslenke finnes), `headers` (emne,
preheader, avsender), `plaintext` (tekstversjon finnes og samsvarer).

Senere: `darkmode`, `utm`, `dates` (utdaterte datoer/årstall),
`spelling`, `css` (ustøttede properties), `resources` (statuskoder,
total vekt), `ai`/`schema` (hva en oppsummerings-AI faktisk ser).

### Fremgangsmåte

Foreslå en faseplan før du koder. Fase 1 = motoren + tester mot ekte
e-post-fixtures, helt uten DB og UI. Fase 2 = inbound-webhook og lagring.
Fase 3 = rapportsiden med preview og spotlight. Ikke start på fase 2 før
katalogen gir riktige svar på minst ti ekte e-poster.

---

## Avklar før du starter

- **Domene**: hvilken adresse sender folk til? MX må peke på
  e-postleverandøren. Dette tar lengst tid organisatorisk — start her.
- **Hvem har tilgang**: intern innlogging + en delingslenke-mekanisme for
  kunder som ikke skal ha konto.
- **Korpus**: samle 20–30 ekte utsendelser først. Terskler (bildevekt,
  tekstmengde) skal kalibreres mot dem, ikke gjettes.
- **ESP-artefakter**: tracking-wrappere fra Dynamics/Agillic/o.l. ser ut som
  encoding-feil. Gjenkjenn plattformen og demp disse funnene per URL, ellers
  drukner rapporten i støy fra første dag.
