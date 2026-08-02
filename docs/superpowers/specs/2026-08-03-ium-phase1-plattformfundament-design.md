# IuM-Lernwerk – Phase 1 Plattformfundament

**Status:** schriftlich freigegeben am 3. August 2026

**Fassung:** 1.1

**Datum:** 3. August 2026

**Scope:** Phase 1 der freigegebenen IuM-Lernwerk-Gesamtarchitektur

**Ausgangsstand:** `main` auf Commit `75f661d`

## 1. Entscheidung und Ziel

Phase 1 erstellt ein schlankes, vertragsorientiertes Plattformfundament für das IuM-Lernwerk. Es stellt die technische Grundlage für spätere fachliche Lernmodule bereit, produziert aber selbst noch kein Unterrichtsmodul.

Die Plattform wird ausschließlich mit einer synthetischen technischen Referenz-Fixture geprüft. Das in Phase 0 ausgewählte Goldstandard-Modul `IUM-5-CORE-05 – Präzise Abläufe ausführbar machen` bleibt vollständig Phase 2 vorbehalten.

Phase 1 ist erfolgreich, wenn ein vollständiger technischer Pfad nachweisbar funktioniert:

```text
Manifest laden und validieren
→ Portalroute erzeugen
→ synthetische Interaktion ausführen
→ lokalen Zustand speichern
→ neu laden und fortsetzen
→ exportieren
→ löschen
→ importieren
→ nach erfolgreicher Ersteinrichtung offline weiterarbeiten
→ kontrolliert auf eine neue Version wechseln
```

Dieser „Walking Skeleton“ belegt die Plattformverträge. Er behauptet weder fachliche Modulqualität noch curriculare Abdeckung oder Wirksamkeit im Unterricht.

## 2. Bindende Grundlagen

Bindend bleiben:

- das freigegebene Gesamtdesign `docs/superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md`;
- die Phase-0-Forschung zu Lernwirksamkeit, Informatik- und Medienbildungsdidaktik, Accessibility, Datenschutz, Offlinebetrieb und OER;
- das IuM-Fachprofil für Gymnasium Baden-Württemberg, Klassen 5–7;
- die bestehende Statusfolge `draft → working → reviewed → standard`;
- lokale, datensparsame Lernstände ohne Konto, Backend, Telemetrie oder zentrale Diagnostik;
- digital als Primärmedium und analoge Materialien nur mit eigenständiger Lernfunktion;
- eigener Code unter MIT und eigene Lerninhalte unter CC BY-SA 4.0.

Phase 1 verändert keine Curriculum-, Coverage-, Zeit-, Pilot-, Verfügbarkeits- oder Produktstatuswerte aus Phase 0, IUM09, IUM10 oder IUM11.

## 3. Nichtziele

Phase 1 enthält ausdrücklich nicht:

- fachliche Lerninhalte oder ein Goldstandard-Modul;
- ein modulspezifisches oder übergreifendes Lehrkräftehandbuch;
- reale Unterrichtspilotierung oder reale Lernendendaten;
- Individualdiagnostik, Lernanalyse, automatische Benotung oder personenbezogene Profile;
- zentrale Speicherung, Synchronisation oder Konten;
- eine vollständige visuelle Marken- oder Designsystementwicklung;
- ein zusätzliches UI-Framework ohne nachgewiesenen Bedarf;
- eine Festlegung auf einen langfristigen Hostinganbieter;
- eine Statushochsetzung bestehender Arbeitsstände;
- einen parallelen Druckbestand.

## 4. Bewertete Architekturansätze

### 4.1 Gewählt: vertragsorientiertes Monorepo

Portal, Verträge, Laufzeit, Speicherung, Import/Export und UI-Grundbausteine werden als kleine, klar gerichtete Pakete organisiert. Inhalte bleiben von der Plattform getrennt.

Vorteile:

- zentrale, maschinenprüfbare Verträge;
- isolierte Tests und austauschbare Implementierungen;
- klare Grenze zwischen Plattform und Modul;
- spätere Wiederverwendung in allen 31 Modulkandidaten;
- geringer Framework- und Laufzeitanteil.

### 4.2 Verworfen: eine integrierte Astro-Anwendung

Eine einzige Anwendung wäre initial kürzer, würde aber Portal, Speicher, Modulaufnahme und Interaktion früh miteinander verflechten. Änderungen an einem Bereich wären schwerer isoliert prüfbar.

### 4.3 Verworfen: eigenständige Modul-Apps oder Microfrontends

Einzelne Apps pro Modul würden Deployment, Offlinecache, Paketversionierung und gemeinsame Bedienlogik vervielfachen. Für das geplante Lernwerk ist dies vor einem nachgewiesenen unabhängigen Auslieferungsbedarf unnötige Komplexität.

## 5. Technischer Grundstack

Phase 1 verwendet:

- npm Workspaces für lokale Pakete und eine gemeinsame Lockdatei;
- Astro als statischen Portal- und Inhaltsgenerator;
- TypeScript im strikten Modus;
- semantisches HTML und CSS als robuste Basis;
- frameworkfreie TypeScript-Controller zur progressiven Verbesserung;
- JSON Schema 2020-12 als kanonischen Datenvertrag;
- IndexedDB mit der kleinen Promise-Abstraktion `idb`;
- `vite-plugin-pwa` direkt in Astros Vite-Konfiguration mit `injectManifest` für einen kontrollierten eigenen Service Worker;
- Vitest für reine Vertrags- und Unit-Tests;
- Playwright für reale Browserabläufe;
- eine automatisierte WCAG-Prüfung, ergänzt durch verbindliche manuelle Aufgaben;
- GitHub Actions für Build und automatische Qualitätsgates.

Konkrete Abhängigkeitsversionen werden im Implementierungsplan nach einem aktuellen Kompatibilitätscheck festgelegt und anschließend exakt in `package-lock.json` versiegelt. CI verwendet `npm ci`; Builds mit frei aufgelösten Versionen sind unzulässig.

Kompatibilitätspräzisierung vom 3. August 2026: Das aktuelle `@vite-pwa/astro` 1.2.0 deklariert nur Astro 1 bis 5 als Peerbereich, während Astro 7.1.6 Vite 8 verwendet. `vite-plugin-pwa` 1.3.0 unterstützt Vite 3 bis 8 und wird deshalb ohne die veraltete Astro-Integrationshülle direkt über `astro.config.ts` eingebunden. PWA-Strategie, eigener Service Worker und Updatevertrag bleiben unverändert.

## 6. Zielstruktur

```text
apps/
  lernwerk-portal/
packages/
  module-contract/
  module-runtime/
  ui-components/
  local-state/
  export-import/
schemas/
  module-manifest.schema.json
  learning-state-envelope.schema.json
curriculum/
modules/
tests/
  fixtures/
    curriculum/
    reference-module/
  contract/
  unit/
  browser/
  offline/
docs/
```

`modules/` bleibt in Phase 1 ohne fachliches Modul. Eine kurze Dokumentation erklärt dort das spätere Modulformat. Die Referenz-Fixture liegt ausschließlich unter `tests/fixtures/`.

Generierte Registries, Buildcaches, Testberichte und Ausgabeverzeichnisse sind nicht handgepflegt und werden nicht als Quellbestand committed.

## 7. Abhängigkeitsrichtung und Paketverantwortung

```text
schemas
  ↓
module-contract
  ├── local-state
  ├── export-import
  └── module-runtime
          ↓
     ui-components
          ↓
 lernwerk-portal / spätere Lernmodule
```

Zyklische Paketbezüge sind ein Buildfehler.

### 7.1 `schemas`

Enthält die kanonischen JSON-Schemata für Modulmanifest und Lernstands-/Exporthülle. Schemata sind geschlossen: unbekannte Felder werden abgelehnt, sofern eine ausdrücklich offene fachliche Nutzdatenstruktur sie nicht erlaubt.

### 7.2 `module-contract`

Stellt bereit:

- aus den Schemata erzeugte TypeScript-Typen;
- Laufzeitvalidatoren;
- semantische Referenzprüfungen;
- die Statusfolge `draft → working → reviewed → standard`;
- Ports für Speicherung, Export, Import, Uhr und Fehleranzeige;
- geschlossene Fehlercodes.

Generierte Typen werden nicht manuell verändert. Schema, Typen und Validatoren müssen im Build nachweisbar synchron sein.

### 7.3 `local-state`

Implementiert den Speicherport mit:

- einem versionierten IndexedDB-Adapter;
- einem flüchtigen In-Memory-Adapter;
- atomaren Schreiboperationen und technischen IndexedDB-Schemamigrationen;
- explizitem Löschen eines Modulzustands oder aller lokalen Lernwerkdaten;
- sichtbaren Zuständen für persistent, bewusst flüchtig und fehlerbedingt flüchtig.

Das Paket kennt weder Astro noch konkrete Moduloberflächen.

### 7.4 `export-import`

Enthält reine Funktionen für:

- Exporthülle und Dateinamen;
- Größen-, Format-, Versions- und Modulprüfung;
- Vorbereitung einer importierten Zustandskopie für die Migration durch `module-runtime`;
- Vorschau vor Übernahme;
- Download sowie kopierbaren Textfallback;
- transaktionale Übergabe an den Speicherport.

### 7.5 `module-runtime`

Koordiniert die Anwendungsfälle:

- Modul starten;
- aktiven Arbeitsstand laden;
- Änderungen speichern;
- modulspezifische Zustandsmigrationen auf validierten Kopien ausführen;
- Speicherstatus melden;
- Zustand exportieren, importieren oder löschen;
- Updatebereitschaft und Fehler an die UI weitergeben.

Die Laufzeit hängt nur von Ports ab und greift nicht direkt auf IndexedDB, Dateien, Service Worker oder Astro zu.

### 7.6 `ui-components`

Enthält kleine, frameworkfreie und barrierearme Grundbausteine:

- Speicherstatus;
- Offline-/Verbindungsstatus;
- Fehlersummary;
- Import-, Export- und Löschdialoge;
- Updatehinweis;
- allgemeine lokale Datenkontrolle.

Die Komponenten bestehen aus Astro-Präsentationskomponenten, semantischem HTML, CSS und gezielt angebundenen TypeScript-Controllern. Es gibt kein JSX, keine virtuelle DOM-Laufzeit und keine versteckte globale Zustandsverwaltung.

### 7.7 `lernwerk-portal`

Das Portal komponiert die Pakete und erzeugt:

- öffentliche Start- und Informationsseiten;
- einen ehrlichen Leerzustand, solange keine fachlichen Module existieren;
- später statische Katalog- und Modulrouten aus dem generierten Register;
- PWA-Manifest, Service-Worker-Registrierung und Updateoberfläche;
- korrekte Asset-, Route-, Manifest- und Service-Worker-Pfade sowohl am Domainroot als auch unter einem konfigurierten statischen Unterpfad;
- eine lokale Datenverwaltung.

## 8. Modulmanifest

`module.yaml` ist die prüfbare Beschreibung eines fachlichen Moduls, nicht der vollständige Inhalt des Lehrkräftehandbuchs. Das Manifest besitzt mindestens diese geschlossenen Bereiche:

| Bereich | Inhalt |
|---|---|
| `schemaVersion` | Version des Manifestvertrags |
| `id`, `version`, `title` | stabile Identität und Modulversion |
| `status` | `draft`, `working`, `reviewed` oder `standard` |
| `grade`, `kind`, `strands` | Jahrgang, Kern-/Erweiterungs-/Transfer-/Projektart und Lernstränge |
| `time` | minimaler und maximaler Unterrichtsrahmen sowie Zeitvertragsreferenz |
| `prerequisites` | vorausgesetzte Module und Fähigkeiten |
| `curriculum` | existierende Curriculum-, Kompetenz- und Coverage-Referenzen |
| `learningDesign` | Leitfrage, Lernziele, zentrale Lernhandlungen, Lernprodukt, Fehlvorstellungen und Scaffolds |
| `components` | tatsächlich benötigte interaktive Laufzeitkomponenten |
| `media` | digitale Lernfunktion und begründete analoge Materialien |
| `data` | Dateninventar, Zustandsschema, Export- und Löschbarkeit |
| `offline` | Kernpfad, optionale Onlineanteile und Fallbacks |
| `accessibility` | Bedienalternativen und modulspezifische Prüferfordernisse |
| `licenses` | Inhalts-, Code- und Assetnachweise |
| `quality` | Referenzen auf fachliche, didaktische, technische und reale Prüfnachweise |

Für jedes analoge Material verlangt `media.analogMaterials` mindestens Zweck, fachliche oder lernpsychologische Begründung und Rückkehr in den gemeinsamen Lernprozess. Ohne einen solchen Eintrag wird kein `print/`-Ordner angelegt.

Die Statusfolge ist keine bloße Beschriftung. Ein höherer Status ist nur zulässig, wenn die dafür vorgeschriebenen Nachweise existieren. Die Plattform erzeugt oder erhöht keinen Status automatisch.

## 9. Manifest- und Buildfluss

Der Produktionsbuild besitzt einen fest verdrahteten Quellenpfad `modules/`. Der Fixture-Build besitzt einen getrennten fest verdrahteten Quellenpfad `tests/fixtures/reference-module/`. Ein beliebiger Produktionspfad aus einer unkontrollierten Umgebungsvariable ist unzulässig.

```text
module.yaml und Moduldateien
→ JSON-Schema-Prüfung
→ semantische Referenzprüfung
→ Pfad-, Lizenz- und Abhängigkeitsprüfung
→ deterministisch generiertes Modulregister
→ statische Astro-Routen
→ Asset- und PWA-Build
→ Qualitätsgates
```

Das Modulregister wird nie manuell bearbeitet. Gleiche Quellen und gleiche Werkzeugversionen müssen byteidentische Registries erzeugen.

Produktions- und Fixture-Profil sind getrennt:

- Produktionsprofile akzeptieren nur reguläre Modul-IDs und reale Curriculumreferenzen.
- Fixture-Profile verlangen den reservierten Präfix `TEST-` und synthetische Referenzen unter `tests/fixtures/curriculum/`.
- Das Fixture-Profil speist ein synthetisches, strukturell vollständiges Manifest einschließlich eines Testwerts für das Pflichtfeld `status` ein. Dieser Wert prüft nur den Manifestvertrag; er wird weder publiziert noch als Status der Fixture oder des Lernwerks gewertet.
- Ein `TEST-`-Eintrag im Produktionsregister oder ein reales Curriculumziel im Fixture-Ergebnis ist ein harter Fehler.
- Fixture-Ergebnisse werden niemals in Coverage- oder Statusberichte eingerechnet.

## 10. Lernstandsvertrag

Ein Lernstand verwendet folgende Hülle:

```json
{
  "format": "ium-learning-state",
  "formatVersion": 1,
  "moduleId": "TEST-PLATFORM-REFERENCE",
  "moduleVersion": "1.0.0",
  "stateSchemaVersion": 1,
  "workspaceId": "zufällige UUID",
  "savedAt": "RFC-3339-Zeitpunkt",
  "payload": {}
}
```

Regeln:

- `workspaceId` ist zufällig und enthält keine Identitätsinformation.
- Es gibt keine verlangten Namen, E-Mail-Adressen, Klassenkennungen, Gerätekennungen oder Nutzerprofile.
- Pro Modul existiert im Browser genau ein aktiver Arbeitsstand. Ein Import ersetzt ihn erst nach Vorschau und Bestätigung.
- Ein neuer Arbeitsstand verlangt vorher eine bewusste Entscheidung zum Export oder Löschen des alten Zustands.
- Fachliche Nutzdaten liegen ausschließlich in `payload` und werden gegen das versionierte Zustandsschema des Moduls validiert.
- Zustände anderer Module dürfen weder gelesen noch überschrieben werden.
- Freitext kann freiwillig personenbezogene Angaben enthalten. Die Plattform behauptet deshalb nicht, alle lokalen Inhalte seien anonym; Module sollen solche Eingaben weder verlangen noch nahelegen.

## 11. Speicherzustände

Die Laufzeit unterscheidet mindestens:

| Zustand | Bedeutung | Oberfläche |
|---|---|---|
| `persistent` | IndexedDB-Schreiben wurde bestätigt | lokales Speichern sichtbar bestätigt |
| `volatile-selected` | Nutzung ohne dauerhafte Speicherung wurde bewusst gewählt | dauerhafter Hinweis „nur diese Sitzung“ |
| `volatile-fallback` | dauerhafte Speicherung ist technisch fehlgeschlagen | deutliche Warnung und Exportangebot |

Die Plattform darf `navigator.storage.persist()` und `estimate()` als Best-Effort-Signale verwenden. Eine erteilte Persistenzberechtigung ist kein Versprechen gegen Geräteverlust, Browserbereinigung oder schulische Richtlinien. Export und Löschung bleiben daher immer sichtbar erreichbar.

## 12. Speichern, Exportieren, Importieren und Löschen

### 12.1 Speichern

```text
Lernhandlung
→ fachliche Eingabeprüfung
→ neuer versionierter Zustand
→ atomarer Schreibversuch
→ bestätigter Speicherstatus oder sichtbarer flüchtiger Modus
```

Ein angezeigtes „gespeichert“ setzt den erfolgreichen Abschluss der IndexedDB-Transaktion voraus. Optimistische Erfolgsanzeigen vor dem Commit sind unzulässig.

### 12.2 Export

Der Export erzeugt UTF-8-JSON mit der dokumentierten Lernstandshülle. Der Dateiname lautet ohne Personen- oder Arbeitsstand-ID:

```text
ium-<module-id>-<YYYY-MM-DD>.json
```

Wenn ein eingebetteter Browser den Dateidownload blockiert, wird derselbe validierte Inhalt als fokussierbarer, kopierbarer Text angeboten. Die Oberfläche weist darauf hin, dass eine Exportdatei eigene Arbeitsergebnisse enthalten und entsprechend geschützt werden kann.

### 12.3 Import

```text
Datei auswählen
→ maximale Größe 5 MiB prüfen
→ UTF-8 und JSON parsen
→ geschlossene Hülle validieren
→ Modul- und Versionsbezug prüfen
→ auf einer Kopie migrieren
→ fachliche Nutzdaten validieren
→ verständliche Vorschau
→ Bestätigung
→ atomar ersetzen
```

Unbekannte Felder, falsche Modul-IDs, nicht unterstützte Zukunftsversionen, übergroße Dateien oder ungültige Nutzdaten werden fail-closed abgelehnt. Ein fehlgeschlagener Import verändert den vorhandenen Zustand nicht.

### 12.4 Löschen

Die Oberfläche bietet:

- Löschen des aktiven Arbeitsstands eines Moduls;
- Löschen aller lokalen IuM-Lernwerkdaten über die Portal-Datenverwaltung.

Nach bestätigtem Löschen wird der Zustand erneut gelesen. Erst wenn er nicht mehr vorhanden ist, meldet die Oberfläche Erfolg.

## 13. Offlinevertrag

Offlinefähigkeit beginnt nicht mit einem App-Manifest, sondern mit bestandenen Nutzungsszenarien.

### 13.1 Zustände

- `not-ready`: Die für den Kernpfad benötigten Ressourcen sind noch nicht vollständig zwischengespeichert.
- `ready`: Der vollständige Kernpfad des aktuellen Releases wurde erfolgreich zwischengespeichert.
- `offline`: Die Anwendung arbeitet aus dem bestätigten Cache; lokale Arbeit, Import und Export bleiben verfügbar.
- `degraded`: Ein gekennzeichneter externer Onlineanteil fehlt, der Kernpfad bleibt jedoch nutzbar.

Ein erster, noch nie zuvor geladener Aufruf ohne Netz kann von der Anwendung technisch nicht kontrolliert werden, weil noch kein Service Worker oder Fallback vorhanden ist. Die Plattform behauptet für diesen Fall keine eigene Fehlermeldung. Sobald ein Shell-Cache existiert, führen unbekannte oder nicht zwischengespeicherte Offlinepfade zu einer lokalen verständlichen Offlineerklärung statt zu einer leeren Oberfläche.

### 13.2 Cachegrenze

- Portal-Shell, benötigte lokale Assets und eingeschlossene Kernpfade werden vollständig vorab gecacht.
- Externe Quellen werden nicht stillschweigend in den Kerncache aufgenommen.
- Drittanbieter-Skripte, -Fonts, -Tracker und CDN-Ressourcen sind im Kernpfad verboten.
- Eine sichtbare „offline bereit“-Meldung erscheint erst nach vollständigem erfolgreichen Precache.
- Installation als App und funktionierender Offlinebetrieb werden getrennt geprüft.

## 14. Updatevertrag

Jeder Build besitzt eine eindeutige Release-ID. Assets sind inhaltsgehasht; Einstiegspunkte und Service Worker werden kontrolliert revalidiert.

```text
neuen Service Worker finden
→ vollständigen neuen Cache aufbauen
→ bei Fehler Installation abbrechen und alten Worker aktiv lassen
→ neuen Worker wartend halten
→ Updatehinweis anzeigen
→ offene Zustandsänderungen speichern
→ bewusste Bestätigung
→ neuen Worker aktivieren
→ Seite kontrolliert neu laden
→ Zustand bei Bedarf migrieren
```

Verbindliche Regeln:

- kein automatisches `skipWaiting()` beim Fund einer neuen Version;
- kein automatisches Neuladen während einer Lernhandlung;
- kein Löschen des funktionierenden alten Caches vor vollständig erfolgreicher Installation des neuen Releases;
- keine gemischte Auslieferung aus unvereinbaren Releasecaches;
- ein fehlgeschlagenes Update wird lokal gemeldet und nicht telemetrisch übertragen;
- ein Deployment-Rollback erscheint technisch als neues Release und darf lokale Zustandsschemata nicht still zurückstufen.

## 15. Migration und Wiederherstellung

Zustandsmigrationen sind explizit, schrittweise und vorwärtsgerichtet:

```text
Original lesen
→ unveränderte Sicherung im Speicher halten
→ Kopie n → n+1 migrieren
→ jeden Zwischenschritt validieren
→ Zielzustand validieren
→ atomar speichern
→ erst danach Original ablösen
```

Eine Modulversion muss alle im freigegebenen Supportfenster vorhandenen Zustandsschemata entweder migrieren oder mit einer verständlichen Inkompatibilitätsmeldung ablehnen. Bei einem Migrationsfehler bleibt das Original unverändert exportierbar. Die Oberfläche bietet dann nur:

- Original exportieren;
- Migration erneut versuchen, wenn der Fehler behebbar ist;
- nach ausdrücklicher Bestätigung einen neuen Zustand beginnen.

Ein beschädigter Zustand wird niemals still gelöscht oder mit einem leeren Zustand überschrieben.

## 16. Fehlervertrag

Die öffentliche Laufzeit verwendet mindestens diese stabilen Fehlercodes:

- `STORAGE_UNAVAILABLE`
- `STORAGE_QUOTA`
- `STORAGE_WRITE_FAILED`
- `IMPORT_TOO_LARGE`
- `IMPORT_INVALID`
- `IMPORT_WRONG_MODULE`
- `IMPORT_UNSUPPORTED_VERSION`
- `MIGRATION_FAILED`
- `OFFLINE_NOT_READY`
- `UPDATE_INSTALL_FAILED`

Jeder Fehler besitzt:

- eine kurze verständliche deutsche Meldung;
- eine konkrete nächste Handlung;
- eine maschinenlesbare Fehlerkennung;
- optional aufklappbare technische Details ohne standardmäßig sichtbaren Roh-Stacktrace.

Fehler werden lokal angezeigt und nicht übertragen. Die Anwendung nutzt Feature-Erkennung statt ausschließlich Browsernamen. Fehlen nicht wesentliche Funktionen, bleiben statische Orientierung und Kerninformationen zugänglich. Fehlt eine notwendige Speicherfunktion, bleibt die Interaktion im gekennzeichneten flüchtigen Modus nutzbar.

## 17. Barrierefreiheits- und Bedienvertrag

WCAG 2.2 AA ist verbindliches technisches Ziel, ersetzt aber keine Prüfung mit realen Lernaufgaben.

Alle Phase-1-Grundkomponenten erfüllen mindestens:

- vollständige Tastaturbedienung ohne Maus- oder Drag-Zwang;
- sichtbare, logisch geführte Fokusreihenfolge;
- semantische Überschriften, Regionen, Formulare und Schaltflächen;
- programmatisch zugeordnete Beschriftungen, Hinweise und Fehlermeldungen;
- verständliche Statusmeldungen über angemessen zurückhaltende Live-Regionen;
- Reflow bei 320 CSS-Pixeln und Textzoom bis 200 Prozent;
- ausreichenden Kontrast und keine alleinige Farbcodierung;
- Unterstützung von `prefers-reduced-motion`;
- ausreichend große und voneinander getrennte Bedienziele;
- verständliche Sprache für die Zielgruppe;
- bedienbare Alternativen für jede spätere Canvas-, Sortier- oder Zeigerinteraktion.

Phase 1 verwendet Systemschriften. Eine visuelle Markenbibliothek und dekorative Animationen sind nicht Teil des Scopes.

## 18. Technische Referenz-Fixture

Die Fixture heißt `TEST-PLATFORM-REFERENCE` und ist ausdrücklich kein Lernmodul. Sie enthält nur die kleinste Interaktion, die alle Plattformverträge prüft:

1. eine kurze synthetische Texteingabe;
2. eine Auswahl mit Validierungszustand;
3. sichtbaren Speicherstatus;
4. Neuladen und Wiederherstellen;
5. Export;
6. Löschen;
7. Import;
8. Wechsel in den flüchtigen Modus;
9. Offlinefortsetzung;
10. kontrolliertes Update mit einer testbaren Zustandsmigration.

Die Fixture:

- verwendet nur `TEST-`-IDs;
- referenziert ausschließlich synthetische Curriculum-Fixtures;
- führt im synthetischen Manifest einen reinen Testwert für das Pflichtfeld `status`, erzeugt daraus aber keinen Produkt- oder Modulstatus;
- erscheint nur im expliziten Fixture-Build;
- erscheint nie im Produktionskatalog;
- erzeugt keine Coverage-, Modulstatus- oder Pilotwerte;
- verwendet keine reale Schüler-, Lehrkraft- oder Unterrichtssprache, die als fertiges Material missverstanden werden kann.

## 19. Automatisierte Qualitätssicherung

Jeder Pull Request und jeder Build auf `main` durchläuft mindestens:

### 19.1 Vertrags- und Strukturtests

- gültige und gezielt ungültige Manifest-Fixtures;
- geschlossene Schemas und Ablehnung unbekannter Felder;
- Referenzintegrität und reservierte ID-Namensräume;
- deterministisches Register;
- synchronisierte Schemata, Typen und Validatoren;
- gerichtete, zyklusfreie Paketabhängigkeiten.

### 19.2 Unit-Tests

- IndexedDB- und In-Memory-Adapter;
- bestätigte Transaktionen und Fehlerfälle;
- Export, Import, Größenlimit und Löschung;
- jede Zustandsmigration;
- Fehlerklassifikation und nutzerverständliche Folgeschritte;
- reine Modul-Runtime-Anwendungsfälle.

### 19.3 Browsertests

Chromium, Firefox und WebKit prüfen:

- Portalnavigation und Leerzustand;
- vollständige Tastaturbedienung;
- Bearbeiten, Speichern, Neuladen und Wiederherstellen;
- Export–Löschen–Import;
- flüchtigen Modus und Speicherfehler;
- eingebettete Nutzung mit blockiertem Speicher oder Download und den vorgesehenen Fallbacks;
- einen statischen Unterpfad-Build ohne harte Root-URL-Annahmen;
- Reflow und zentrale responsive Zustände.

### 19.4 Offline- und Updatetests

- erster Fixture-Build online und danach offline;
- Netzverlust während einer Interaktion;
- Offline-Import und -Export;
- unvollständige Cacheinstallation;
- wartender neuer Service Worker;
- bewusste Aktivierung;
- Zustandsschemamigration;
- Rückkehr online;
- unbekannter Offlinepfad mit lokaler Erklärung;
- korrekten Service-Worker-Scope und Cachezugriff unter einem statischen Unterpfad;
- Trennung von Produktions- und Fixture-Cache.

Playwright automatisiert Service-Worker-Inspektion nur in Chromium. WebKit-/Safari-Offlinenachweise werden deshalb nicht durch einen grünen Chromium-Test ersetzt.

### 19.5 Accessibility

- automatisierte WCAG-2.2-AA-Prüfung jeder Phase-1-Route;
- Tastatur-, Fokus-, Fehler- und Statusaufgaben;
- Reflow, Zoom, Kontrast und reduzierte Bewegung;
- manuelle Screenreader-Aufgaben mit NVDA oder vergleichbarer Desktopkombination sowie VoiceOver auf dem realen iPad.

### 19.6 OER, Sicherheit und Reproduzierbarkeit

- vollständige Lizenz- und Assetmetadaten;
- kompatible Abhängigkeitslizenzen;
- keine Drittanbieterrequests im Kernpfad;
- keine Telemetrie, Tracker, Secrets oder lokalen Runtime-Dateien;
- keine dynamische Codeausführung aus Importdaten;
- Lockdatei und reproduzierbarer `npm ci`-Build;
- Dependency- und Sicherheitsprüfung;
- maschinenlesbare Abhängigkeitsübersicht beziehungsweise SBOM.

## 20. Performance- und Offlinebudgets

Für Portal plus Fixture-Build gelten:

| Budget | Grenze | Messung |
|---|---:|---|
| kalter Ersttransfer | höchstens 250 KiB | Summe der gzip-komprimierten ersten HTML-, CSS-, JS- und notwendigen Iconantworten |
| initiales Plattform-JavaScript | höchstens 100 KiB | gzip-komprimierte, beim ersten Aufruf geladene JS-Ressourcen |
| Offline-Kernumfang | höchstens 2 MiB | Summe der dekodierten, für Portal und Fixture vorab gecachten Ressourcen |
| Drittanbieterrequests | genau 0 | Netzwerkprotokoll des Kernpfads |

Spätere fachlich begründete Simulationen erhalten eigene Modulbudgets. Sie dürfen die Plattformbudgets nicht still verändern.

## 21. Browser- und Realgerätematrix

Automatisierte Browserläufe verwenden zum Implementierungszeitpunkt konkret protokollierte Hauptversionen von Chromium, Firefox und WebKit. Formulierungen wie „aktueller Browser“ genügen nicht als Prüfnachweis.

Die reale Phase-1-Prüfung umfasst mindestens:

- ein verwaltetes schulisches iPad mit dokumentierter iPadOS-/Safari-Version, Web-Clip-, Speicher- und Filterpolicy;
- einen aktuellen Chromium-Browser auf einem schulisch relevanten Desktop- oder Notebookbetriebssystem;
- einen aktuellen Firefox-Browser;
- VoiceOver auf dem iPad und einen benannten Desktop-Screenreaderpfad;
- Online-, Offline-, Speicher-, Export-, Import- und Updateaufgaben mit der Fixture.

Ein fehlender Zugang zu einem verwalteten Schul-iPad wird als offenes Gerätegate dokumentiert und nicht durch Browseremulation umgedeutet.

## 22. Reifestufen und Definition of Done

Phase 1 verwendet drei technische Nachweisstufen. Diese Stufen beschreiben das Projektfundament und sind keine zusätzlichen Modulstatus:

### 22.1 `specified`

- diese Spezifikation ist schriftlich freigegeben;
- ein testgetriebener Implementierungsplan liegt vor.

### 22.2 `implemented`

- alle geplanten Quellen sind umgesetzt;
- sämtliche automatisierten Gates bestehen auf dem committed Hauptstand;
- Fixture-Build und Produktions-Leerbuild sind reproduzierbar;
- keine fachlichen Module oder Statusänderungen wurden eingeführt;
- Dokumentation erklärt lokale Entwicklung, Build, Datenlöschung, Offlinegrenzen und QA.

### 22.3 `device-verified`

- die reale Zielmatrix ist mit Datum, Versionen, Policy und Aufgaben dokumentiert;
- alle verpflichtenden iPad-, Desktop-, Screenreader-, Offline- und Updateaufgaben bestehen;
- verbleibende Einschränkungen sind entweder behoben oder als ausdrückliches späteres Gate akzeptiert.

Phase 1 ist erst abgeschlossen, wenn `implemented` und `device-verified` vorliegen. Ein grüner CI-Lauf allein genügt nicht.

## 23. Hohe Implementierungsreihenfolge

Der spätere TDD-Plan muss diese Abhängigkeit einhalten:

```text
Workspace und kanonische Verträge
→ Manifestvalidierung und Fixture-Isolation
→ Portal-Leerzustand und Fixture-Route
→ Local-State-Adapter und Runtime
→ Export, Import und Löschung
→ barrierearme UI-Grundkomponenten
→ Service Worker, Offline- und Updatevertrag
→ vollständige automatische Gates
→ dokumentierter Produktions- und Gerätehandoff
```

Diese Reihenfolge ist noch kein Implementierungsplan. Erst nach schriftlicher Freigabe dieser Spezifikation wird sie mit `superpowers:writing-plans` in kleine testgetriebene Tasks, Dateien, Befehle und Reviewpunkte zerlegt.

## 24. Risiken und Gegenmaßnahmen

| Risiko | Gegenmaßnahme |
|---|---|
| Phase 2 beginnt verdeckt in Phase 1 | ausschließlich synthetische Fixture; `modules/` bleibt ohne Fachmodul |
| Manifest wird zur unwartbaren Gesamtdatenbank | nur strukturierte, prüfbare Metadaten; ausführliche Inhalte bleiben in Moduldateien und Handbuch |
| Schema und TypeScript driften auseinander | ein kanonisches JSON-Schema, generierte Typen und CI-Driftgate |
| lokaler Speicher wird als sicher garantiert | sichtbarer Speicherstatus, Export und dokumentierte Eviction-/Policygrenzen |
| fehlerhaftes Update zerstört Arbeit | wartender Worker, bewusste Aktivierung, atomare Migration und unverändertes Original bei Fehler |
| grüner Chromium-Test wird als iPad-Nachweis ausgegeben | getrennte Stufen `implemented` und `device-verified` |
| Fixture erscheint als Unterrichtsmaterial | reservierter Namensraum, getrennte Quellenwurzel und Produktions-Fail-closed-Gate |
| Accessibility wird nur automatisiert geprüft | verpflichtende Tastatur-, Screenreader-, Reflow- und Realgeräteaufgaben |
| spätere Komponenten erzwingen ein frühes Framework | frameworkfreie Basis; neue Laufzeit nur nach konkretem Phase-2-Lernbedarf |
| Import wird zur Code- oder HTML-Einschleusung | geschlossene Datenschemata, reine Datenbehandlung und keine dynamische Codeausführung |

## 25. Primäre technische Referenzen

Aktuell geprüft am 2./3. August 2026:

1. Astro, *Content Loader API*: https://docs.astro.build/en/reference/content-loader-reference/
2. npm, *Workspaces*: https://docs.npmjs.com/cli/using-npm/workspaces/
3. Vite PWA, *Framework-agnostic setup*: https://vite-pwa-org.netlify.app/frameworks/
4. Vite PWA, *Advanced injectManifest*: https://vite-pwa-org.netlify.app/guide/inject-manifest
5. Jake Archibald, *idb – IndexedDB with usability*: https://github.com/jakearchibald/idb
6. MDN, *StorageManager*: https://developer.mozilla.org/en-US/docs/Web/API/StorageManager
7. MDN, *Service Worker API*: https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API
8. Playwright, *Service Workers*: https://playwright.dev/docs/service-workers
9. Vitest, *Browser Mode*: https://vitest.dev/guide/browser/
10. W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*: https://www.w3.org/TR/WCAG22/

Die Referenzen begründen technische Fähigkeiten und bekannte Testgrenzen. Sie ersetzen nicht die schulische Realgeräteprüfung, die rechtliche Prüfung des späteren konkreten Hostings oder eine fachlich-didaktische Modulprüfung.

## 26. Schriftliches Freigabegate

Mit Freigabe dieser Spezifikation werden ausschließlich Ziel, Scope, Architektur, Verträge, Fehlerverhalten und Abnahmekriterien von Phase 1 verbindlich.

Die Freigabe startet noch keine Implementierung. Der nächste zulässige Schritt ist ein detaillierter testgetriebener Implementierungsplan. Reale Unterrichtspilotierung, fachliche Modulproduktion, Release und Statushochsetzung bleiben separate spätere Aufträge.
