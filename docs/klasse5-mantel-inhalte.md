# Klasse-5-Mantel: Inhalte aufnehmen und prüfen

Der gemeinsame Einstieg liegt unter `klasse5/`. Die drei vorhandenen Werkzeuge beziehen ihre Inhalte weiterhin aus den jeweiligen `content.js` beziehungsweise `studio-learning.js`-Dateien. Der Mantel kopiert deren vollständige Seiten aus derselben Quelle und ergänzt die gemeinsame Oberfläche. Historische Einstiegspfade bleiben erhalten.

## Inhalt ohne neue UI-Programmierung

Weitere Lerneinheiten aus den allgemeinen Inhaltstypen werden als UTF-8-JSON unter `prototypes/shared/inhalte/` aufgenommen. Der Ordner muss erst mit dem ersten echten Inhalt entstehen. `class5-content.cjs` validiert jede Datei und erzeugt daraus Einstieg, Schritte, vollständige Einzelmaterialien, Wissen/Materialübersicht und Lehrpersonenhinweise. Ein fehlerhafter Lernbogen stoppt den Build.

Pflichtfelder: `area` (stabile URL-ID), `id` (IUM-5-…), `version` (SemVer), `grade:5`, `family:"content"`, `title`, `topic`, `description`, `product`, `prerequisites`, `teacher`, `steps`, `coverage`. Jeder Schritt hat `id,title,goal,criteria,blocks`. `coverage` verweist für entry/explanation/example/practice/application/revision/securing/transfer/retrieval auf vorhandene Schritt-IDs. Die Redaktion prüft zusätzlich die fachliche Qualität; vorhandene Felder beweisen keine Lernwirksamkeit.

Bekannte Blöcke: explanation, example, task, external, cooperative, private, retrieval. Alle tragen title/text, antwortende Blöcke zusätzlich id/prompt. Aufgaben können solution für einen bewusst geöffneten Vergleich enthalten.

- external: preparation, action, HTTPS-url, return. Der Link öffnet einen neuen Tab und kennzeichnet den Internetbedarf. Die Rückkehr verlangt ein eigenes Ergebnis. Eine Simulation wird nicht als erledigte Recherche ausgegeben.
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
