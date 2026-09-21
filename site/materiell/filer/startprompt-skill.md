# Startprompt: bygg en verktøy-skill (som `/gif-konvertering`)

Lim inn i Claude Code. Bytt ut det som står i «⟨⟩». Mønsteret passer for
alle skills som pakker inn et CLI-verktøy i en arbeidsflyt: ffmpeg,
ImageMagick, pandoc, rclone, sharp, exiftool.

---

## Prompt

Lag en skill som lar meg ⟨konvertere video og bildesekvenser til animert
GIF/WebP for e-post⟩ ved hjelp av ⟨ffmpeg⟩.

Legg den i `⟨plugins/epost-verktoy⟩/skills/⟨navn⟩/SKILL.md` med frontmatter
`name`, `description`, `version`.

### Skriv for en agent, ikke for et menneske

En SKILL.md er instruksjoner til en modell som skal utføre jobben — ikke
dokumentasjon noen skal lese. Det gir seks konkrete krav:

1. **`description` er triggerflaten.** Den avgjør om skillen i det hele tatt
   blir plukket opp. List fraser jeg faktisk kommer til å skrive, på norsk,
   inkludert de klønete: «lag en gif», «gjør videoen om til gif», «gif til
   nyhetsbrev». Nevn også harde krav («krever ffmpeg»). Én setning som
   beskriver skillen abstrakt trigger aldri.
2. **Steg 0 er alltid en avhengighetssjekk.** Kjør `⟨ffmpeg -version⟩` først.
   Mangler den: forklar installasjon per OS (macOS/Windows/Linux), stopp,
   og si eksplisitt «ikke forsøk alternative verktøy». Uten den linjen
   improviserer agenten seg til et dårligere resultat i stedet for å si fra.
3. **Kommandoer skal være kopierbare, ikke beskrevet.** Fullstendige
   kommandoer med `[PLACEHOLDER]`-tokens, én kodeblokk per variant, med
   kulepunkter rett under om hvilke flagg som kan utelates. Prosa om hva
   verktøyet «kan gjøre» blir til hallusinerte flagg.
4. **En tabell med standardverdier.** Da slipper agenten å stille åtte
   spørsmål. Skriv også hva den IKKE skal spørre om: «spør ikke om WebP
   med mindre brukeren nevner det».
5. **Oppslagstabeller for alt som har et fast sett med gyldige verdier** —
   transitions, formater, egnethet. Agenten gjetter ellers på navn som ikke
   finnes.
6. **Fallgruver står der valget tas**, ikke i en «Tips»-seksjon til slutt.
   Advarselen om at GIF med fade på fotoinnhold blir 2–3 MB hører hjemme i
   steget der format velges.

### Struktur

- Frontmatter → Steg 0 (avhengighetssjekk) → én workflow per inputtype,
  nummerert → kommandoblokker → oppslagstabeller → standardverdier →
  fallgruver → opprydding.
- **Hver workflow slutter med å rapportere resultatet**: filnavn,
  filstørrelse, og hvilke innstillinger som ble brukt. Brukeren skal kunne
  si «prøv igjen med lavere fps» uten å gjette på hva som ble gjort.
- **Rydd opp i mellomfiler** (palette, temp) som eget siste steg.

### Fremgangsmåte

Skriv SKILL.md først, så tester vi den på ⟨en ekte fil⟩ med en gang. Alt
jeg må korrigere underveis er en mangel i skillen — skriv rettelsen inn i
SKILL.md i stedet for bare å fikse det i samtalen.

---

## Avklar før du starter

- **Er det egentlig én skill eller to?** Video→GIF og bilder→GIF deler
  verktøy men har ulike defaults og spørsmål. Her ble de to workflows i
  samme skill fordi triggerfrasene er like. Ulike triggere → egne skills.
- **Hva er outputkravet?** «Under 1–2 MB for e-post» er det som styrer alle
  defaults (fps, bredde, format). Uten et tall blir valgene vilkårlige.
- **Hvilke spørsmål er verdt å stille?** Hvert spørsmål koster en runde.
  Alt som har et fornuftig standardsvar hører hjemme i defaults-tabellen.
- **Test på det stygge tilfellet først** — den lange videoen, bildene med
  ulik størrelse. Det er der skillen trenger eksplisitte instruksjoner.

> Claude Code har `/skill-creator` innebygd for scaffolding og evals.
> Den lager strukturen; innholdet over er det som avgjør om skillen funker.
