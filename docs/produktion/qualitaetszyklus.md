# Adaptiver Qualitätszyklus für alle Lernwerk-Inhalte

Stand: 04.10.2026 · Arbeitsstandard v1 · ab jetzt für die Inhaltsproduktion anzuwenden.

## Geltung
Gilt für alle Jahrgänge und für vollständige Lernbögen, offene Projekte, Recherche, Urteile, Kooperation, Programmierung, Simulation, persönliche Reflexion, Wissen und einzelne Materialien. Die Dateien-Referenz legt weder Schrittzahl noch Gerätewege, Medienwahl oder Aufgabenfolge anderer Inhalte fest.

Der aktuelle fachliche Produktionsvertrag bleibt maßgeblich. Technische Autorenverträge sind Ausgabeschnittstellen. Wenn sie eine erforderliche Lernhandlung nicht tragen, Entwicklungsbedarf sichtbar machen statt den Inhalt didaktisch zu verengen.

## Einstieg
Installierter Skill: $lernwerk-qualitaetszyklus.
Gemeinsame Quelle: Shared/Codex/Skills/lernwerk-qualitaetszyklus/ im AI-Workspace.
Dort liegen SKILL.md, Prüfraster, Bedienung/Protokoll, kontrastierende Prüffälle und das eigenständig ausführbare Node-Skript. Auf TIER unter %USERPROFILE%/.codex/skills/lernwerk-qualitaetszyklus/ installiert; andere Geräte müssen gezielt synchronisiert werden. Keine neue Abhängigkeit im Lernwerk.

## Ablauf
1. Auftrag und aktive Planungsfassung sichern; knapper Brief mit Zielgruppe, Zielen, Verwendung, Lernhandlung, Nachweis, Kontext und Grenzen.
2. Allgemeine Kriterien sowie passende Zusatzprofile wählen. Zu jeder Profilentscheidung einen knappen Grund; neue Anforderungen als eigene Kriterien ergänzen. Einzelmaterial im Nutzungskontext beurteilen.
3. Vereinbarten Inhalt mit abhängigen Ausgaben erzeugen und angemessen technisch prüfen.
4. Prüffassung samt relevanten Quellen, gemeinsamen Abhängigkeiten, erzeugten Seiten/Medien und Nachweisen erfassen. Vollständigkeit der Pfadauswahl fachlich prüfen.
5. Tatsächliche Ausgabe kritisch prüfen: fachlich, aus Lernendensicht und hinsichtlich Zugang/Material. Keine Pflichtzahl von Kritikpunkten.
6. Befunde gewichten, überarbeiten, erneut ausgeben und an neuer Prüffassung nachprüfen. Frühere Befunde erhalten; unbegründete Kritik belegt verwerfen.
7. Abschlussprüfung ausführen und mit Protokoll/kurzem Bericht übergeben. Höchstens zwei Nacharbeitsrunden; verbleibende Hindernisse konkret zur Entscheidung vorlegen.

## Abschlussprüfung
Aufruf: node quality-cycle.cjs init --run ABSOLUT/qa/run.json --id inhalt-id --scope ABSOLUT/quelle --scope ABSOLUT/ausgabe

Brief und Profile ausfüllen, anschließend mit review --run … --evidence ABSOLUT/testprotokoll.txt eine Prüffassung anlegen. Reviewurteile entstehen durch tatsächliche Prüfung, nicht durch das Skript. Nach Überarbeitung erneut review ausführen und aktuelle Nachweise angeben. Schließlich check --run … sowie report --run ….

Der Scriptpfad liegt im Skill unter scripts/quality-cycle.cjs. Kleine Prüfprotokolle können mit dem Projekt versioniert werden; technische Test-/Renderdateien außerhalb OneDrive in einem lokalen Work-Verzeichnis. Kein Protokoll innerhalb seines überwachten Inhaltsverzeichnisses.

READY_FOR_REVIEW (Exit 0): Pflichtprüfungen mit Evidenz, keine offenen Befunde ohne Entscheidung, aktuelle Fassungsbindung, notwendige Nachprüfung. BLOCKED (Exit 2): konkrete fehlende Voraussetzung. Nicht geprüfte redaktionelle Pflichten bleiben blockierend. Ausstehende reale Unterrichts-/Geräteerprobung wird separat ausgewiesen.

Die Prüfung ist ein verpflichtender Produktionsschritt, kein Hintergrunddienst oder automatischer Veröffentlichungsmechanismus. Sie prüft formale Konsistenz und Dateifassung, nicht die Wahrheit redaktioneller Aussagen. Ein fiktiver Testeintrag ist keine Evidenz.

## Anwendung in diesem Produktstand
Für neue Klasse-5-Inhalte insbesondere docs/produktion/klasse5.md, docs/klasse5-mantel-inhalte.md und aktive Curriculumplanung beachten. Andere Jahrgänge nutzen ihre eigenen Planungs-/Fachgrundlagen. Unterrichtsprofile und Medienproduktion nur passend zum Inhalt nachladen.

## Folgeauftrag
> Erstelle [beauftragten Inhalt] mit dem Lernwerk-Qualitätszyklus. Leite Struktur und Prüfprofil aus Ziel, Zielgruppe und Lernhandlung ab. Erstelle die benötigten Ausgaben, führe einen kritischen Selbstreview durch, überarbeite wesentliche Befunde und prüfe die Endfassung erneut. Liefere Inhalt/Vorschau, Fassungsprotokoll und kurzen Qualitätsbericht samt Grenzen. Arbeite inline; veröffentliche nicht automatisch.

## Validierungsgrenze
Die technische Abschlussprüfung ist mit positiven und negativen Fällen getestet. Die Allgemeinheit des Rasters wird an kontrastierenden synthetischen Beispielen selbst geprüft; eine unabhängige Evaluation und echte Unterrichtserprobung bleiben eigene Nachweise. Neue Inhaltstypen zunächst gezielt sichten und Erkenntnisse zurückführen.
