# Pilot: Lernbewegung bei gezielter Überarbeitung erhalten

Stand 07.11.2026. Nutzer hat Vorgehen und Umsetzung in eigenem Entwicklungsbranch ausdrücklich beauftragt.

## Ziel, Fassung und Grenzen

Branch `feat/ium-lernbogen-pilot-20261107`, Ausgang `2c3b5563ae6f0a0888811df314337853dcb041f4`. Drei unterschiedliche Lernformen: reguläre Recherche Klasse 5, Medienprodukt Klasse 6, abschließende Programmierwerkstatt ALG-6 Klasse 7 im Kontext ALG-1–5 und späterer Wiederaufnahme. Gemeinsame Funktionen verlässlich führen; keine einheitliche Aufgabenschablone. Bestehende Ziele, Aufgabenzeit, Material, Eigenleistung und Ergebnisse erhalten. Keine Veröffentlichung oder Integration nach main.

## Umsetzung und Zuständigkeit

- [x] Isolierten lokalen Worktree anlegen, Ausgang prüfen und Vergleichsbuild erzeugen. 233 bestehende Pages-Tests bestanden; 1391 Dateien im Vergleichsbuild.
- [x] Recherche: eigene Aussage durch Quellenvergleich, Herkunft und begründeten Prüfstand führen. Bericht vor Eingriff; Bearbeiter `pilot_recherche`. Nur recherche.json, bestehender Textbogen, M02-Kommentar in klasse5.json. Alle vorhandenen Bogenfelder und Anker erhalten.
- [x] Medienprodukt: Dateifolge sichtbar, ein Notizort, Werkzeugprobe tatsächlich am Gerät zeigen, begründet korrekte Rechteangaben beibehalten. Bericht vor Eingriff; Bearbeiter `pilot_medien`. Nur medienprodukt.json, synchroner bestehender Projektspur-Download und unmittelbar betroffener Reihenkommentar in class6-media-project.cjs. Leserprobe und wirkliche Produktrevision erhalten.
- [x] ALG-6: Vorhersage/Fehlersuche vor Begriffsarbeit erhalten; doppelte Erklärung der vier Bausteine zusammenführen; vorhandene Randnotizen durch zugängliche Format-/Begriffshilfe an anderem Code stützen. Root bearbeitet alg-6.md, durchfuehrung-256.md, hoerbriefing.md und ihre erzeugten HTML-Ausgaben.
- [x] Root integriert die drei Pakete. Bestehende Hashbindungen durch eng begrenzte neue Revisionen fortführen, historische Manifeste nicht überschreiben. Gemeinsame Build-/Prüfdateien allein durch Root.
- [x] Vollständige Wege einschließlich Material, Wissen, Hilfen, Nachweisen, Lehrhinweisen und Anschluss bearbeiten. Tatsächliche Browserausgabe einschließlich druckfähiger Einzelmaterialien sichten; kein neuer PDF-Paginierungsnachweis, als Prüfgrenze dokumentiert. Unabhängiger Gegencheck der drei Wege auf Gewinne und Verluste, keine bloße Erledigungsliste.
- [x] Bestehende Pages-Prüfungen und Quell-/Ausgabesynchronität; Gesamtbuild; Ausgabevergleich gegen Ausgang auf erlaubte Änderungen. Fassungsgebundenen Qualitätszyklus ausführen; Bericht, Session und Git-Stand übergeben.

## Prüfungsschwerpunkte

Recherche: unvollständige erste Antwort, bereits tragfähige Antwort, scheinbarer Widerspruch; zwei Links plus Anbietername genügen weiterhin nicht. Medienprodukt: missverständliche Karte und korrekte Rechteleiste; keine doppelte Dokumentation, echte Leser-/Empfängerprobe. ALG-6: erste Fehlentscheidung selbst identifizieren; Werte/Wirkungen am ursprünglichen Code erklären; Schrittweite 12/15 und veränderter fester Teil erhalten. Weniger Text ist allein kein Erfolgskriterium.

## Arbeitsregeln und Nachweise

Der ganze betroffene Lernbogen ist die Bezugsgröße. Jedes Paket hält Lernbewegung, Hürde, erhaltene Eigenleistung, Aufwand und Verlustrisiko vor Änderung fest. Die Programmieraufgabe bildet einen vollständigen 60-Minuten-Abschlussbogen innerhalb der 405-Minuten-Reihe; frühere Aufgaben und spätere Wiederaufnahme werden auf Anschluss geprüft. Erhaltene Gesamtzeiten sind Planungsgrößen, keine gemessene Durchführbarkeit. Reale Lernenden-, Zeit- und Schulgeräteerprobung bleibt offen.

Entscheidung: Git-Worktree unter dem vom Nutzer vorgeschriebenen lokalen Work-Verzeichnis. Die native Worktree-Funktion bietet keine Wahl dieses Pfads; daher Git-Fallback. Keine neuen technischen Arbeitsbäume in OneDrive. Inhaltsrevisionen sind redaktionelle Änderungen; keine Wortlauttests hinzufügen. Bestehende Schutz-/Funktionstests verwenden und tatsächliche Ausgabe prüfen.

## Abschluss auf der geprüften Ausgangsbasis

Alle drei Pakete redaktionell umgesetzt und vollständig gegengeprüft. 233Tests bestanden, Build1391Dateien,27gezielte Änderungen,1364bytegleich. Formale Prüffassung a5b9cc297a4c64cf6095346aca62ddc5fd849da6f1d224d766e5c8e5407c0741:20Kriterien pass,3begründete minor-Grenzen,READY_FOR_REVIEW. Tatsächliche Erprobungsgrenzen stehen im Ergebnisbericht.

Währenddessen erreichte origin/main mit getrennten Papierturm-Änderungen51a9fd6. Fetch erfolgreich; vorgeschriebener pull --ff-only wegen Überschneidung der zwei Build-/Testdateien ohne Änderung abgebrochen. Pilot bleibt auf2c3b556 und wird nur lokal gesichert; kein Push. Spätere Integration muss Revisionsbasis und gemeinsamen Serviceworker neu binden und neu prüfen. M07-Inhalte und relevante M06-Anschlüsse sind auf Main unverändert; eigenständiger Gegencheck bestätigt Abschluss des isolierten Piloten.
