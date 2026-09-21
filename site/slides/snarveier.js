/* Egne tastatursnarveier på toppen av deck-stage sine.
 *
 *   T   vis/skjul thumbnail-stripa til venstre
 *
 * deck-stage lytter selv på window for meldingen under — kommentaren i
 * deck-stage.js kaller den «the TweaksPanel toggle (or any author script)»,
 * så dette er den støttede veien inn. Den animerer stripa, re-fitter
 * slidet og skalerer miniatyrene selv.
 *
 * Merk: deck-stage lagrer valget i localStorage, men bygg.py skriver den
 * verdien på nytt ved hver sidelast. Snarveien gjelder altså for økta;
 * utgangspunktet bestemmes av visThumbnails i deck-config.js.
 */
(() => {
  let synlig = true;
  try {
    synlig = localStorage.getItem('deck-stage.railVisible') !== '0';
  } catch (e) {}

  window.addEventListener('keydown', (e) => {
    if (e.key !== 't' && e.key !== 'T') return;
    // Samme forbehold som deck-stage sin egen _onKey: ikke stjel tasten
    // mens noen skriver, og ikke tolk cmd+T / ctrl+T som vår.
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const t = e.composedPath ? e.composedPath()[0] : e.target;
    if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;

    synlig = !synlig;
    window.postMessage({ type: '__deck_rail_visible', on: synlig }, '*');
    e.preventDefault();
  });
})();
