# Am IuM-Lernwerk mitarbeiten

Der aktuelle öffentliche Stand umfasst Klasse 5–7. Beginnen Sie bei der [README](README.md), dem [Projektstand](docs/projektstand.md) und den [Projektregeln](AGENTS.md).

## Den passenden Quellort wählen

Die [Pages-Dokumentation](prototypes/pages/README.md) ordnet Generatoren und Quellen zu. Die Website wird aus mehreren gebundenen Inhaltsständen zusammengesetzt. Dateien in `dist/` sind Ausgaben; dort vorgenommene Änderungen gehen beim nächsten Build verloren.

Für Klasse 7 liegen redaktionelle Ausgangstexte im projektinternen Obsidian-Workspace. Der gemeinsame Ausgangsbereich ist dort Vault/40_Projekte/IuM-Lernwerk/Klasse 7/; die Renderquellen liegen unter Shared/Scripts/Build-IuM7-*.mjs. Die Zuordnung ist beispielsweise im [Jahrgangsadapter](prototypes/klasse7-jahrgang/README.md) beschrieben. Bei den einzelnen Lernbögen zusätzlich das jeweilige Herkunftsmanifest und den zugehörigen Renderweg im Workspace prüfen; deren ältere READMEs dokumentieren diesen Weg noch nicht durchgängig. Ohne Zugriff auf diesen Workspace eine Korrektur als Vorschlag mit genauer Fundstelle einreichen; veröffentlichte HTML-Dateien und SHA-Manifeste nicht unabhängig von ihrer Quelle umschreiben. Die Dokumentation und die im Repo enthaltenen Generatoren lassen sich unmittelbar im Repository bearbeiten.

Substanzielle Inhaltsänderungen durchlaufen den [Qualitätszyklus](docs/produktion/qualitaetszyklus.md): tatsächliche Ausgabe prüfen, Befunde nacharbeiten und die geänderte Fassung erneut prüfen. Betroffene Durchführungshinweise, Briefings, Materiallinks und Zeitangaben gleichzeitig nachführen. Ein grüner technischer Test ersetzt keinen Inhaltsreview.

## Lokal bauen und ansehen

Für die aktuelle Pages-Ausgabe genügt Node.js 22 (`>=22.12.0 <23`, siehe [package.json](package.json)). Sie nutzt Node-Bordmittel und braucht kein `npm ci`.

```powershell
node prototypes/pages/build.cjs dist/vorschau-1
python -m http.server 4173 --bind 127.0.0.1 --directory dist/vorschau-1
```

Öffnen Sie anschließend `http://127.0.0.1:4173/klasse5/`, `/klasse6/` oder `/klasse7/`. Beim nächsten Build ein neues Ziel wie `dist/vorschau-2` verwenden und den Server auf dieses Verzeichnis richten. Der Build lehnt bereits existierende Ziele ab.

Für Arbeiten am älteren Plattformfundament unter `apps/` und `packages/` gelten zusätzlich npm 10 und `npm ci`, danach die Befehle in [package.json](package.json) und der [Plattformdokumentation](docs/platform/README.md). `npm run build` erzeugt nicht die aktuelle Pages-Website.

Entwicklungsordner, Abhängigkeiten, Caches und Builds außerhalb synchronisierter Cloudordner halten. Im betreuten AI-Workspace ist dafür `AI-Workspace-Local` vorgesehen; das gemeinsame Geräteprofil bestimmt den konkreten Arbeitsort.

## Passend zur Änderung prüfen

Die vollständige bestehende Pages-Prüfkette aus dem [Veröffentlichungsworkflow](.github/workflows/klasse5-pages.yml) lautet:

```powershell
node --test prototypes/shared/*.test.cjs prototypes/m06-reinigungsfall/pages-build.test.cjs prototypes/m06-reinigungsfall/class5-pages.test.cjs prototypes/recherche-beispiel/pages.test.cjs prototypes/pages/pages.test.cjs prototypes/pages/grade-navigation.test.cjs prototypes/klasse7-programmieren/*.test.cjs prototypes/klasse7-medien/*.test.cjs prototypes/klasse7-daten/*.test.cjs prototypes/klasse7-gaming/*.test.cjs prototypes/klasse7-jahrgang/*.test.cjs prototypes/m01-netze/*.test.cjs prototypes/m05-zeichnen/*.test.cjs
```

Zusätzlich den vollständigen Build ausführen und betroffene Seiten im Browser ansehen. Bei UI-Änderungen auch schmale Ansicht, Tastaturbedienung und Rückwege prüfen. SHA-Bindungen nur zusammen mit bewusst geänderten Quellen und deren Nachprüfung aktualisieren.

Bei Änderungen an historischen README-/Pilotabschnitten auch die bestehenden Publikationsverträge prüfen:

```powershell
python -B scripts/build_ium11_publication_contract.py --check
python -B scripts/validate_ium11.py
python -B -m unittest discover -s tests -p "test_*.py"
```

Die [Repository-CI](.github/workflows/ci.yml) prüft außerdem Plattformverträge, Build, Browser, Offlineverhalten und Zugänglichkeit des Plattformfundaments. Seit PR 54 laufen dort bereits vor dem Merge auch die Veröffentlichungsverträge für die Klasse-7-Bögen Medien, Daten und Gaming; die vollständige Pages-Prüfkette bleibt zusätzlich erforderlich. Eine erfolgreiche Plattform-CI ist allein kein Nachweis für eine geänderte aktuelle Lernseite.

## Änderungen integrieren

1. Mit `git status --short --branch` beginnen. Bei paralleler Arbeit einen eigenen Branch und Arbeitsbaum verwenden.
2. Vor Commit und Push `git fetch --prune` und `git pull --ff-only` ausführen. Bei Konflikten oder Authentifizierungsfehlern zunächst den Synchronisationsstand klären.
3. Nur die zum Auftrag gehörenden Quelldateien committen. Keine Builds, `node_modules`, lokalen Runtime-Dateien, Secrets oder personenbezogenen Lernprodukte aufnehmen.
4. Einen Pull Request mit Anlass, tatsächlicher Änderung und Prüfergebnis erstellen. Der Merge nach `main` startet den Pages-Workflow; deshalb vor dem Merge die Veröffentlichung des konkreten Umfangs klären.
5. CI, Pages-Deployment und betroffene öffentliche Wege nach der Integration prüfen. Commit, Branch und Ergebnis nachvollziehbar dokumentieren.

Die [Inhaltslizenz](LICENSE-CONTENT.md), [Codelizenz](LICENSE) und abweichende Lizenzen Dritter gelten weiterhin. Quellen und Unsicherheiten kenntlich machen; keine Lernwirkung oder reale Geräteprüfung aus automatisierten Tests ableiten.
