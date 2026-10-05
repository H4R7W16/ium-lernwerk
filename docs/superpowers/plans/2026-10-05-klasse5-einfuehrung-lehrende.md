# Einführung für Lehrende Klasse 5 – Implementierungsplan

> Ausführung inline durch Codex, ohne Subagenten; Nutzer hat den gemeinsam entwickelten Entwurf am 05.10.2026 zur Umsetzung beauftragt.

**Ziel:** Ein selbstständig und gemeinsam nutzbarer Einstieg mit überspringbaren Abschnitten und freiwilligen Vertiefungen.
**Architektur:** Eigener Renderer und ausschließlich auf der Seite geladene CSS-Datei; vorhandener Mantel, Build und Cache. Original-Dateienfall wird aus dem bestehenden Inhalt gelesen. Natürliche Sprunglinks und details/summary; keine neue Runtime oder Speicherung.
**Technik:** CommonJS, HTML, CSS; node:test; keine neuen Abhängigkeiten.
**Entwurf:** Nutzerfreigabe im Chat; verbindlicher Umfang und Plan in der Task-Notiz „2026-10-05 - IUM Einführung für Lehrende Klasse 5 erstellen“.

## Grenzen und Prüffokus
- Merkmale, Konzeption, Beispiel, Begleitung, Vorbereitung als fünf frei erreichbare Abschnitte.
- Lernfolge als Dateienbeispiel; Thema entscheidet die konkrete Folge.
- Keine automatische Bewertung von Erklärungen oder Behauptung beobachteter Wirkung.
- Keine Erfassung von Demoantworten; persönliche Reflexionen privat.
- Alle Sprungziele, Originalfall, Gerätehandlung, Sicherung und Rückwege korrekt.
- Schmale Darstellung, Tastatur und Rückkehr aus verlinkter Einheit tatsächlich prüfen.

## Task 1: Einführung integrieren und prüfen
**Dateien:** class5-teacher-intro.cjs, einfuehrung.css; class5-teacher-pages.cjs und mantel-render.cjs; class5-teacher-intro.test.cjs.
**Schnittstellen:** render(pack) liefert HTML-Inhalt; packs.find(area=dateien) liefert Originalfall. prepare() liefert integrierte Ausgabenmap.
- [x] Integrationstests schreiben und rot ausführen: Seite fehlt, beide Tests schlagen deshalb fehl.
- [x] Renderfunktion, Seite, gezielte Gestaltung und Übersichtslink implementieren.
- [x] Gezielte neue und bestehende Prüfungen grün; frischen lokalen Build erzeugen.
- [x] Tatsächlichen Browserdurchgang und Selbstreview; nötige Nacharbeit und neue Prüffassung.
- [x] Qualitätsabschluss, Git-Fetch/Pull, lokaler Commit, Handoff.