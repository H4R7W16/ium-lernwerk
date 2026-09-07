# V2 Runtime, Speicher und Update – Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans`; keine Subagenten ohne ausdrücklichen Auftrag. Nur tatsächlich autorisierte Pakete ausführen. Schritte sind mit `- [ ]` markiert.

**Goal:** TECH-F01–F06 mit konsistenter Datenannahme, zugänglicher Originalsicherung und überprüfbarem Schutz vor Überschreiben, Löschen und Updateverlust schließen.

**Architecture:** Die vorhandene Runtime erhält einen gemeinsamen Annahmepfad und separat gehaltene Recoverydaten. Ein neuer V2-Repositoryadapter implementiert den bestehenden Speicherport mit atomarem Revisionsvergleich. Eine eigene Reload-Vorbereitung unterscheidet temporär vorhandene von tatsächlich wiederherstellbarer Arbeit und koordiniert betroffene Clients.

**Tech Stack:** Bestehende TypeScript-/Vitest-/idb-/fake-indexeddb-/Playwright-Abhängigkeiten; Node 22.23.2/npm 10.9.8. Keine neue externe Abhängigkeit.

**Spec:** [Hauptplan](2026-09-07-ium-v2-referenzmodul-implementation.md), [TECH-F01–F06](../../../roadmap/v2/follow-ups/technical/findings.md), [MOD](../specs/2026-09-07-ium-v2-g5-m06-referenzmodul-design.md), [PILOT-Datenvertrag](../../../roadmap/v2/follow-ups/pilot/data-and-rights.md).

## Global Constraints

- Alle Grenzen und Ausführungsbedingungen des Hauptplans gelten. IMP01 muss angenommen abgeschlossen sein.
- Kein V1→M06-Payloadimport, kein neues globales Produktions-/Einsatzrecht.
- P1/P2/P3/P5/P6 begrenztes Dossier, P0/P4 flüchtig. Keine Telemetrie oder realen Daten in Tests.
- Ein Download-Anstoß ist kein Nachweis einer vorhandenen Datei. Automatisches Clipboard entfällt.
- V1-Inhalts-/Payloadformat und alte Datenbank bleiben erhalten. V2 nutzt eigenen expliziten Datenraum.
- Tests sind vor Produktänderungen rot auszuführen; Prüfbeispiele dieses Plans sind noch nicht ausgeführte Tests.

## IMP02 – Einheitliche Datenannahme, Recovery und Importtransaktion

**Files – Modify:** `packages/module-runtime/src/runtime.ts`, `packages/module-runtime/src/migrations.ts`, `packages/module-runtime/src/index.ts`, `tests/platform/runtime.test.ts`, `packages/module-contract/src/errors.ts`, `schemas/learning-state-envelope.schema.json`, `tests/platform/contracts.test.ts`. Nur neue Fehlercodes ergänzen, wenn bestehende Codes die Unterscheidung nicht tragen.

**Files – Create:** `packages/module-runtime/src/accept-state.ts`, `tests/platform/runtime-acceptance.test.ts`.

**Interfaces:** Bestehend: `createModuleRuntime(dependencies)`, `start()`, `updatePayload(payload)`, `flush()`, `previewImport(bytes)`, `confirmImport()`, `deleteActive()`, `deleteAll()`, `exportState()`. `StateRepository.load(moduleId)` liefert bisher eine deklarierte Envelope; Inhalt trotzdem als untrusted validieren.

Neue optionale Dependencies mit rückwärtskompatiblen Defaults:

```ts
import type { LearningStateEnvelope } from '@ium/module-contract';
export type StatePolicy = Readonly<{
  supportedModuleVersions: readonly string[];
  createInitialPayload: () => Record<string, unknown>;
  validatePayload: (payload: unknown) => boolean;
}>;
```

`ModuleRuntimeDependencies.statePolicy?: StatePolicy`; ohne Policy gilt unterstützte Version genau `moduleVersion`, Initialpayload `{}`, modulneutrale Objekthülle. M06 liefert immer seine explizite Policy. Neue Methoden `cancelImport(): void`, `hasRecovery(): boolean`, `exportRecovery(): Promise<ExportResult>`; `ExportResult` entspricht dem bisherigen `exportState`-Resultat. Recoveryausgabe ist als Original-/Fehlerdatei bezeichnet und nie als gültiger M06-Arbeitsstand aktiviert. Gesonderter Typ `RecoverySnapshot = {source:'local'; value:unknown} | {source:'import'; bytes:Uint8Array}` intern, nicht in der Payload.

- [ ] **1. Sequenzfehler und Ladeabweichung als rote Tests ergänzen.** In bestehender `runtime.test.ts` die vorhandenen Funktionen `state()` und `createRuntime()` nutzen; diese sind dort definiert. Test vollständig:

```ts
test('a failed new preview invalidates the preceding valid preview', async () => {
  const repository = new MemoryStateRepository();
  const original = state({ payload: { text: 'original' } });
  await repository.save(original);
  const runtime = createRuntime(repository);
  expect((await runtime.start()).ok).toBe(true);
  expect(runtime.previewImport(serializeState(state({payload:{text:'A'}}))).ok).toBe(true);
  expect(runtime.previewImport(new TextEncoder().encode('{broken')).ok).toBe(false);
  expect((await runtime.confirmImport()).ok).toBe(false);
  expect(await repository.load(original.moduleId)).toEqual(original);
});
```

Zweiter Test mit `state({moduleVersion:'2.0.0'})`: direkter Start und Import beide `IMPORT_UNSUPPORTED_VERSION`. Dritter mit ungültigem `savedAt`: beide ablehnen. Run: `npx vitest run tests/platform/runtime.test.ts`. Erwartet zunächst mindestens diese drei fehlschlagenden Fälle.
- [ ] **2. Zustandshülle und Annahmepfad implementieren.** Die bestehende `moduleId`-Regex akzeptiert M06 noch nicht. Exakt `V2-G5-M06` als weitere Alternative zulassen; keine beliebigen V2-IDs, keine Änderung des V1-Modulmanifests. Vertragstests: M06 akzeptiert, V2-G5-M07 und V2-G8-M06 abgewiesen, alle bisherigen gültigen IUM-/TEST-IDs erhalten. `npm run contracts:generate` regeneriert die ignorierten `.d.ts` unter `packages/module-contract/src/generated`; keine Handänderung oder Aufnahme dieser Laufzeitdateien in Git. `npm run contracts:check` und Vertragstests prüfen das Ergebnis.

`acceptState(raw, dependencies)` liefert `RuntimeStateSuccess | RuntimeFailure` ohne Speicherung; Reihenfolge Hüllenvalidierung → Modulidentität → unterstützte Modulversion → lückenlose Schema-Migration auf einer Kopie → Hüllen-/Payloadprüfung. Abgelehnte Fremd-/Zukunftsversion nicht durch Schemaidentität legitimieren. Nur nach Erfolg darf auf die Zielmodulversion umgestellt werden, und nur wenn die Supportliste diese Quellversion ausdrücklich zulässt. Nie die globale Modulversion mit Schemanummer gleichsetzen. Migration prüft auch den Fall null Schritte. Initialpayload vor erstem Speichern validieren. Prüfung von `updatePayload` gegen die Policy vor Änderung von `#active`; ungültiger eigener UI-Payload muss sichtbar scheitern und alten Stand erhalten.

```ts
// Am Beginn jeder Vorprüfung, auch vor UTF-8-/JSON-Parsing:
this.#pendingImport = null;
// Erst nach vollständiger Annahme:
this.#pendingImport = structuredClone(accepted.state);
```

`cancelImport`, `deleteActive`, `deleteAll` und ein neuer `start()` entwerten Pending bereits am Anfang. `confirmImport()` konsumiert genau den aktuellen Kandidaten einmal; bei Savefehler bleibt der aktive Stand unverändert, erneute Bestätigung erfordert neue Vorprüfung. Keine zufällige Wiederaktivierung einer früheren Vorschau.
- [ ] **3. Recovery separat erhalten.** Lokales Original direkt nach Load kopieren, vor Migration. Bei Import Originalbytes vor Parsing kopieren, Größenlimit 5 MiB beibehalten. `start()` fängt Load-/Savefehler; ein echter Loadfehler ohne gelesene Daten darf keine vorhandene Originalsicherung behaupten. Fehlermeldung bietet Wiederholung und bereits vorhandene externe Sicherung. Verfügbares Recoveryoriginal bleibt unabhängig von `#active` exportierbar, wird nicht überschrieben und nicht beim bloßen Schließen eines Fehlerdialogs gelöscht. Explizites Löschen/Neustarten entwertet es nach bestätigter Datenentscheidung. Für lokales JSON-fähiges Original inhaltsgetreue JSON-Ausgabe, bei Import bytegetreue Ausgabe. Nicht serialisierbarer beschädigter IDB-Inhalt: verständlicher Recoveryfehler, kein falscher Exporterfolg.
- [ ] **4. Recovery-/Migrationsmatrix testen.** Migration fehlt/wirft/liefert falsche Payload; lokale gleiche/neue/falsche Version; leerer/ungültiger JSON-Import; Initialpayload falsch; Savefehler nach erfolgreicher Migration; Vorschau→Abbruch→Bestätigung, Vorschau→Löschen→Bestätigung, zweimalige Bestätigung. Prüfen: Original unverändert, ungültiger Zielstand nie aktiv, gültige Migration erst nach allen Checks gespeichert. Capture-Exportport des Tests vergleicht Originalbytes und aktiviert nichts. M06-Versionpolicy später `['0.1.0']`, Schema1, `migrations: []`.
- [ ] **5. Regression und Abschluss.** `npx vitest run tests/platform/runtime.test.ts tests/platform/runtime-acceptance.test.ts tests/platform/export-import.test.ts`, `npm run typecheck`, neue Entwicklungsprüfung. Fetch/Pull und Commit `fix: unify runtime state acceptance and recovery`. TECH-F01–03 als synthetisch behoben mit konkreten Tests führen; echte Zielprüfung offen.

## IMP03 – Revisionsschutz, Speicherwahl und bewusste Ausgabe

**Files – Create:** `packages/local-state/src/versioned-indexeddb-repository.ts`, `packages/local-state/src/versioned-memory-repository.ts`, `packages/local-state/src/version-token.ts`, `apps/lernwerk-portal/src/controllers/storage-choice.ts`, `apps/lernwerk-portal/src/controllers/local-data-v2.ts`, `apps/lernwerk-portal/src/pages/tests/[probe].astro`, `apps/lernwerk-portal/src/components/RuntimeProbe.astro`, `apps/lernwerk-portal/src/controllers/runtime-probe.ts`, `playwright.runtime.config.mts`, `tests/platform/versioned-state.test.ts`, `tests/browser/v2-storage.spec.ts`, `tests/browser/helpers/storage-choice.ts`.

**Files – Modify:** `apps/lernwerk-portal/astro.config.ts`, `tests/platform/portal-build.test.ts`, `packages/local-state/src/index.ts`, `packages/module-contract/src/errors.ts`, `apps/lernwerk-portal/src/pages/daten.astro`, `apps/lernwerk-portal/src/controllers/algorithm-workbench/browser-ports.ts`, `apps/lernwerk-portal/src/controllers/algorithm-workbench/workbench-controller.ts`, `tests/platform/local-state.test.ts`, `tests/platform/export-import.test.ts`, `tests/browser/ium5-workbench.spec.ts`, `tests/browser/ium5-state.spec.ts`, `tests/browser/ium5-accessibility.spec.ts`, `tests/browser/ium5-offline.spec.ts`. Der V1-Controller bekommt nur Speicherwahl-/Exporttextkorrektur, keinen neuen M06-Lernweg. Bestehende IUM5-Browsertests wählen ihren vorgesehenen Modus ausdrücklich in der neuen UI; sie überspringen die Wahl nicht durch manipulierten Speicher. Die generischen Testfixture-Seiten behalten explizit gewählte Testmodi.

**Interfaces:** Die neuen Repositoryklassen implementieren `StateRepository` unverändert. Jede Runtime erhält **eigene Adapterinstanz**, keine gemeinsame Tokenmap. V2-Fabrik `createV2StateRepository(options: CreateStateRepositoryOptions): Promise<StateRepositorySelection>` wie vorhandene Fabrik, aber V2-Adapter. `VersionedIndexedDbStateRepository.open({indexedDbFactory,databaseName?})`; `VersionedMemoryStateRepository(mode?, backing?)`, wobei `backing` ausschließlich für geteilte synthetische Tests eine gemeinsame Map/Generation hält.

```ts
type VersionToken = Readonly<{ generation: number; revision: number }>;
type StoredRow = Readonly<{
  moduleId: string;
  revision: number;
  state: import('@ium/module-contract').LearningStateEnvelope | null;
}>;
// IDB-Datenbank ium-lernwerk-v2, Version 1:
// store states: keyPath moduleId; store meta: key 'generation', value number.
```

- [ ] **1. Reproduzierbaren CAS-Test rot schreiben.** `syntheticState()` in neuer Testdatei mit gültiger Envelope (Modul `V2-G5-M06`, Version0.1.0, Schema1, UUID, ISO-Datum, Payload `{test:'A'}`) definieren. Vollständiger zentraler Test:

```ts
import { test, expect } from 'vitest';
import { IDBFactory } from 'fake-indexeddb';
import { VersionedIndexedDbStateRepository as Repository }
  from '../../packages/local-state/src/versioned-indexeddb-repository.js';
test('stale instance cannot overwrite a newer row or revive deletion', async () => {
  const indexedDbFactory = new IDBFactory();
  const a = await Repository.open({ indexedDbFactory, databaseName: 'synthetic-cas' });
  const b = await Repository.open({ indexedDbFactory, databaseName: 'synthetic-cas' });
  const original = {
    format: 'ium-learning-state' as const, formatVersion: 1 as const,
    moduleId: 'V2-G5-M06', moduleVersion: '0.1.0', stateSchemaVersion: 1,
    workspaceId: '123e4567-e89b-42d3-a456-426614174000',
    savedAt: '2026-09-07T12:00:00.000Z', payload: { test: 'A' }
  };
  await a.load(original.moduleId);
  expect((await a.save(original)).ok).toBe(true);
  await b.load(original.moduleId);
  expect((await a.save({...original,payload:{test:'new'}})).ok).toBe(true);
  expect((await b.save(original)).ok).toBe(false);
  await b.load(original.moduleId);
  expect((await a.deleteAll()).ok).toBe(true);
  expect((await b.save(original)).ok).toBe(false);
  expect(await a.load(original.moduleId)).toBeNull();
});
```

Run `npx vitest run tests/platform/versioned-state.test.ts`; zuerst fehlender Adapter, danach jede Konfliktfolge prüfen.
- [ ] **2. Atomare Speicherung implementieren.** `load` liest `meta` und `states` gemeinsam in einer readonly-Transaktion und merkt `{generation, revision}`; leerer Slot Revision0. `save` braucht diesen Token und eine readwrite-Transaktion über beide Stores. Innerhalb derselben Transaktion Isttoken vergleichen, dann Revision+1 schreiben. Bei Konflikt Fehler `STORAGE_CONFLICT`, niemals still neu laden/erneut speichern. Token nur nach erfolgreichem Commit aktualisieren. Vollständige Methode darf zwischen Lesen und Put keinen zweiten Transactionkontext öffnen. Bei Quota/abgebrochener Transaktion Token und Datensatz unverändert.

```ts
export function sameVersion(a: VersionToken, b: VersionToken): boolean {
  return a.generation === b.generation && a.revision === b.revision;
}
```

Diese reine Funktion ist nur Vergleich; Atomarität muss im IDB-Adapter und im echten Browser getestet werden. `deleteModule` schreibt Tombstone `{state:null,revision:old+1}`; `deleteAll` erhöht Generation und leert Zustandsinhalte atomar. Minimale nicht personenbezogene Generation/Tombstones dürfen als technischer Löschschutz bleiben. Alte Clients mit alten Tokens scheitern. Ein bewusst gestarteter neuer Stand lädt den aktuellen Token nach expliziter Speicherwahl. Ein Konflikt zeigt erhaltene eigene Sitzung plus Export/Wiederöffnen, nicht stillen Verlust.
- [ ] **3. Speicherwahl vor erstem Schreiben implementieren.** `chooseStorage(root): Promise<'persistent'|'volatile-selected'>` verbindet zwei sichtbare Buttons „Auf diesem Gerät speichern“ und „Nur in dieser Sitzung arbeiten“. Erst nach Auswahl Fabrik/Runtime starten; auch kein leeres Initialdossier vorher anlegen. Kein gespeicherter automatischer Zustimmungsmarker. Erneuter Besuch fragt wieder; „Auf diesem Gerät speichern“ öffnet vorhandenen Profilstand, ohne neue Personenzuordnung zu behaupten. Flüchtiger Modus liest/schreibt keine persistente Datenbank. Nicht verfügbare IDB liefert `volatile-fallback` mit sichtbarer Verlustgrenze. V1-Controller setzt dieselbe Wahl vor seine bisherige Fabrik, `?storage=volatile` kann explizit nur flüchtig wählen; der normale Link bleibt bewusst auswählbar.
- [ ] **4. Exportwege berichtigen.** `createBrowserExportPort.copyText` zeigt lediglich das auswählbare Textfeld. `navigator.clipboard.writeText` nur nach eigenem Klick „In Zwischenablage kopieren“, Fehler hält Textfeld bedienbar. Erfolgsmeldung Download: „Download angefordert. Prüfe die Datei in deiner Ablage.“ Keine Annahme einer geprüften Datei aus `link.click()`. Recovery als Originaldatei klar vom gültigen Dossierexport unterscheiden. Bei erneutem Bearbeiten vorherigen Sicherungshinweis entwerten. Exporttexte benennen externe Downloads/Clipboard/Profilsync als getrennte Ablagen.
- [ ] **5. Globale Datenverwaltung integrieren.** `deleteAllLocalLearningData(): Promise<{ok:boolean; v1:'deleted'|'failed'; v2:'deleted'|'failed'}>` ruft beide lokalen Datenräume auf. Keine Datenbank kann gemeinsame Atomarität mit der anderen bieten; Teilerfolg daher explizit anzeigen und Wiederholung ermöglichen. Reine Verwaltungsseite öffnet Speicher nur bei tatsächlicher Verwaltungsaktion; kein neuer Lernstand. Texte begrenzen Löschung auf Browserprofil/Origin, nicht Gerät insgesamt. Exporte, Clipboard, externe Syncs und Serverlogs sind nicht eingeschlossen. Vorhandene volatile Clients werden per Invalidation-Nachricht zum Verwerfen des gelöschten Profils und ihrer Pendingimports aufgefordert; persistentes CAS erzwingt zusätzlich den Löschschutz. Andere offene volatile Seiten können ohne Clientbestätigung nicht als gelöscht gelten; fehlende Bestätigung sichtbar machen.
- [ ] **6. Synthetische Prüfhülle und Browserprüfung erstellen.** Die neue dynamische Route `tests/[probe].astro` liefert `getStaticPaths()` ausschließlich im vorhandenen Profil `fixture` mit `{params:{probe:'v2-runtime'}}`; bei production und v2-development eine leere Liste. `RuntimeProbe.astro`/`runtime-probe.ts` verbinden eine synthetische Textpayload mit den echten neuen Speicher-/Runtimeports: Textfeld, Speichern, Wiederöffnen, Export und Löschen, klarer Synthetikhinweis. Keine Lernendenmaterialien oder echte Daten. `playwright.runtime.config.mts` startet den bestehenden Fixture-Preview auf4321 und verwendet die neue Route. Buildtest muss deren Abwesenheit im Produktionsbuild prüfen; Astro-Ausgabeisolation muss auch die zugehörigen Probe-JavaScriptbundles aus production entfernen.

Neue Browserdatei nutzt zwei Seiten **desselben Contexts** für gemeinsame IDB, zusätzlich zweiten Context für getrenntes Profil. Vor Wahl weder Datenbank mit Lernstand noch Sentinelinhalt, flüchtiger Modus bleibt nach Reload leer, Konflikt/Globaldelete verhindert Wiederbelebung, Quota/IDB-Sperre erzeugt ehrliche Meldung, kein unaufgeforderter Clipboardaufruf. Netzwerk- oder Clipboardzugriff durch Testspies beobachten, nicht lediglich Codewortsuche. `tests/browser/helpers/storage-choice.ts` exportiert `choosePersistent(page)` und `chooseVolatile(page)` als Klick auf die entsprechenden sichtbaren Buttons, ohne automatische bedingte Umgehung.
- [ ] **7. Abschluss.** `npx vitest run tests/platform/versioned-state.test.ts tests/platform/local-state.test.ts tests/platform/export-import.test.ts`, `npm run typecheck`, `npx playwright test tests/browser/v2-storage.spec.ts --config playwright.runtime.config.mts`; V1-Speicherwahlregression gezielt ausführen. Ohne Browserbeleg kein vollständiger IMP03-Abschluss. Fetch/Pull, Commit `feat: protect V2 storage revisions and explicit data choices`.

## IMP04 – Wiederherstellbarkeit und Updatekoordination

**Files – Create:** `apps/lernwerk-portal/src/controllers/reload-readiness.ts`, `apps/lernwerk-portal/src/controllers/update-coordinator.ts`, `tests/platform/reload-readiness.test.ts`, `tests/browser/v2-update.spec.ts`.

**Files – Modify:** `apps/lernwerk-portal/src/controllers/pwa-registration.ts`, `apps/lernwerk-portal/src/sw.ts`, `apps/lernwerk-portal/src/controllers/algorithm-workbench/workbench-controller.ts`, `apps/lernwerk-portal/src/controllers/fixture-workspace.ts`, `apps/lernwerk-portal/src/controllers/runtime-probe.ts`, `packages/module-runtime/src/runtime.ts`, `packages/module-runtime/src/index.ts`, `tests/platform/pwa-contract.test.ts`. IMP07 registriert anschließend den neuen M06-Controller an diesem Vertrag.

**Interfaces:** `prepareForReload(): Promise<ReloadReadiness>` an jeder registrierten Runtime/Controller; `FlushRequestDetail.add(Promise<boolean>)` wird vollständig durch `ReloadRequestDetail.add(Promise<ReloadReadiness>)` abgelöst, alle Listener aktualisieren. Ergebnis:

```ts
export type ReloadReadiness =
  | { safe: true; reason: 'persisted-readback' | 'no-work' | 'explicit-discard'; revision: number }
  | { safe: false; reason: 'volatile' | 'write-failed' | 'conflict' | 'readback-failed' | 'unknown-client' };
export function allReady(values: readonly ReloadReadiness[]): boolean {
  return values.every(value => value.safe);
}
```

`revision` ist eine lokale Bearbeitungsrevision ohne Lernzeit-/Historienlogging. Persistenter Readback vergleicht die tatsächlich gespeicherte aktuelle Envelope mit dem aktuellen Entwurf; ein fremder oder veralteter Datensatz ist nicht sicher. Ein gelöschter/noch nicht gestarteter Arbeitsplatz hat `no-work`. Flüchtig bedeutet immer unsicher, außer die Person verwirft nach sichtbarem Hinweis genau diese aktuelle Revision bewusst. „Export angefordert“ erzeugt kein `safe:true`.

- [ ] **1. Verlustfall als roten Test schreiben.** In `reload-readiness.test.ts` reine Entscheidung und async Orchestrierung prüfen:

```ts
import { test, expect } from 'vitest';
import { allReady } from '../../apps/lernwerk-portal/src/controllers/reload-readiness.js';
test('one volatile client prevents reload even if another persisted', () => {
  expect(allReady([
    {safe:true,reason:'persisted-readback',revision:1},
    {safe:false,reason:'volatile'}
  ])).toBe(false);
});
```

Zusatz: abgelehnte Readiness-Promise ergibt sichtbaren Abbruch, niemals unhandled rejection; noch eine Änderung nach Readback entwertet die Bereitschaft. Run `npx vitest run tests/platform/reload-readiness.test.ts`.
- [ ] **2. Lokale Readiness statt Booleanflush implementieren.** Runtime hält Zähler für jede eigene Änderung, Import, Löschung; Readback muss zur eingefrorenen Revision passen. Während kurzer Updatevorbereitung Eingaben sperren; Veto/Timeout löst Sperre wieder. Fehlerbehandlung umschließt **auch** `Promise.all`/Readback, nicht nur `updateServiceWorker`. Kein Silent-Fallback von fehlendem Listener auf „sicher“ für einen als Arbeitsplatz gekennzeichneten Client.
- [ ] **3. Andere Clients einschließen.** Service Worker inventarisiert eigene kontrollierte WindowClients; Updatehandshake über `postMessage`/`MessageChannel`, mit wechselnder zufälliger Requestkennung und Versionsprotokoll1. Jede Teilnehmerseite bestätigt `ready` oder `veto`, hält ihre passende Revision eingefroren. Timeout nach 5 Sekunden ist technische UX-Heuristik und ergibt `unknown-client`, kein erzwungener Reload. Neue Clients während Vorbereitung invalidieren die Inventarliste; vor Aktivierung erneut inventarisieren. Alte Seiten ohne Protokollantwort blockieren und fordern geordnetes Schließen. BroadcastChannel kann ergänzende Benachrichtigung sein, ist wegen verpasster Nachrichten keine Vollständigkeitsgarantie.
- [ ] **4. Aktivierung kontrollieren.** Zweiphasig vorbereiten/aktivieren, bei Veto alle bestätigten Clients entsperren. Keine `skipWaiting`-/Claim-/Reload-Automatik außerhalb des Koordinators. Versions-/Requestkennungen verhindern späte Antworten auf alte Versuche. Defekter Kandidat bleibt zurückgestellt. Ein offener fremder Scope wird nicht einbezogen, eigene Produkt-/Fixture-/V2-Clients desselben tatsächlichen SW-Scopes dagegen schon. Mehrere Tabs sind mit tatsächlich registriertem Service Worker zu testen, nicht nur durch Arrays von Wahrheitswerten.
- [ ] **5. Ausweichhandlung anbieten.** „Weiterarbeiten“/„Später aktualisieren“, bewusster Export, oder „Diesen ungesicherten Stand verwerfen und aktualisieren“. Letzte Handlung benennt Verlust und benötigt unmittelbare Bestätigung; nach weiterer Bearbeitung ungültig. Für einen anderen ungesicherten Client keine globale Verlustzustimmung stellvertretend annehmen.
- [ ] **6. Verifizieren und abschließen.** Tests mit volatile-selected, volatile-fallback, Quota, Promise-Rejection, veraltetem Readback, zwei Tabs, geschlossenem/neu hinzugekommenem Client, Timeout, altem Protokoll, erfolgreichem und defektem Kandidaten. `npx vitest run tests/platform/reload-readiness.test.ts tests/platform/pwa-contract.test.ts`, `npm run typecheck`; `npx playwright test tests/browser/v2-update.spec.ts --config playwright.runtime.config.mts` gegen die bereits in IMP03 erstellte synthetische Prüfhülle. Ohne Browserbeleg bleibt die koordinierte Updatefunktion unbestätigt. Fetch/Pull, Commit `fix: require recoverable client state before updates`.

## Übergabe zum Fachkern

IMP02–04 sind mit reiner Logik und der synthetischen Browserhülle unabhängig vom späteren M06-UI prüfbar. Erst nach ihren tatsächlichen Abschlüssen folgt IMP05. IMP08 wiederholt die relevanten Daten-/Updatefälle an der integrierten M06-Oberfläche. Kein Implementierungspaket behauptet reale iPad-/LMS-/Schulfreigaben.
