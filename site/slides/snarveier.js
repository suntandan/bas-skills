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

  /* Kort kvittering midt på skjermen. Uten den er en snarvei som ikke
   * virker umulig å skille fra en som virker på noe usynlig. */
  let toastEl = null;
  let toastTimer = null;
  function toast(tekst) {
    if (!toastEl) {
      toastEl = document.createElement('div');
      toastEl.setAttribute('role', 'status');
      toastEl.style.cssText = [
        'position:fixed', 'left:50%', 'bottom:72px', 'transform:translateX(-50%)',
        'z-index:2147483000', 'padding:10px 18px', 'border-radius:999px',
        'background:rgba(20,20,20,.92)', 'color:#fff',
        'font:500 15px/1 ui-sans-serif,system-ui,sans-serif',
        'letter-spacing:.01em', 'pointer-events:none',
        'opacity:0', 'transition:opacity 140ms ease',
      ].join(';');
      document.body.appendChild(toastEl);
    }
    toastEl.textContent = tekst;
    toastEl.style.opacity = '1';
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => { toastEl.style.opacity = '0'; }, 1100);
  }

  /* Capture-fasen: da er vi først uansett hvem andre som lytter, og
   * uavhengig av om noe lenger ned kaller stopPropagation.
   * e.code i tillegg til e.key, så tastaturoppsett ikke spiller inn. */
  window.addEventListener('keydown', (e) => {
    if (e.code !== 'KeyT' && e.key !== 't' && e.key !== 'T') return;
    // Samme forbehold som deck-stage sin egen _onKey: ikke stjel tasten
    // mens noen skriver, og ikke tolk cmd+T / ctrl+T som vår.
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const t = e.composedPath ? e.composedPath()[0] : e.target;
    if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;

    synlig = !synlig;
    window.postMessage({ type: '__deck_rail_visible', on: synlig }, '*');
    toast(synlig ? 'Stripe på' : 'Stripe av');
    e.preventDefault();
  }, true);
})();
