'use strict';

// Der URL-Parameter verweist ausschließlich auf eine beim Rendern registrierte Arbeitsstelle.
(() => {
  const roots = /* PUBLIC_ORIGINS */ {};
  const base = new URL('./', document.currentScript.src);
  const page = new URL(location.href).pathname.slice(base.pathname.length);
  const parameter = 'arbeitsstelle';
  const marked = '[data-arbeitsstelle]';
  const support = /^(?:wissen|material|quellen|(?:baustein|bild|hilfe|leas-weg)-[a-z0-9-]+)\.html$/;

  function origin(token) {
    if (!token) return null;
    const [file, id] = token.split('#');
    if (token !== file + '#' + id || !Object.hasOwn(roots, file) || !Object.hasOwn(roots[file], id)) return null;
    return {token, label: roots[file][id], href: new URL(token, base).href};
  }

  function placeFor(link) {
    if (!Object.hasOwn(roots, page) || link.closest('[data-private]')) return null;
    const here = link.closest(marked);
    if (here) return origin(page + '#' + here.id);

    // Ein Wissens- oder Materialverweis nach dem Arbeitsauftrag führt zur letzten
    // zugehörigen Antwort. Bei mündlichen Aufgaben bleibt die eingeklappte Notiz zu.
    const places = [...document.querySelectorAll('main ' + marked)]
      .filter(node => !node.closest('[data-private], details:not([open])'));
    const preceding = places.filter(node => node.compareDocumentPosition(link) & Node.DOCUMENT_POSITION_FOLLOWING);
    const last = preceding.filter(node => node.matches('label')).pop()
      || preceding.filter(node => node.matches('section')).pop() || preceding.pop() || places[0];
    return last ? origin(page + '#' + last.id) : null;
  }

  const tokens = new URL(location.href).searchParams.getAll(parameter);
  const currentOrigin = tokens.length === 1 ? origin(tokens[0]) : null;

  function setLinks() {
    for (const link of document.querySelectorAll('main a[href], .lw-shell-nav > a[href]')) {
      if (link.hasAttribute('download') || link.closest('[data-private]')) continue;
      const target = new URL(link.href);
      if (target.origin !== base.origin || !target.pathname.startsWith(base.pathname)) continue;
      const file = target.pathname.slice(base.pathname.length);
      if (currentOrigin && link.hasAttribute('data-lw-return')) {
        link.removeAttribute('data-lw-return');
        link.href = currentOrigin.href;
        continue;
      }
      const name = file.split('/').pop();
      const helpStep = name.startsWith('schritt-') && link.closest('details.lw-help, .lw-check-help');
      if (!support.test(name) && !helpStep) continue;
      // Jahrgangsweite Übersichten sind bewusst außerhalb eines einzelnen Lernwegs.
      if (!/^[a-z0-9-]+\/[a-z0-9-]+\.html$/.test(file)) continue;
      const from = currentOrigin || placeFor(link);
      if (from) {
        target.searchParams.set(parameter, from.token);
        link.href = target.href;
      }
    }
  }

  function showReturn() {
    if (!currentOrigin) return;
    document.querySelector('[data-arbeitsstellen-return]')?.remove();
    const main = document.querySelector('main');
    if (!main) return;
    const target = document.getElementById(location.hash.slice(1));
    const section = target && main.contains(target) ? target : null;
    const heading = section
      ? (section.matches('h1, h2, h3, h4') ? section : section.querySelector('h1, h2, h3, h4'))
      : main.querySelector('h1');
    const link = document.createElement('a');
    link.setAttribute('data-arbeitsstellen-return', '');
    link.className = 'lw-arbeitsstellen-return';
    link.href = currentOrigin.href;
    link.textContent = '← Zurück zur Arbeitsstelle: ' + currentOrigin.label;
    if (heading) heading.insertAdjacentElement('afterend', link);
    else if (section) section.insertAdjacentElement('afterend', link);
    else main.prepend(link);
  }

  function revealWorkplace() {
    const id = location.hash.slice(1);
    const place = document.getElementById(id);
    if (!place?.matches(marked) || !roots[page] || !Object.hasOwn(roots[page], id)) return;
    for (let node = place.parentElement; node; node = node.parentElement) {
      if (node.tagName === 'DETAILS') node.open = true;
    }
    place.scrollIntoView({block: 'start'});
  }

  setLinks();
  showReturn();
  revealWorkplace();
  window.addEventListener('hashchange', () => { showReturn(); revealWorkplace(); });
})();
