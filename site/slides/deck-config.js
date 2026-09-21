/* DK26-decket — lokale verdier.
 *
 * Dette er den eneste fila du trenger å redigere før presentasjonen.
 * Feltene tilsvarer «Åpne felter» i Claude Design, men her er de faste
 * så decket virker uten editoren.
 *
 * Kjør `python3 bygg.py` etter hver endring her. Url-ene styrer QR-kodene
 * (ferdige PNG-er i assets/, ikke API-kall), og visThumbnails styrer om
 * `no-rail` settes på decket i index.html.
 */
window.DK26 = {
  "wifiPassord": "GanskeVanskelig",
  "urlPrompt": "https://work.bas.no/dk26/materiell/",
  "urlRapport": "https://work.bas.no/dk26/rapport/",
  "urlRepo": "https://github.com/suntandan/bas-skills",

  // Thumbnail-stripa til venstre. Grei å ha når du forbereder deg,
  // men den skal ikke være med på lerretet.
  "visThumbnails": false
};
