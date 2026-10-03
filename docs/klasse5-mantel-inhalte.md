# Klasse-5-Mantel: Inhalte aufnehmen und prüfen

Der gemeinsame Einstieg liegt unter `klasse5/`. Die drei vorhandenen Werkzeuge beziehen ihre Inhalte weiterhin aus den jeweiligen `content.js` beziehungsweise `studio-learning.js`-Dateien. Der Mantel kopiert deren vollständige Seiten aus derselben Quelle und ergänzt die gemeinsame Oberfläche. Historische Einstiegspfade bleiben erhalten.

## Inhalt ohne neue UI-Programmierung

Weitere Lerneinheiten aus den allgemeinen Inhaltstypen werden als UTF-8-JSON unter `prototypes/shared/inhalte/` aufgenommen. Das erste vollständige Autorenpaket ist dateien.json; dessen Ordner und Assets sind die praktische Referenz. `class5-content.cjs` validiert jede Datei und erzeugt daraus Einstieg, Schritte, vollständige Einzelmaterialien, Wissen/Materialübersicht und Lehrpersonenhinweise. Ein fehlerhafter Lernbogen stoppt den Build.

Pflichtfelder: `area` (stabile URL-ID), `id` (IUM-5-…), `version` (SemVer), `grade:5`, `family:"content"`, `title`, `topic`, `description`, `product`, `prerequisites`, `teacher`, `steps`, `coverage`. Jeder Schritt hat `id,title,goal,criteria,blocks`. `coverage` verweist für entry/explanation/example/practice/application/revision/securing/transfer/retrieval auf vorhandene Schritt-IDs. Die Redaktion prüft zusätzlich die fachliche Qualität; vorhandene Felder beweisen keine Lernwirksamkeit.

Bekannte Blöcke: explanation, example, task, external, cooperative, private, retrieval. Alle tragen title/text, antwortende Blöcke zusätzlich id/prompt. Aufgaben können solution für einen bewusst geöffneten Vergleich enthalten.

- external: preparation, action, HTTPS-url, return. Für eine lokale Gerätehandlung in Autorenversion 2 stattdessen context:"device" und konkrete routes; dafür wird kein Internetzugang behauptet. Der Link öffnet einen neuen Tab und kennzeichnet den Internetbedarf. Die Rückkehr verlangt ein eigenes Ergebnis. Eine Simulation wird nicht als erledigte Recherche ausgegeben.
- cooperative: contribution, exchange, return. Reale Beiträge und Austausch sowie die anschließende eigene Erklärung sind beschrieben. Der Mantel bestätigt keine stattgefundene Kooperation.
- private: harmlose eigene Erfahrung/Nichtnutzung redaktionell ermöglichen; keine Pflichtoffenlegung. Persönliche Texte bleiben außerhalb normaler Speicher-/Export-/Druckdaten. Eine gesonderte Textdatei braucht eine eigene Vorschau und Bestätigung.
- retrieval: when und solution. Zuerst selbst rekonstruieren, danach vergleichen; der Mantel schickt keine Erinnerungen.

Ein minimales, schemafähiges Beispiel mit diesen Blocktypen steht im Vertragstest `mantel.test.cjs`. Es wird nicht als echtes Lernangebot veröffentlicht. Für die Übernahme einer vorhandenen Werkzeugfamilie dienen die drei bestehenden Inhaltsquellen als verbindliche Vorlagen. Neue fachliche Interaktionen benötigen weiterhin einen eigenen geprüften Adapter; ein JSON-Inhalt kann keine unbekannte Simulation erzeugen.

Der gemeinsame Katalog ist ein Mantel-Inhaltsvertrag, kein Ersatz für den vollständigen Plattform-`ModuleManifest`. Die versionierte Arbeitsdatei verwendet den vorhandenen `ium-learning-state`-Envelope mit dem familienbezogenen Payload `klasse5-mantel-1`. Keine neue konkurrierende Modul-ID-Systematik.

## Arbeit und Fehler

Standard: normale Arbeit im sessionStorage des laufenden Tabs. Gerätesicherung ist freiwillig. Browser können Tabs wiederherstellen; Schließen garantiert keine endgültige Löschung. Ausschalten beendet neue dauerhafte Sicherungen und erklärt die weiter vorhandene Kopie. Dateiexport bestätigt ausschließlich das Dateiangebot.

Ein Arbeitsstand besitzt eine eigene UUID. Neu beginnen und Importieren erzeugen bevorzugt einen separaten Stand. Bestehende Texte werden ausschließlich über textContent/HTML-Escaping angezeigt. Größe, Version, Feldkategorien und alle bekannten Werkzeugdaten werden vor einer Vorschau validiert. Beschädigte und fremde Dateien verändern die vorhandene Arbeit nicht. Nicht mehr kompatible lokale Kopien bleiben erhalten und lassen sich unverändert als Datei sichern.

Offlinevorbereitung verwendet einen eigenen Scope `klasse5/`. Erst ein vollständiger Cache-Nachweis heißt „offline bereit“. Fehlschlag und Updatewarten sind eigene Zustände. Die alte Fassung wird nicht automatisch abgelöst; vor freiwilliger Übernahme wird die Arbeit gesichert. Reale Internetrecherche bleibt online.

## Redaktionsabnahme

Prüfen Sie vollständige Lernbögen, gültige Direktlinks, Materialherkunft, freie Hilfen, Rückmeldung mit Revision, Transfer und spätere Wiederaufnahme. Schulbezogene Hilfewege werden in den Lehrpersonenhinweisen vorbereitet und von der jeweiligen Schule ergänzt. Lokale Kontakte sind keine Voraussetzung für eine schulübergreifende Veröffentlichung.

Technischer Schnelltest: Node 22, `node --test prototypes/shared/mantel.test.cjs`, danach der bestehende Pages-Build in ein frisches lokales Work-Verzeichnis. Keine technischen Arbeitsbäume oder Buildausgaben in OneDrive.

Vor dem Unterricht bleiben Tests auf den tatsächlich vorgesehenen Schulgeräten und eine Unterrichtserprobung erforderlich. Die bisherige Prüfung ist keine vollständige AA-Konformitäts- oder Lernwirksamkeitsbescheinigung.


## Autorenversion 2: vollständiges redaktionelles Paket
Neue Serieninhalte verwenden authorVersion:2. Zusätzlich erforderlich:
- duration als ausgewiesene Zeitannahme; curriculum mit moduleId, goalIds, source und ehrlicher scope-Grenze.
- sources: stabile id, title, author, HTTPS-url, license und checked. Das Prüfdatum ist redaktionell, keine technische Bestätigung der Richtigkeit.
- knowledge: id, Fragestellung/title, paragraphs, example, boundary, Schritte und Quellen-/Medienreferenzen.
- media: lokale Datei unter assets/, id, kind:image oder download, title, creator, license, sourceId. Bilder brauchen alt und caption. Textdownloads tragen printText, der mit der tatsächlichen Datei übereinstimmen muss.
- steps ergänzen task, outcome, knowledge. Optionale prerequisites nennen die Besonderheiten eines direkt geöffneten Schritts; sie ergänzen die allgemeinen Voraussetzungen.
- Blöcke können paragraphs, items, table, media, sources, help und routes tragen. Listen und Tabellen bleiben strukturierte Daten, kein HTML.
- teacherSections und briefing ermöglichen gegliederte Lehrpersonenhinweise und einen eigenständigen Vorlesetext. preview verweist auf eine eigene Bild-ID.

Wissen und Material haben verschiedene Ausgaben: Wissensartikel mit Beispielen/Aussagegrenzen einerseits, vollständige Einzelblätter und echte Übungsdateien andererseits. Das Paket erzeugt Einstieg, Schrittseiten, Wissen, Materialübersicht, sieben beziehungsweise entsprechend viele Einzelblätter, Lehrpersonenhinweise und Briefing. Kleine lokale Assets werden auch ins Offlinepaket aufgenommen; verlinkte Herstellerseiten werden nicht kopiert.

Die Validierung stoppt ungültige Referenzen, doppelte IDs, unzulässige Pfade, fehlende Pflichtangaben und abweichende Druck-/Downloadtexte. Medien dürfen maximal 2 MiB groß sein. Erlaubt sind SVG/PNG/JPEG/WebP und TXT; SVGs dürfen keine erkannten aktiven Inhalte oder externen Ressourcen einbetten. Andere Medien brauchen einen eigenen geprüften Anschluss. Rechteangaben werden auf Vorhandensein geprüft; ihre Rechtmäßigkeit muss die Redaktion klären.

Druckauswahl: Lernendenblatt, mit Hilfen, mit Hilfen und Lösungen. Die Druckvorbereitung öffnet nur die passende Gruppe und stellt danach den Lesestand wieder her. Kontrollierte Felder bleiben außerhalb des Drucks. Ohne JavaScript ist nur die Grundfassung gewährleistet; reale Geräteaufträge bleiben als Voraussetzung erkennbar.

Die Rückkehr aus Wissen/Material merkt sich im Tab den zuletzt geöffneten Autoren-Schritt auch vor einer Antwort. Diese Navigation wird nicht als Lernnachweis/Arbeitsprodukt angelegt. Das Arbeitsdateiformat bleibt unverändert.

Produktionsfolge, Versionsbindung und kopierbarer Folgeauftrag: [Klasse 5](produktion/klasse5.md). Fachbrief und Selbstreview des ersten Pakets: [Dateien](produktion/g5-m01-dateien.md).


## Redaktionelle Ergänzungen aus dem Dateien-Review · 04.10.2026
- learnerDuration trennt den kurzen Lernendenhinweis von der Lehrpersonen-Zeitannahme.
- Schritt timing:later trennt den späteren Abruf in Einstieg und Vorwärtsnavigation. completion mit title/text erzeugt den aktuellen Abschluss auch auf dem Einzelblatt.
- responseHint steht vor dem Antwortfeld; responseMode:oral bietet eine freiwillige digitale Notiz. Auch im Papiermaterial ist mündliches Antworten möglich.
- routes.items akzeptiert weiter Strings oder strukturierte Schritte mit title, text und optionalen validierten media-Referenzen. Downloads stehen dadurch am Handlungspunkt.
- Gerätewege sind Kernmaterial: auf Einzelblättern geöffnet, bei allen Druckmodi enthalten; nach dem Druck kehrt der vorherige Klappzustand zurück. Zusätzliche Hilfen und Lösungen bleiben getrennt.
- workNotice / storageNotice erläutern die Grenze zwischen Lernwerk-Antworten und externen Dateien. Kein Zugriff auf tatsächliche Geräteordner.


## Modellnähe, Prüfhilfen und Materialvarianten · 04.10.2026
- layout:model-task gruppiert genau ein Beispiel und eine anschließende Aufgabe, responsiv und auf dem Blatt.
- checkHelp nennt je Schritt title/text und optional step oder knowledge mit label für geprüfte Direktlinks. Dieselben Linkfelder sind in help möglich; Kriterien bleiben unverändert.
- experiencedEntry (title/text/step/label) empfiehlt einen geprüften Einstieg, ohne andere Schritte zu sperren.
- materialNeeds ersetzt auf dem Einzelblatt die pauschalen Paketvoraussetzungen. deviceNeeds kann abweichenden Bedarf für ipad/windows enthalten.
- routes.device ordnet einen vollständigen Geräteweg zu. Für vorhandene Geräte erzeugt der Renderer baustein-SCHRITT-ipad.html bzw. -windows.html zusätzlich zum kombinierten Blatt. Medien, Aufgaben und Kriterien bleiben vollständig enthalten; die Auswahl benötigt kein JavaScript.
