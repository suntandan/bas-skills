# site/

Statiske sider som legges på `work.bas.no`.

## materiell/

Nedlastingsside for startpromptene fra DK26. Publisert på
`work.bas.no/dk26/materiell/` — last opp hele `materiell/`-mappa som den er:

```
materiell/
  index.html
  bas-logo.png
  filer/
    startprompt-preflight.md
    startprompt-bildeverktoy.md
    startprompt-skill.md
    startprompter-dk26.zip
```

Alle lenker er relative, så mappa kan ligge hvor som helst.

Kildefilene ligger i `prompts/` i rota. Etter endring der:

```bash
cp prompts/*.md site/materiell/filer/
cd site/materiell/filer && zip -q -X startprompter-dk26.zip *.md
```

Husk å oppdatere `~X kB` i `index.html` hvis filstørrelsene endrer seg
merkbart.

Lokal forhåndsvisning:

```bash
cd site && python3 -m http.server 8787   # → http://localhost:8787/materiell/
```

«KOPIER»-knappen henter filen med `fetch`, så den virker ikke via
`file://` — bruk en server.
