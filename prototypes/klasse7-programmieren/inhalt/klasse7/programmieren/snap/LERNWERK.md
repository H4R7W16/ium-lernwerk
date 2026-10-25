# Snap! · Lernwerk-Ansicht Klasse 7

Zusätzliche Erprobungsansicht vom 25.10.2026 für den vollständigen Programmierbogen ALG-1 bis ALG-6. Einstieg: [Lernwerk-Editor](lernwerk.html). Das vorbereitete Projekt wird über `?aufgabe=alg-1` bis `?aufgabe=alg-6` gewählt. Alte `#open:`-Adressen werden nur für diese sechs lokalen Startdateien akzeptiert.

## Herkunft und Quelltext

Die Kernlaufzeit Snap! 12.3.6 stammt aus dem [offiziellen Release](https://github.com/jmoenig/Snap/releases/tag/v12.3.6), siehe [ursprüngliche Herkunft und Änderungen](AENDERUNGEN.md), [Dateihashes](provenienz.json) und [AGPLv3-Lizenz](LICENSE). Sämtliche bisherigen Quelldateien unter src/, Sprache, Projekte und die bisherige index.html sind bei dieser Ergänzung unverändert.

Die ergänzenden Dateien sind vollständig lesbar veröffentlicht: [HTML](lernwerk.html), [Darstellung](lernwerk.css), [Konfigurationsmodell](lernwerk-modell.js), [Bedienung und Engineanbindung](lernwerk-editor.js). Sie werden zusammen mit dieser Snap!-Anpassung unter AGPL-3.0-or-later bereitgestellt. Ihr Dateimanifest steht in [lernwerk-herkunft.json](lernwerk-herkunft.json). Originalurheber von Snap!: Jens Mönig, Brian Harvey und weitere Beitragende; Ergänzung für das IuM-Lernwerk durch Jan/Codex.

## Bedienung und Grenzen

Helles flaches Design, größere Blöcke, vier Einstiegskategorien und große beschriftete HTML-Aktionen. Mehr Werkzeuge erweitert die Palette und zeigt native Menüs ohne Projektwechsel. Die ursprünglichen Blockfarben und deutschen Bezeichnungen bleiben erhalten. In schmaleren Ansichten werden die vorbereiteten Stapel beim ersten Laden untereinander angeordnet; Befehlsfolge und Verbindungen bleiben gleich. Importierte eigene Anordnungen werden erhalten. Der Auswahlfilter verändert keine Programmblöcke; beim XML-Export wird die ursprüngliche Sichtbarkeit der importierten Datei verwendet.

Starten ist die grüne Flagge. Lose Stapel aus ALG-1 benötigen weiterhin einen Stapeltipp. Der Schrittmodus verwendet Snap!s echte Auswertung und Pausen. Auch einzelne Ausdrücke können mehrere Auswertungsschritte brauchen. Es wird keine eigene Debugger- oder Rückwärtsschrittlogik simuliert. Angezeigte Position und Richtung stammen aus der aktuell ausgewählten Figur.

Datei speichern erzeugt einen XML-Download mit wählbarem Namen. Die Oberfläche sagt lediglich Download angefordert; sie bestätigt keine Ablage oder dauerhaft gespeicherte Datei. Änderungen werden nicht automatisch als neue Geräteablage gespeichert. Datei öffnen liest lokal, prüft vollständiges Projekt-XML und fragt vor dem Verwerfen geänderter Arbeit. Beschränkung dieser Ansicht auf XML-Dateien bis 10 MB.

Die Zusatzansicht ergänzt keine externe Schrift, Analyse, Cloudanmeldung oder zusätzliche Speicherung. Verbindungen bleiben durch dieselbe CSP auf den eigenen Ursprung begrenzt; der vorhandene Editor lädt selbst benötigte lokale Ressourcen. Dies ist kein beobachteter Nachweis eines vollständigen Offline- oder Datenschutztests. Keine Behauptung einer bestandenen Safari-Geräteprobe. Unter 840 Pixeln ist die Programmierfläche intern seitlich verschiebbar; primär Querformat auf dem iPad und Desktop. Die native Canvas-Fläche bleibt eine Einschränkung für assistive Zugänge.

Der bisherige Einstieg öffnet die vorbereitete Startdatei in einem neuen Tab. Zum Übertragen eigener Arbeit dort vorher die XML-Datei sichern und in der anderen Ansicht öffnen. Mehr Werkzeuge erhält das aktuelle Projekt direkt in dieser Ansicht.

[Zur bisherigen unveränderten Snap!-Ansicht](index.html) · [Zum Safari-Prüfauftrag](../lehrpersonen/safari-test.html)
