# Gemeinsame Pages-Ausgabe für Klasse 5–7

Stand der Dokumentation: 06.11.2026. `build.cjs` ist der Veröffentlichungsweg des aktuellen Lernwerks. Der historisch beibehaltene Workflowname `klasse5-pages.yml` und das Standardziel `dist/klasse5-pages` umfassen heute alle drei Jahrgänge und das zusätzliche Recherche-Beispiel.

## Bauen

```powershell
node prototypes/pages/build.cjs
```

Der Build nutzt Node.js 22 ohne externe Pakete. Das Ziel darf noch nicht existieren; für eine weitere Vorschau einen neuen Pfad übergeben:

```powershell
node prototypes/pages/build.cjs dist/vorschau-2
python -m http.server 4173 --bind 127.0.0.1 --directory dist/vorschau-2
```

Die Einstiege liegen unter `/klasse5/`, `/klasse6/` und `/klasse7/`. Klasse 7 öffnet die gemeinsame Jahrgangsübersicht. Der zusätzliche Recherche-Referenzstand liegt unter `/beispiele/recherche/`.

## Tatsächliche Buildkette

| Stufe | Aufgabe |
| --- | --- |
| `preparePages()` | Bestehende Klasse-5-Ausgabe und Recherche-Beispiel übernehmen, Klasse 6 ergänzen, die vier Klasse-7-Adapter für Programmieren, Medien, Daten und Gaming einfügen. Bestandshashes, zulässige Pfade und lokale Verweise prüfen. |
| `prepareNavigablePages()` | Reihenlayout für Programmieren anwenden, die vier Klasse-7-Bögen verbinden und gemeinsame Jahreswege einschließlich Kopfzeile, Aufgaben- und Materialwegen ergänzen. |
| `preparePublishedPages()` | Klassenwahl, Gesamtkonzept 5–7, Themenorientierung und gerätebezogene Arbeitsstellen auf die vollständige Ausgabe anwenden. |
| `build(output)` | Die fertige Dateimenge in ein neues Ausgabeziel schreiben. |

`preparePages()` ist eine Zwischenstufe für Inhaltsbindungen. Für die tatsächlich veröffentlichte Website `preparePublishedPages()` beziehungsweise `build()` verwenden.

## Quellen und Zuständigkeiten

| Bereich | Quellen / Adapter |
| --- | --- |
| Klasse-5-Grundausgabe und gemeinsamer Lernwerkmantel | [m06-reinigungsfall](../m06-reinigungsfall/) und [shared](../shared/) |
| Klasse-6-Inhalte und Jahreswege | [class6-render.cjs](../shared/class6-render.cjs), weitere `class6-*`-Dateien in `shared/`, [Netze](../m01-netze/) und [Zeichnen](../m05-zeichnen/) |
| Klasse-7-Lernbögen und deren Herkunft | [Programmieren](../klasse7-programmieren/README.md), [Medien](../klasse7-medien/README.md), [Daten](../klasse7-daten/README.md), [Gaming](../klasse7-gaming/README.md) |
| Klasse-7-Jahreseinstieg, Diagnose, Wiederaufnahme und Kopfzeile | [Jahrgangsadapter](../klasse7-jahrgang/README.md) |
| Klassenwahl, Themenwege, Gesamtkonzept und iPad-/Windows-Arbeitsstellen | [shared](../shared/), insbesondere `grade-navigation.cjs`, `themen-navigation.cjs`, `gesamtkonzept.cjs`, `gesamtkonzept.json` und `arbeitsstellen.cjs` |
| Zusätzliches eingefrorenes Recherche-Beispiel | [recherche-beispiel](../recherche-beispiel/README.md) |

Klasse-7-Adapter enthalten synchronisierte Quelltexte, HTML-Lesefassungen und SHA-256-Herkunftsbindungen. Die redaktionellen Ausgangsquellen liegen im AI-Workspace unter Vault/40_Projekte/IuM-Lernwerk/Klasse 7/, die Renderquellen unter Shared/Scripts/Build-IuM7-*.mjs. Der [Jahrgangsadapter](../klasse7-jahrgang/README.md) dokumentiert seinen Weg ausdrücklich; die älteren READMEs der einzelnen Lernbögen beschreiben ihn noch nicht durchgängig. Vor einer inhaltlichen Änderung zusätzlich das jeweilige Herkunftsmanifest und den Renderweg im Workspace abgleichen. Nicht erst in der fertigen Website korrigieren.

## Erhaltungs- und Prüfregeln

- `bestand-sha256.json` und die datierten Revisionsmanifeste binden den geprüften Ausgangsbestand. Neue Revisionen müssen die beabsichtigten Abweichungen nachvollziehbar festhalten.
- Die ursprüngliche Snap!-Engine und Projektdateien behalten ihre Herkunftsbindung. Änderungen an der eigenen Editorhülle werden gesondert nachgewiesen.
- Das zusätzliche Recherche-Beispiel behält seinen Referenzstand; allgemeine Anpassungen der aktuellen Jahrgänge dürfen es nicht versehentlich verändern.
- Die gemeinsamen Ausgabestufen pflegen die Versionen und Dateilisten der Klasse-5/6-Offlinepakete. Ein Klassenwechsel stellt nicht automatisch einen anderen Jahrgang offline bereit.
- Interne Quellenpfade, QA-Logs, Laufzeitdateien und private lokale Adressen gehören nicht in die Website.

`pages.test.cjs` prüft die gebundene Zusammensetzung; `grade-navigation.test.cjs` prüft unter anderem Jahrgangsziele, relative Verweise, erhaltene Inhalte, Offline-Assets und Herkunftsmanifeste. Dazu kommen die Tests der gemeinsamen Ausgabestufen und der einzelnen Inhaltsadapter. Die vollständige Prüfkette steht in [CONTRIBUTING.md](../../CONTRIBUTING.md) und im [Pages-Workflow](../../.github/workflows/klasse5-pages.yml).

## Veröffentlichung

Der Workflow **IuM Lernwerk Pages** baut und veröffentlicht auf `main`. Er führt zuerst die Inhaltsprüfungen aus und lädt dann die komplette statische Ausgabe als Pages-Artefakt hoch. Frühere Pages-Workflows bleiben als historische Prüfpfade erhalten und sind als Veröffentlichungswege stillgelegt.

Die [allgemeine CI](../../.github/workflows/ci.yml) prüft zusätzlich das frühere Plattformfundament und seit PR 54 die drei Klasse-7-Veröffentlichungsverträge für Medien, Daten und Gaming bereits vor dem Merge. Dessen `npm run build` ist ein eigener Buildweg und ersetzt diese Pages-Ausgabe nicht.
