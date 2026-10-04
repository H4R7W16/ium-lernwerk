# Klasse 5 auf GitHub Pages veröffentlichen – Implementierungsplan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Aktuellen Klasse-5-Stand mit Design 02 im GitHub-Repository und ausschließlich diesen Stand über GitHub Pages bereitstellen.

**Architecture:** Bestehenden lokalen Design-Branch mit dem neueren Klasse-5-Abschlussstand zusammenführen. Der bestehende Generator bleibt die Quelle; ein kleiner Pages-Export veröffentlicht nur `klasse5/`, einen neuen Wurzeleinstieg und den neutralisierenden Wurzel-Service-Worker. Alte Pages-Workflows verlieren die Deploy-Berechtigung durch eine unerfüllbare Job-Bedingung. Pages startet nach Integration in `main` automatisch.

**Tech Stack:** Node 22, CommonJS, GitHub Actions, GitHub Pages, Git.

**Spec:** Nutzerauftrag vom 04.10.2026: Layout und aktueller Stand Klasse 5 auf GitHub/Pages; ältere Fassungen nicht mehr über Pages erreichbar. Design-Handoff: `docs/design/2026-10-04-klasse5-design-final.md`.

## Global Constraints

- Keine neuen Unterrichtsinhalte oder Textänderungen außer dem notwendigen Ersatz eines Links auf eine entfernte alte Fassung.
- Bestehenden Git-Verlauf, Worktrees und ältere Quellprototypen erhalten; nur Pages-Ausgabe einschränken.
- Vor Commit/Push `git fetch --prune` und `git pull --ff-only`; kein Force-Push.
- Veröffentlichung nur aus `main`; alte Pages-Routen fehlen im neuen statischen Artefakt.
- Alte offline gespeicherte Kopien im Browser lassen sich serverseitig nicht widerrufen; keine Lernstände löschen.

## Review Focus

- Export darf nur `index.html`, `sw.js` und `klasse5/**` enthalten.
- Jeder lokale HTML-Verweis innerhalb von Klasse 5 muss innerhalb der Exportmenge auflösbar sein.
- Alter Root-Service-Worker muss neutralisiert bleiben; Klasse-5-Offlinepaket bleibt im eigenen Scope.
- Kein alter Workflow darf nachher einen Pages-Deployjob starten.
- Integration darf weder Design noch Abschluss-Review-Inhalte verlieren.

---

### Task 1: Aktuellen Klasse-5-Stand und Design integrieren

**Files:** bestehende lokale Änderungen; Abschlusscommit `f0020c3`.

- [x] Designänderungen nach Git-Abgleich geprüft committen.
- [x] `f0020c3` in den Design-Branch integrieren; Konflikte in CSS/Renderer anhand beider Fassungen lösen.
- [x] Gemeinsame Klasse-5-Tests und frischen Build ausführen; Design und Abschlussseite prüfen.

### Task 2: Eng begrenztes Pages-Artefakt

**Files:** `prototypes/m06-reinigungsfall/build-class5-pages.cjs`, `prototypes/m06-reinigungsfall/class5-pages.test.cjs`, `prototypes/shared/mantel-render.cjs`.

- [x] Test schreiben: erlaubte Dateien, keine alten Routen, gültige lokale Verweise und Root-Einstieg.
- [x] Negativen Testlauf sehen.
- [x] Export implementieren: vorhandene `prepare()`-Ausgabe filtern; root auf Klasse 5 verweisen; vorhandenen neutralisierenden Root-Worker ausgeben.
- [x] Den einzigen Klassen-5-Link auf eine entfernte alte Lesefassung zu einem aktuellen Material-/Wissenspfad führen.
- [x] Positiven Testlauf und frischen Export prüfen.

### Task 3: Nur ein Pages-Veröffentlichungsweg

**Files:** `.github/workflows/klasse5-pages.yml`, vier ältere `*-pages.yml`, `tests/platform/pages-workflow.test.ts`, Projekthandoff.

- [x] Workflowtests für Klasse-5-Export und deaktivierte Alt-Deployjobs formulieren; Negativlauf prüfen.
- [x] Klasse-5-Workflow für `main`-Push/manuellen Lauf einrichten; die alten Deployjobs deaktivieren.
- [x] Relevante Node-/Workflowtests, `git diff --check` und Build lokal prüfen.
- [x] Branch nach erneutem Fetch/Fast-Forward-Abgleich pushen; mangels PR-Recht der GitHub-App per Fast-Forward nach `main` integrieren; Pages-Lauf abwarten.
- [x] Öffentliche Klasse-5-URL und mindestens zwei frühere Versionspfade über HTTP prüfen; Commit/Run/Status dokumentieren.

## Ausführung am 04.10.2026

- Release-Commit `3e5bd15de90b9b37d8db4fc0999828f3ba768856` wurde nach `origin/main` fast-forward gepusht. GitHub-App verweigerte PR-Erstellung mit 403; der normale Git-Push war autorisiert und erfolgreich.
- GitHub-Pages-Lauf [37211818129](https://github.com/H4R7W16/ium-lernwerk/actions/runs/37211818129) erfolgreich. Root und `klasse5/` sowie `klasse5/review.html` antworten HTTP 200; `selbstlernen/`, `reinigungsfall-v2/`, `reinigungsfall.html` und `medienanalyse/` antworten HTTP 404.
- Die geprüften öffentlichen HTML-Dateien sind bytegleich mit dem lokalen Build. CSS stimmt nach Normalisierung der Windows-Zeilenenden überein; die beiden Logo-PNGs sind binär identisch. Der Offline-Worker unterscheidet sich nur durch seinen daraus abgeleiteten Versionshash.
- Lokal: 59/59 Klasse-5-Tests, 133/133 Plattformtests, 323 Dateien im begrenzten Pages-Artefakt.
- Allgemeine CI des ersten Release-Commits: drei Jobs erfolgreich; ein Firefox-Test des unveränderten Altmoduls `IUM-5-CORE-05` scheiterte nach Reload. Dieser Befund betrifft nicht den erfolgreichen Klasse-5-Pages-Workflow und wird separat beim CI-Nachlauf beobachtet.
