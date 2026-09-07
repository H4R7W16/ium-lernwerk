# R5-M06 – Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans`. Steps use checkbox (`- [ ]`) syntax. Sequenzielle Ausführung; keine Subagenten ohne ausdrücklichen Nutzerauftrag. Dies ist ein Plan zur Abnahme, kein Ausführungsauftrag.

**Goal:** Einen lokal prüfbaren V2-Entwicklungskandidaten für R5-M06 mit geschütztem Arbeitsstand, eigenem ausführbarem Code, vollständigen Materialien und den angenommenen Prüfinstrumenten herstellen.

**Architecture:** Acht abhängige Pakete: additive Entwicklungssteuerung → Runtimeannahme/Recovery → revisionsgeprüfter Speicher und bewusste Speicherwahl → verlustgeschütztes Update → neutraler M06-Fachkern → Materialien → Entwicklungsauslieferung/Oberfläche → integrierte Prüfung. V1-Inhalte und historische V2-Entscheidungen behalten ihre Identität; der neue Kandidat erhält eigene Modul-, Speicher- und Buildkennung.

**Tech Stack:** Bestehender Lockfile-Stand: TypeScript 6.0.3, Astro 7.1.6, Vitest 4.1.10, Playwright 1.62.1, `idb`, `fake-indexeddb` 6.2.5, JSON Schema/Ajv und Python-Standardbibliothek. Node 22.23.2/npm 10.9.8 sind lokal geprüft; `engines` bleibt `>=22.12.0 <23` / `>=10.9.0 <11`. Keine neue externe Laufzeitbibliothek vorgesehen.

**Spec:** [Angenommenes Moduldesign](../specs/2026-09-07-ium-v2-g5-m06-referenzmodul-design.md), [MOD-Bindung](../../../roadmap/v2/follow-ups/reference-module/specification.json), [TECH-Befunde](../../../roadmap/v2/follow-ups/technical/findings.md), [angenommener PILOT-Vertrag](../../../roadmap/v2/follow-ups/pilot/design.md) einschließlich seiner verlinkten Instrumente. MOD an `9365045a2c2a50d2259d01ef172b7b292cd0ee24`, PILOT an `150deea22ba9bcf3170915bb4b24852d376f6a8b`; Annahmen jeweils additive `acceptance.json`.

## Global Constraints

- Dieser Auftrag erstellt den Plan. Erst tatsächliche Planannahme und konkreter Umsetzungsauftrag aktivieren die betroffenen Pakete. Keine Ausführung aus der Annahme eines alten V1-Plans ableiten.
- „Alle sieben M06-Curriculumrecords bleiben `unassessed`“; kein automatisches Coverage-, Lernwirkungs-, Geräte- oder Pilotlabel.
- „P1, P2, P3, P5 und P6 bilden das begrenzte Dossier.“ P0/P4 nur flüchtige aktuelle Diagnose. Keine Klick-/Zeit-/Hilfe-/Versuchshistorie, Namen, Klassenkennung oder private Mediennutzung speichern.
- Fünf Termine à 45 Minuten; O35/G55/I60/F40/S35 = 225. Keine elf Pflichtphasen oder 270-Minuten-Erweiterung. Erwachsenenorganisation aus PILOT separat.
- Feste nicht verschachtelte Schleifen; Anzahlen 2–9, Körper 1–5 Grundanweisungen, Ausführung höchstens 100 Aktionen. M06-Befehle nur Bewegung/Links-/Rechtsdrehung. S4 ist manueller Transfer, keine neue Programmierumgebung.
- V2 ist Planungs-/Entwicklungsbaseline, V1 bestehender Produktstand. Kandidat nur lokal; `pilot: not-started`, `publication: closed`. Keine Übernahme von LXP05, keine echten Daten/Schülerprodukte, kein Hosting, Push oder Merge.
- Technische Probes bestätigen keine reale Zielprüfung. Echte Schule, Betreiber, Reviewer, Rechte, Zugänge und Termine bleiben Bedingungen vor tatsächlichem Einsatz.
- Bestehende Siegel nicht neu berechnen, um Veränderungen zu kaschieren. Paket-/Dashboardänderungen sind erst nach IMP01 im neuen Entwicklungsvertrag zulässig.
- Vor jedem Paket Status und autorisierten Umfang prüfen; vor jedem Commit Fetch/Prune, danach Pull/ff-only. Keine History-Rewrites. Reversible Code-/Dokumentarbeit wird innerhalb eines autorisierten Pakets ohne Zwischenfreigabe erledigt.

## Lesepfad und Ausführung

Dieser Hauptplan enthält IMP01 und IMP08 sowie übergreifende Verträge. [Runtimeplan](2026-09-07-ium-v2-runtime-implementation.md) enthält IMP02–04, [Modulplan](2026-09-07-ium-v2-m06-implementation.md) IMP05–07. Vor Ausführung jedes Teilplans Hauptplan und die oben genannten Specs lesen; keine Planfragmente ohne globale Grenzen ausführen.

| Paket | Ergebnis / Abhängigkeit | Modellvorschlag für spätere Ausführung |
| --- | --- | --- |
| IMP01 | Historische Aktivierung und veränderbare Entwicklung unterscheiden; aktuelle FU-Projektion. Ausgangspunkt. | GPT-6 Astra · Hoch |
| IMP02 | Einheitliche Datenannahme, Original-Recovery und aktueller Importkandidat. Nach IMP01. | GPT-5.6 Sol · Hoch |
| IMP03 | Atomarer Revisions-/Löschschutz, Speicherwahl, bewusster Export. Nach IMP02. | GPT-5.6 Sol · Hoch |
| IMP04 | Update nur nach nachgewiesener Wiederherstellbarkeit aller betroffenen Clients. Nach IMP03. | GPT-5.6 Sol · Hoch |
| IMP05 | Neutraler Fachkern, S0–S5 und begrenztes Dossier. Nach IMP04. | GPT-5.6 Sol · Hoch |
| IMP06 | MAT-01–10, Hilfen, Lehrkrafthandbuch, lesbares Briefing und gleichwertige Text-/Printfassung. Nach IMP05. | GPT-5.6 Sol · Hoch |
| IMP07 | Eigene V2-Registry/Route und vollständiger zugänglicher Lernweg. Nach IMP06. | GPT-5.6 Sol · Hoch |
| IMP08 | Toolchain, vollständige synthetische Prüfung, Pilotübergabe und ehrlicher Entwicklungsstatus. Nach IMP07. | Sol · Hoch; abschließender Gesamt-/Didaktikreview Astra · Extra hoch |

Die Vorschläge ändern keine Modelleinstellung. Inline-Ausführung ist geeignet, weil die Pakete dieselben Verträge und Builds nacheinander verändern. Keine automatische Parallelisierung/Ultra-Ausführung. Je Paket ein nachvollziehbarer Reviewabschluss; bei mehreren Sessions bleibt das Paket `in_progress`, bis seine Kriterien tatsächlich erfüllt sind.

## Neue technische Planentscheidungen

Diese Entscheidungen konkretisieren MOD/TECH und stehen mit dem Plan zur Annahme. Sie sind nicht als bereits implementierte Eigenschaften zu lesen.

1. **Entwicklungsnachfolger der Aktivierung:** Das alte Aktivierungspaket bleibt unverändert historisch prüfbar. Ein neuer Entwicklungsvalidator vergleicht geschützte aktuelle Inhalte mit dem angenommenen Eingang und erlaubt nur planbezogene Entwicklungsdateien. Der genehmigte konkrete Umsetzungsumfang wird additiv protokolliert.
2. **Runtime:** Gemeinsamer Datenannahmepfad für Laden/Import, explizite Initialpayload und Modulversions-Support. M06 beginnt bei Modulversion `0.1.0`, Zustandschema `1`; keine V1→M06-Payloadmigration.
3. **Speicher:** Eigene Datenbank `ium-lernwerk-v2`, Version 1, ein ausdrücklich gemeinsamer anonymer Browserprofilslot je Modul. Atomare Revision plus globale Löschgeneration. Keine Identität/Vertraulichkeit innerhalb eines gemeinsam verwendeten Browserprofils behaupten; dort bevorzugt flüchtig oder schulisch getrennte Profile.
4. **Export/Update:** Download-Anstoß ist kein Nachweis einer wiederherstellbaren Datei. Kein automatisches Clipboard. Flüchtige oder nicht sicher speicherbare Arbeit blockiert das Update; bewusster Verzicht auf diesen Stand ist eine eigene sichtbare Handlung und gilt nur für die aktuelle Bearbeitungsrevision.
5. **Fachkern:** Neues `@ium/v2-g5-m06` ohne DOM/Framework und ohne Import des alten Lieferrobotermodells. Fachsemantik selektiv in kleine reine Funktionen übertragen; V1-Körperlimit und Payload bleiben erhalten.
6. **Kandidatenbuild:** Neues Profil `v2-development`, ausschließlich Veröffentlichungsmodus `development`, eigener Renderer `v2-m06`. `production`/`fixture` behalten ihren Inhalt. Kein V2-Kandidat im V1-Produktkatalog; kein neuer Deploymentworkflow.
7. **Dossier:** Eigene editierbare Ablaufgrafik wird getrennt vom Code geführt; eine automatisch gerenderte Codeliste allein belegt P1/P3 nicht. Gespeichert werden begrenzte, aktuelle Produkte und ausgewählte Spuren mit Codebindung, keine Bearbeitungshistorie.

## IMP01 – Entwicklungsvertrag und aktuelle Projektsteuerung

**Files – Create:**

- `roadmap/v2/implementation/authorization.json` – ausschließlich tatsächliche Nutzerentscheidungen und beauftragte Pakete, bei Folgeaufträgen additiv fortschreiben.
- `roadmap/v2/implementation/progress.json` – aktuelle Paketzustände mit Prüf-/Abnahmebezügen.
- `roadmap/v2/implementation/change-plan.json` – exakte Paket-/Datei-/Abhängigkeitsliste und Referenzen auf diesen Plan; keine reale Freigabe.
- `schemas/v2/implementation.schema.json` – geschlossener Nachfolgevertrag.
- `scripts/validate_v2_implementation.py` – aktuelle Entwicklung gegen angenommene Baseline und tatsächlichen Umsetzungsauftrag prüfen.
- `tests/test_validate_v2_implementation.py` – Eingabe-, Drift-, Pfad- und Freigabefehler.
- `tests/dashboard/implementation.test.mjs` – aktuelle FU-Annahmen, Entwicklungsfortschritt, historische Nachweise.

**Files – Modify:** `packages/project-status/index.mjs`, `scripts/project-dashboard.mjs`, `tests/dashboard/contract.test.mjs`, `tests/dashboard/snapshot.test.mjs`, `tests/test_validate_v2_activation.py`, `package.json`. Nur falls Darstellung neuer getrennt typisierter Felder dies erfordert: `apps/project-dashboard/src/pages/[...page].astro`. Nicht pauschal alle 108 Aktivierungsinputs zur Änderung freigeben.

**Schnittstelle / Eingaben:** Aktuelles `active-baseline.json` nennt **108** versiegelte Eingaben; darunter `package.json`, `package-lock.json`, Dashboardleser/-tests, historische Validatoren und Grundlagen. Das alte `validate_v2_activation.validate(ROOT)` prüft diese gegen die aktuelle Arbeitskopie. Deshalb darf IMP02 nicht mit Paketänderungen anfangen, bevor der Nachfolger funktioniert.

Neue öffentliche Python-Schnittstellen: `ImplementationError(ValueError)` als eigene Fehlerklasse; `validate_change_plan(plan: dict, *, allowed_files: set[str]) -> dict` liefert die geprüfte Paketbeschreibung; `validate(repo: Path, *, authorization: dict | None = None, vault: Path | None = None) -> dict` liefert getrennte Felder `historicalActivation` und `development`. Paketbeschreibung hat exakt `schemaVersion`, `packageId`, `files`, `dependsOn`. Der umfassende Changeplan enthält eine Liste solcher Beschreibungen plus Plan-/Eingabebindungen; Schema und Validator prüfen beide Ebenen. Keine leeren Funktionskörper committen. `authorization.json` und `progress.json` gehören bei jedem Paket zur begrenzten Statuspflege; historische Nutzerentscheidungen dürfen nicht ersetzt werden. Der Validator prüft Konsistenz und Bindung, keine kryptografische Echtheit eines Gesprächs: Autorenschaft und Wortlaut müssen auf den tatsächlichen Nutzerauftrag zurückgehen.

- [ ] **1. Auftrag festhalten und roten Vertragstest schreiben.** Vor tatsächlicher Implementierung `roadmap/v2/implementation/authorization.json` additiv mit Nutzerwortlaut, Datum, angenommenem Plancommit und ausdrücklich beauftragten Paket-IDs anlegen. Kein `approved` aus dieser Planerstellung. Beispiel für den reinen Pfadvalidator, mit vollständiger Fixture in derselben Testdatei:

```python
import unittest
from validate_v2_implementation import validate_change_plan, ImplementationError

class PlanTests(unittest.TestCase):
    def test_no_path_escape_or_foundation_reseal(self):
        plan = {"schemaVersion": 1, "packageId": "IMP01",
                "files": ["../secret"], "dependsOn": []}
        with self.assertRaises(ImplementationError):
            validate_change_plan(plan, allowed_files={"package.json"})
        plan["files"] = ["roadmap/v2/cutover/active-baseline.json"]
        with self.assertRaises(ImplementationError):
            validate_change_plan(plan, allowed_files={"package.json"})
```

Run: `python -B -m unittest discover -s tests -p test_validate_v2_implementation.py`. Erwartet zunächst fehlendes neues Modul, danach Ablehnung beider verbotenen Pfade.

- [ ] **2. Historie prüfbar erhalten.** `git show <angenommener-Plancommit>:<plan>` und die drei FU-Annahmen gegen exakte Commit-/Dateibindungen prüfen; verkürzte SHA, nicht vorhandene Commitobjekte und abweichende Annahmen ablehnen. Historische Aktivierung an `150deea22ba9bcf3170915bb4b24852d376f6a8b` validieren: historische Dateiinhalte einschließlich dortiger Validatoren aus Git in eine isolierte temporäre Dateisicht materialisieren. Mitgliedspfade gegen Traversal prüfen; keine aktuelle uncommittete Datei hineinmischen. `git`-Abfragen bleiben am echten Repo; ein Archiv allein hat keine Commitdatenbank. Die historischen Python-Module in einem separaten Prozess aus dieser Dateisicht laden, ihre `git(repo, *args)`-Helfer in `validate_v2_cutover` und `validate_v2_activation` auf einen read-only Runner mit `cwd` des echten Repos binden. `ROOT`/Dateilesen bleiben in der historischen Sicht. Originalquellen und Siegel werden nicht editiert. Positivtest mit echten Commitobjekten; Negativtest verändert nur die Test-Dateisicht und muss historische Validierung scheitern lassen. Die zugelassene Git-Befehlsmenge im Runner auf `show`, `rev-parse` und `merge-base` begrenzen.
- [ ] **3. Aktuelle Änderungsliste prüfen.** `git diff --name-status <authorization.acceptedPlanCommit>` plus untracked-Dateien erfassen. Neue/alte Pfade jeder Umbenennung prüfen; Löschungen geschützter Dateien ablehnen. Nur die exakten Dateien der beauftragten Pakete zulassen, keine breite `roadmap/**`-Ausnahme. Die [vollständige Dateiliste](../../../roadmap/v2/implementation-planning/plan.json) wird einmalig in `change-plan.json` übertragen; optionale Pfade bleiben an ihre dortigen Gründe gebunden. Der Nachfolger schützt außerdem alle Dateien des angenommenen Planungspakets. Änderungen am Plan benötigen eine eigene dokumentierte Entscheidung und neue Bindung. Unveränderliche CUR/SRC/LXF/GOV/R5–7/AUD/CUT- und angenommene FU-Inputs gegen ihre historischen Hashes vergleichen; aktuelle Entwicklungsnachweise separat binden. CRLF/LF wie bisher nur beim dokumentierten Vergleich normalisieren. Codekern:

```python
from pathlib import PurePosixPath

def checked_path(value: str, allowed: set[str]) -> str:
    path = PurePosixPath(value)
    if (not value or "\\" in value or ":" in value or path.is_absolute()
            or any(part in {"", ".", ".."} for part in value.split("/"))
            or value not in allowed):
        raise ImplementationError("Nicht autorisierter Entwicklungspfad")
    return value
```

- [ ] **4. Nachweis und Erlaubnis unterscheiden.** `development.packages` darf `planned|in_progress|review|done` berichten, jeweils mit tatsächlichem Commit/Prüfbezug; `done` verlangt passende Abnahme. `historicalActivation.productBaseline` bleibt `v1`. Zulässige Kandidatenimplementierung ist kein globales `contentProduction: open`. Konkrete Materialproduktion nur im autorisierten IMP06/07. `usage`, `pilot`, `release`, `curriculum` bleiben geschlossen/unassessed. Der Validator schreibt keine Freigaben. Negative Tests: gefälschte Autorenschaft, Zukunftscommit, fremdes Paket, gelöschte Foundation, veränderter Plan, erfülltes Pilotlabel, geschönte TECH-Evidenz.
- [ ] **5. Aktuellen Statusleser anbinden.** Wenn gültige Entwicklungsautorisierung vorliegt, neuen Validator verwenden; ohne diese bleibt der bestehende Aktivierungsweg maßgeblich. Die FU-Liste aus dem unveränderten AUD lesen, Status ausschließlich aus exakt passenden additiven Annahmen bzw. aktuellen Task-/Reviewbelegen ableiten. Widersprüche → Fehler/ungeklärt, nie stillschweigend `done`. Alter globaler technischer Nachweis bleibt historisch; Entwicklungsprüfungen eigenes Feld. Testkern:

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { resolveFollowUpState } from '../../packages/project-status/index.mjs';

test('an accepted instrument is not a completed real pilot', () => {
  const result = resolveFollowUpState({
    taskId: 'IUM-V2-FU-PILOT', state: 'approved-by-user',
    scope: 'pilot-instrument-specification',
    acceptedCommit: '150deea22ba9bcf3170915bb4b24852d376f6a8b',
    pilot: 'not-started', publication: 'closed'
  });
  assert.equal(result.workStatus, 'done');
  assert.equal(result.pilot, 'not-started');
});
```

`resolveFollowUpState(acceptance)` erhält erst nach vorgelagerter Identitäts-/Commitprüfung einen typisierten Datensatz und liefert `{workStatus, pilot, publication}`. Unbekannte Scopes/Statuswerte direkt ablehnen. Dashboardtests und den vorhandenen Aktivierungstest so aufteilen, dass **historische** Negativfälle weiterhin gegen den historischen Snapshot prüfen und die aktuelle Entwicklung zusätzlich durch neue Negativtests abgesichert ist. Alte Tests nicht durch bloßes Entfernen von Assertions „reparieren“.
- [ ] **6. Prüfen und committen.** `python -B -m unittest discover -s tests -p 'test_validate_v2_*.py'`, `npm run test:dashboard`, neue CLI `python -B scripts/validate_v2_implementation.py --vault ../../Vault`, `npm run dashboard:update`. Testfälle müssen auch ohne Vault in CI funktionieren; reale Eintrittsbedingungen ohne Vault bleiben unbestätigt. Staged Diff prüfen, Fetch/Pull, Commit `feat: add controlled V2 implementation contract`. Abschlussbeleg nennt historische und aktuelle Prüfungen getrennt.

**Abschluss IMP01:** Neue Entwicklung kann bestehende Paket-/Dashboarddateien ändern, während jede unautorisierte Foundationänderung scheitert. FU-TECH/MOD/PILOT werden im aktuellen HTML korrekt als angenommene Planungsaufträge dargestellt. Dieses Paket löst nicht die Runtimebefunde.

## IMP08 – Integration, Toolchain und Pilotübergabe

**Files – Create:** `scripts/verify-v2-m06.ts`, `playwright.v2.config.mts`, `tests/browser/v2-m06-workbench.spec.ts`, `tests/browser/v2-m06-state.spec.ts`, `tests/browser/v2-m06-accessibility.spec.ts`, `tests/browser/v2-m06-offline.spec.ts`, `docs/reviews/v2-m06-technical.md`, `docs/reviews/v2-m06-didactic.md`, `roadmap/v2/implementation/evidence.json`.

**Files – Modify:** `package.json`, `.github/workflows/ci.yml`, `tests/platform/pages-workflow.test.ts`, `tests/platform/pwa-contract.test.ts`; bei tatsächlich reproduziertem Runnerproblem `playwright.config.mts` und `playwright.ium5.config.mts` gezielt. Keine Änderung von Publishworkflows oder Neuinstallation beliebiger Browser-/Paketversionen auf Verdacht.

**Schnittstellen:** Konsumiert Kandidatenbuild und `connectM06` aus IMP07, Fachverträge IMP05, Storage/Update IMP02–04 sowie [elf reale TECH-Prüfaufträge](../../../roadmap/v2/follow-ups/pilot/technical-runbook.md). Erzeugt maschinenlesbare **synthetische** Ergebnisse pro Build/Prüfpfad und einen leeren Realprüf-Handoff. `evidence.json` enthält Commit, Builddigest, Toolversionen, Testkommando, Exitcode, tatsächliche Summen und Grenzen; keine echten Unterrichtsdaten.

- [ ] **1. Vollständigen Gegenbeispiel-Browsertest schreiben.** Browserfixtures ausschließlich synthetisch. Beispiel in der neuen V2-Konfiguration, `use.baseURL` aus dem lokal gestarteten `preview:v2` auf Port 4324:

```ts
import { test, expect } from '@playwright/test';

test('P4 is not restored from the dossier and P3 remains editable', async ({ page }) => {
  await page.goto('/module/v2-g5-m06/');
  await page.getByRole('button', { name: 'Auf diesem Gerät speichern' }).click();
  await page.getByRole('button', { name: 'Abruf öffnen' }).click();
  await page.getByLabel('Deine Abrufbegründung').fill('SYNTHETIC-P4-SENTINEL');
  await page.getByRole('button', { name: 'Zum eigenen Entwurf' }).click();
  await page.getByLabel('Begründung der Prüffahrt').fill('SYNTHETIC-P3-SENTINEL');
  await page.getByRole('button', { name: 'Arbeitsstand speichern' }).click();
  await page.reload();
  await page.getByRole('button', { name: 'Auf diesem Gerät speichern' }).click();
  await expect(page.getByLabel('Begründung der Prüffahrt')).toHaveValue('SYNTHETIC-P3-SENTINEL');
  await page.getByRole('button', { name: 'Abruf öffnen' }).click();
  await expect(page.getByLabel('Deine Abrufbegründung')).toHaveValue('');
});
```

Diese zugänglichen Labels sind Teil des IMP07-Vertrags. Zusätzlich Storageinhalt und Export auf P0/P4-Sentinel prüfen, nicht nur die UI. Test scheitert zunächst vor vorhandener Oberfläche; kein künstlich grünes Mock der Kerninteraktion.
- [ ] **2. End-to-end-Matrix aufbauen.** S0–S3 inklusive fünfteiliger Schleife, selbst bearbeiteter Grafik und ausgewählter Spur; S2 Ursache 2/Fehler 3; leeres S3-Programm trotz gleichem Endzustand; S4/S5-Materialanker; alte/falsche/defekte Importdatei; A-Preview→B-Fehler; Recovery; zwei Seiten derselben Origin mit CAS/Löschen; getrennte Browserprofile als andere Datenräume; Speicherwahl; Quota/blocked IndexedDB; bewusster Export/Clipboard; Offline/fehlender Cache; Updateveto/Promise-Rejection/zwei Clients. Tests gegen reale Browseroperationen, keine Quelltextsuche als Ersatz.
- [ ] **3. Firefox-/WebKit-Befunde eingrenzen.** Mit gepinntem Node/Lockfile leeres Firefox-`newPage` reproduzieren. Passenden Playwright-Browserbuild anhand des bestehenden Lockfiles installieren/reparieren, wenn Ursache belegt; keine Absenkung der Testmatrix. Fokusfall getrennt per Tastatur und Pointer prüfen. Erwartete Fokusführung aus der Bedienhandlung begründen, nicht nur den Test auf aktuelles Fehlverhalten ändern. Produktfix nur bei reproduzierbarem Produktbefund; Umgebungsfehler getrennt berichten.
- [ ] **4. Toolchain/CI an den geprüften Stand binden.** CI Node 22.23.2 und npm 10.9.8 mit Versionausgabe prüfen; `npm ci` respektiert Lockfile. Bestehende Legacy-Jobs behalten. Neue Stufen explizit: `verify:v2`, historischer Aktivierungsnachweis innerhalb `verify:v2:implementation`, aktueller Entwicklungsvalidator und `verify:v2:m06`. Alte `verify:v2:active` bleibt als historische Direktprüfung dokumentiert und darf nach absichtlicher Paketänderung nicht als aktuelle Grünprüfung ausgegeben werden. Browser Chromium/Firefox/WebKit plus Root-/Subpath-Build. YAML-Konfiguration semantisch testen:

```ts
const requiredCommands = [
  'npm run verify:v2',
  'npm run verify:v2:implementation',
  'npm run verify:v2:m06',
];
// In pages-workflow.test.ts aus geparsten run-Schritten prüfen,
// jeweils eigene ausführbare CI-Stufe; vorhandene Jobs nicht ersetzen.
for (const command of requiredCommands) expect(runSteps).toContain(command);
```

`runSteps: string[]` wird im Test aus `parse(readFileSync('.github/workflows/ci.yml','utf8')).jobs` und deren `steps[].run` gewonnen, nicht als Testkonstante gesetzt.
- [ ] **5. Prüforchestrator implementieren.** Befehle als Argumentarrays via `spawnSync`, Exitcode jeder Stufe erhalten; nach einem Fehler keine Gesamt-Grünmeldung. Resultate jeder Stufe getrennt in ignoriertem `reports/v2-m06/` schreiben. Keine Parallelbuilds gegen `src/generated`, keine abgeschnittenen/hängenden Läufe als bestanden zählen. Grundgerüst:

```ts
import { spawnSync } from 'node:child_process';
export function runCheck(command: string, args: readonly string[]): number {
  const result = spawnSync(command, [...args], { stdio: 'inherit', shell: false });
  return result.status ?? 1;
}
```

Unter Windows Node-basierte npm-CLI wie im bestehenden Verifier verwenden, statt `npm.cmd` mit Shellstrings zu interpolieren. Stufen: Contracts/Boundaries, Typecheck/Astro, Vitest, Python, V2-Nachfolger, Registry/Material, Build Root/Subpath, Browser, Offline/Accessibility, Lizenzen. Bestehendes V1 `verify:ium5` einmal als Integrationsregression ausführen; bekannte Fehler nicht stillschweigend überspringen.
- [ ] **6. Menschlich lesbaren Review schreiben.** Didaktikreview deckt alle sieben Curriculumrecords, P0–P6, MAT-01–10, zwölf LXF-Gates und drei Informationsbereiche ab. Technikreview ordnet F01–F08 und TECH-01–11 konkreten Befunden zu. Status pro Befund: synthetisch behoben / realer Nachweis offen / ungelöst. Vorläufige `pass`-Zahlen aus diesem Plan niemals übernehmen. Leerer Realprüf-Handoff bindet Kandidatenrevision und listet benötigte Zielprofile, Rollen, fünf Termine, Materialrechte und absoluten Löschvertrag aus PILOT; fehlende Kontextdaten bleiben offen.
- [ ] **7. Commit und Übergabe.** `git diff --check`, alle erforderlichen tatsächlichen Gates, Fetch/Pull, Commit `test: verify V2 M06 development candidate`. Dashboard auf den neuen belegten Implementierungs-/Technikstand setzen; reale Nutzung/Pilot/Release und Coverage unverändert. Falls die Vollprüfung scheitert, Paket bleibt offen mit exaktem verbleibendem Fehler, kein Gesamterfolg. Keine tatsächliche Realprüfung aus diesem Paket ableiten.

## Abdeckung und Review des Plans

| Eingang / Grenze | Zuständiges Paket |
| --- | --- |
| TECH-F01/F02/F03 | IMP02: gleiche Datenannahme, Recovery, Previewtransaktion |
| TECH-F04/F05 | IMP03: Revision/Löschgeneration, Speicherwahl, Datenverwaltung, bewusste Ausgabe |
| TECH-F06 | IMP04: Wiederherstellbarkeit und Clientkoordination |
| TECH-F07 | IMP05–07: neutraler Kern, eigene Grafik/Code, Payload, neue Registry/Route |
| TECH-F08 | IMP01: Siegel/Statusnachfolger; IMP08: Toolchain/CI/Firefox/WebKit |
| P0/P4 | IMP05: flüchtiger Sessionzustand; IMP06/07: frühe Diagnose/Abruf vor Wiederanzeige; IMP08: Speicher-/Exportsentinels |
| P1/P2/P3 | IMP05–07: editierbare Darstellung, eigener Code, Vorhersage/Spur und Revision |
| P5/P6 | IMP05–07: manueller Zustandswechsel und begründete Systemzuordnung |
| MAT-01–10 / H1–H4 | IMP06 vollständig; IMP07 Ausspielung und zugängliche Interaktion |
| PILOT TECH-01–11 / USE-01–05 / OBS-01–12 | IMP08 synthetische Vorprüfung und vorbereitete Realübergabe; keine reale Erhebung |
| LXF-Gates / Quellen und Rechte | IMP06/08 einzeln reviewen, fremde Assets nicht voraussetzen |
| Tatsächlicher M01-Stand, Schule, Personal, Datenorte, Termine | Vor realer Nutzung/Pilot durch zuständige Stellen; keine fiktive Befüllung |

Prüfung dieses Plans: Quellpfade und vorhandene API-Signaturen am Eingang `150deea` gelesen; neue APIs ausdrücklich als geplant deklariert. Kein Produktionscode oder neuer Test aus den Codeblöcken ausgeführt. Die acht Pakete und ihre Vault-Tasks sind in [plan.json](../../../roadmap/v2/implementation-planning/plan.json) vollständig verzeichnet. [Eingabebindungen](../../../roadmap/v2/implementation-planning/input-bindings.json) und [Prüfbericht](../../../roadmap/v2/implementation-planning/validation-report.md) machen den Autorenreview nachvollziehbar. Die Pakete werden vor Ausführung nach tatsächlichem Auftrag übernommen. Alle Codebeispiele sind Test-/Implementierungsanker, keine Behauptung einer fertigen Implementierung.

Die alte direkte FU-PILOT-Paketprüfung begrenzt Repoänderungen auf ihren damaligen Auftrag. Sie darf nach neuen Plan-/Implementierungsdateien erwartbar nicht mehr als globale aktuelle Prüfung eingesetzt werden. Angenommenen Paketstand historisch prüfen, Integrität seiner Dateien aktuell prüfen und neue Entwicklungsprüfungen additiv ergänzen. Gleiches gilt für FU-MOD-Probes, die historische Produktionsunverändertheit voraussetzen.

**Nächster Ausführungsschritt nach Planannahme:** IMP01 mit eigenem konkretem Auftrag starten. Der geeignete erste Auftrag lautet: „Plan angenommen. Führe IUM-V2-IMP01 aus.“ Nach diesem Paket liegen die Voraussetzungen für sichere weitere Entwicklung vor; die folgenden Pakete werden dadurch nicht automatisch erledigt.
