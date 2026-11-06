# IuM-Repository aktualisieren – Umsetzungsplan

> Ausführung mit superpowers:executing-plans; Abschlussprüfung mit superpowers:verification-before-completion.

**Ziel:** Der GitHub-Einstieg beschreibt das veröffentlichte Lernwerk 5–7 und ermöglicht eine reproduzierbare lokale Vorschau.

**Auftrag und Entwurf:** Nutzerauftrag vom 06.11.2026: GitHub-Repo überarbeiten und auf aktuellen Stand bringen. Bestandsabgleich zeigt eine überholte Klasse-5-README und einen veralteten Pages-Leitfaden. Dokumentation wird am aktuellen main b672e11 ausgerichtet. Inhalte, Laufzeit und Abhängigkeiten benötigen für diesen Abgleich keine Änderung. Die laufende Medienproduktion bleibt eigenständig.

**Arbeitsort:** Eigener Branch docs/ium-repo-aktualisierung-20261106 unter %USERPROFILE%/AI-Workspace-Local/Work/ium-repo-aktualisierung-20261106. Integration über Pull Request nach main. Native Worktree-Erstellung bietet keine Wahl des vorgeschriebenen lokalen Work-Verzeichnisses; deshalb git worktree add.

**Technik:** Markdown, bestehender Node-22-Pages-Generator, Python-Prüfungen.

## Dateien und Arbeitsschritte

- [x] README.md: aktuelle Links für Klasse 5, 6, 7 und Lehrpersonen, Lernwerkumfang, Speicherung, Erprobungsstand und Entwicklungsstart. Historische Beschreibung vollständig in einem aufklappbaren Abschnitt erhalten; die gebundenen IUM09/10/11-Abschnitte und Marker beibehalten.
- [x] prototypes/pages/README.md: tatsächliche Buildkette einschließlich Jahreswege, Klassenwahl, Gesamtkonzept, Themen und Arbeitsstellen dokumentieren. Quellorte und Prüfungen zuordnen.
- [x] CONTRIBUTING.md: Quellenbearbeitung, lokales Bauen/Ansehen, bestehende Prüfungen, sichere Git-Integration und Lizenzverweise knapp dokumentieren.
- [x] docs/projektstand.md: belegte jüngste Integrationen, aktueller Funktionsumfang und offene Erprobungs-/Entwicklungsgrenzen. Keine Entwürfe als veröffentlicht darstellen.
- [x] Bestehende Pages-Prüfkette und Build ausführen, neue relative Links und öffentliche Einstiegslinks prüfen; IUM11-Publikationsvertrag und Python-Regressionen prüfen.
- [ ] Lesenden Abschlussreview einholen, Befunde beheben; nach fetch/pull committen, pushen und per PR integrieren. CI und Pages bis zum Abschluss verfolgen.
- [ ] Session Summary mit Commit, Branch, Push-/Merge-/Prüfstand im gemeinsamen Vault erstellen.

## Prüfschwerpunkte

- Alle drei Jahrgangs- und Lehrpersoneneinstiege existieren tatsächlich.
- npm run build bezeichnet weiterhin das frühere Plattformfundament; die aktuelle Pages-Ausgabe entsteht mit node prototypes/pages/build.cjs.
- Das Buildziel muss neu sein; keine bestehende Ausgabe löschen.
- Die historische Zeitmodell-/Pilotfreigabe wird durch neue Dokumentation nicht hochgestuft.
- Klasse 7 hat noch keine gemeinsame Arbeitsübersicht wie Klasse 5/6. Keine einheitliche Speicherung oder Offlinefunktion für alle Jahrgänge behaupten.
- Keine fremden Arbeitsstände, Build-Artefakte, privaten Gerätedaten oder neuen Abhängigkeiten committen.

## Nachweise und Entscheidungen

Reine Dokumentationspflege: keine neuen Implementierungstests, sondern bestehende Vertrags-, Inhalts- und Linkprüfungen. Der ausdrückliche Repo-Aktualisierungsauftrag umfasst die Veröffentlichung dieser Dokumentation; die bereits anderweitig freigegebene Kopfzeile ist Basis, kein zusätzlicher Merge-Auftrag.

Prüfzwischenstand: 669 Python-Tests erfolgreich, IUM11-Publikationsvertrag aktuell, 1374 Pages-Dateien gebaut, 84 relative Dokumentationslinks vorhanden und zehn öffentliche Einstiege mit HTTP 200. Die vollständige Pages-Prüfkette meldete zunächst drei bereits auf main vorhandene Menüstil-Vertragsabweichungen; deren Korrektur wird im parallelen Kopfzeilenauftrag integriert und anschließend hier nachgezogen.

Abschluss der lokalen Prüfung: Korrektur PR 54 auf main d57db00 per Fast-forward übernommen; alle 190 Pages-Prüfungen bestanden. Der lesende Abschlussreview bestätigt Buildkette, Einstiege, Zeitkonten und historische Verträge. Sein kleiner Befund zu zu pauschalen Quellenhinweisen wurde korrigiert. GitHub-Kurzbeschreibung auf Klasse 5–7 aktualisiert und fehlende Website-Adresse ergänzt. Commit/PR/CI-Ergebnis werden in der Session Summary und im Pull Request dokumentiert.
