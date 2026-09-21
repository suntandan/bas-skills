#!/usr/bin/env python3
"""Bygg index.html fra Claude Design-kilden, og lag QR-kodene.

    python3 bygg.py

Kilden (src/DK26 Slides.dc.html) er uendret slik den kommer fra
claude.ai/design. Alt som skal til for at decket skal virke som en vanlig
statisk side — uten Claude Design-editoren og uten nett — gjøres her:

  1. React, ReactDOM og Babel pekes til vendor/ i stedet for unpkg.
     dc-runtime har en offisiell krok for dette: window.__resources.
  2. Font-lenkene til Google Fonts og Fontshare byttes med fonts/fonts.css.
  3. deck-config.js lastes, så wifi-passord og url-er er faste verdier.
  4. QR-kodene lages som PNG-er i assets/ i stedet for å hentes fra
     api.qrserver.com mens du presenterer.

Kjør på nytt hver gang src/ eller deck-config.js endres.
"""

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "src" / "DK26 Slides.dc.html"
OUT = HERE / "index.html"
CONFIG = HERE / "deck-config.js"

CDN = {
    "https://unpkg.com/react@18.3.1/umd/react.production.min.js":
        "vendor/react.production.min.js",
    "https://unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js":
        "vendor/react-dom.production.min.js",
    "https://unpkg.com/@babel/standalone@7.29.0/babel.min.js":
        "vendor/babel.min.js",
}

# Feltnavn i deck-config.js -> filnavn under assets/
QR_FIELDS = {"urlPrompt": "prompt", "urlRapport": "rapport", "urlRepo": "repo"}

BANNER = "<!-- GENERERT av bygg.py — rediger src/ eller deck-config.js, ikke denne. -->"

HEAD = """{banner}
<script>
/* Bruk vendor/-kopiene i stedet for unpkg, så decket virker uten nett. */
window.__resources = {resources};
/* Thumbnail-stripa til venstre. deck-stage leser denne innstillingen når
 * den starter opp — se _enableRail() i deck-stage.js. Styres av
 * visThumbnails i deck-config.js; vi skriver begge verdier, ellers ville
 * en gammel «skjul» ligget igjen i nettleseren etter at flagget slås på.
 *
 * (`no-rail`-attributtet er den andre veien, men x-import gjør om
 *  bindestreker til camelCase, så det kommer aldri fram til elementet.) */
try {{ localStorage.setItem('deck-stage.railVisible', {rail}); }} catch (e) {{}}
</script>
<script src="./deck-config.js"></script>
<script src="./snarveier.js" defer></script>
<script src="./support.js"></script>"""

FONT_LINKS = """  <link href="fonts/fonts.css" rel="stylesheet">"""


def read_config():
    txt = CONFIG.read_text(encoding="utf-8")
    m = re.search(r"window\.DK26\s*=\s*(\{.*?\n\})\s*;", txt, re.S)
    if not m:
        sys.exit(f"Fant ikke «window.DK26 = {{...}};» i {CONFIG.name}")
    # Hele linjer med // er lov i fila, men ikke i JSON. (Bare hele linjer,
    # så vi ikke kapper // midt i en url.)
    body = "\n".join(
        line for line in m.group(1).splitlines() if not line.lstrip().startswith("//")
    )
    # Etterfølgende komma er heller ikke lov i JSON.
    body = re.sub(r",(\s*[}\]])", r"\1", body)
    try:
        return json.loads(body)
    except json.JSONDecodeError as e:
        sys.exit(f"{CONFIG.name} er ikke gyldig JSON i DK26-objektet: {e}")


def make_qr_codes(cfg):
    """Lag PNG per utfylt url. Returnerer {kortnavn: filsti-eller-None}."""
    made = {}
    todo = {k: cfg.get(k, "").strip() for k in QR_FIELDS}
    if any(todo.values()):
        try:
            import qrcode
        except ImportError:
            sys.exit(
                "Mangler qrcode-modulen. Installer med:\n"
                "  python3 -m pip install qrcode pillow"
            )
    for field, short in QR_FIELDS.items():
        url = todo[field]
        path = HERE / "assets" / f"qr-{short}.png"
        if not url:
            made[short] = None
            if path.exists():
                path.unlink()
                print(f"  fjernet {path.name} ({field} er tom)")
            continue
        # Samme uttrykk som originalen brukte mot api.qrserver.com.
        img = qrcode.QRCode(border=1, box_size=20, error_correction=qrcode.ERROR_CORRECT_M)
        img.add_data(url)
        img.make(fit=True)
        img.make_image(fill_color="#111115", back_color="#fef6ed").save(path)
        made[short] = f"assets/{path.name}"
        print(f"  {path.name}  ->  {url}")
    return made


def build(cfg, qr_paths):
    html = SRC.read_text(encoding="utf-8")

    # 1 + 3. Erstatt support.js-taggen med resources-krok, config og support.
    old_head = '<script src="./support.js"></script>'
    if old_head not in html:
        sys.exit("Fant ikke support.js-taggen i kilden — har formatet endret seg?")
    html = html.replace(
        old_head,
        HEAD.format(
            banner=BANNER,
            resources=json.dumps(CDN, indent=2),
            rail="'1'" if cfg.get("visThumbnails", False) else "'0'",
        ),
        1,
    )

    # 2. Bytt ut de tre eksterne font-lenkene med den selvhostede css-en.
    font_block = re.search(
        r'[ \t]*<link rel="preconnect"[^>]*>\n'
        r'[ \t]*<link href="https://fonts\.googleapis\.com[^>]*>\n'
        r'[ \t]*<link href="https://api\.fontshare\.com[^>]*>\n',
        html,
    )
    if not font_block:
        sys.exit("Fant ikke font-lenkene i kilden — har formatet endret seg?")
    html = html[: font_block.start()] + FONT_LINKS + "\n" + html[font_block.end():]

    # 4. qr() slår opp ferdige PNG-er i stedet for å bygge en api-url.
    old_qr = re.search(r"^ {2}qr\(url\) \{.*?\}\n", html, re.M | re.S)
    if not old_qr:
        sys.exit("Fant ikke qr()-metoden i kilden — har formatet endret seg?")
    table = json.dumps({k: v for k, v in qr_paths.items()})
    html = html[: old_qr.start()] + f"  qr(navn) {{ return {table}[navn] || null; }}\n" + html[old_qr.end():]

    html = html.replace(
        "const qrPrompt = this.qr(p.urlPrompt), qrRapport = this.qr(p.urlRapport), qrRepo = this.qr(p.urlRepo);",
        "const qrPrompt = this.qr('prompt'), qrRapport = this.qr('rapport'), qrRepo = this.qr('repo');",
        1,
    )
    wifi = cfg.get("wifiPassord", "").strip()
    html = html.replace(
        "const pw = p.wifiPassord || '[fylles inn]';",
        f"const pw = p.wifiPassord || {json.dumps(wifi or '[fylles inn]')};",
        1,
    )

    OUT.write_text(html, encoding="utf-8")


def main():
    cfg = read_config()
    print("QR-koder:")
    qr_paths = make_qr_codes(cfg)
    build(cfg, qr_paths)
    print(f"\nSkrev {OUT.name} ({OUT.stat().st_size / 1024:.0f} kB)")
    if not cfg.get("wifiPassord", "").strip():
        print("Merk: wifiPassord er tom — decket viser «[fylles inn]».")
    if not cfg.get("urlRapport", "").strip():
        print("Merk: urlRapport er tom — QR-slidet står uten kode.")
    if cfg.get("visThumbnails", False):
        print("Merk: thumbnail-stripa er på — skru av før presentasjon.")


if __name__ == "__main__":
    main()
