'use strict';
/* Nur die reguläre Jahrgangsnavigation; keine Arbeitsstände oder Fachwerkzeuge. */
(() => {
  const close = menu => {
    menu.open = false;
    menu.querySelector('summary').focus();
  };
  for (const menu of document.querySelectorAll('.year-shell-header .year-topics')) {
    menu.querySelector('[data-lw-close-menu]').addEventListener('click', () => close(menu));
  }
  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    for (const menu of document.querySelectorAll('.year-shell-header .year-topics[open]')) close(menu);
  });
})();
