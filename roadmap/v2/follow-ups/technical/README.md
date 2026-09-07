# IUM-V2-FU-TECH – technische Übernahmeprüfung

**Fortschreibung vom 07.09.2026:** Der Nutzer hat den Audit an Commit `69634c56d3d100d3bf33632f29a4f98eaf579276` angenommen (`done`) und FU-MOD anschließend ausdrücklich beauftragt. [Abnahmebeleg](acceptance.json). Die acht Befunde und Einsatzgrenzen bleiben offen; keine technische Reparatur wurde beauftragt. Die folgenden Abschnitte dokumentieren den historischen Abgabestand vom 06.09.2026.

Stand: 6. September 2026. **Audit zur Nutzerabnahme (`review`); technische Wiederverwendung nur nach den beschriebenen Anpassungen.** Der Auftrag ist ausgeführt, die gefundenen Produktlücken sind nicht behoben. Ein dokumentarischer Abschluss dieses Audits würde keine der offenen technischen oder institutionellen Einsatzbedingungen erfüllen.

Geprüfter Repositoryinput: `32b523a657a3e6717a83fd9aaa755c8deed9adbf`, Branch `feat/ium-v2-rebaseline`. 52 einzeln benannte Dateien aus IUM04, IUM12, IUM13 und IUM18: **13 retain, 31 adapt, 8 reference-only**. `retain` meint ausschließlich die im Inventar beschriebene technische Funktion. Das ist weder die Auswahl eines V2-Moduls noch eine Freigabe zur unveränderten Produktübernahme.

## Ergebnis und Unterlagen

- [Dateiinventar mit Begründung, Zeilenanker, Inputhash und Migrationszuordnung](inventory.json)
- [Lesbare Dateimatrix](inventory.md)
- [Acht Befunde und konkrete Abnahmetests für Nacharbeiten](findings.md)
- [Tatsächlich ausgeführte Prüfungen und offene reale Nachweise](validation-report.md)
- [Reproduzierbarer synthetischer Befundlauf](probe.mts) und [beobachtete Ergebnisse](probe-results.json)

Die technische Pakettrennung, geschlossene Importhülle, kopierende Speichermodelle, deterministische Algorithmussemantik und statische Auslieferung sind brauchbarer Bestand. Der Prüflauf zeigt zugleich echte Daten-/Versionslücken und fehlende V2-Vertragsbindung. Ein grüner V1-Testbestand allein hätte diese Lücken nicht ausgeschlossen.

## Prüfauftrag und Statusführung

Der ausdrückliche Auftrag lautet „Führe IUM-V2-FU-TECH aus“. CUT ist abgeschlossen und V2 als Planungs-/Entwicklungsbaseline aktiv. Der frühere `blocked-follow-up`-Eintrag in `../../audits/follow-up-tasks.json` bleibt ein versiegelter historischer Planungsbeleg. Der aktuelle Zustand steht in dieser additiven Folgeprüfung und der gleichnamigen Workspace-Task-Notiz. AUD, CUT und Aktivierung werden nicht nachträglich neu versiegelt.

V1 bleibt der bestehende Produktstand. Alle 18 Re-Baseline-Gates bleiben abgeschlossen. Inhaltsproduktion bleibt eingefroren, LXP05 unintegriert, Pilot `not-started`, reale V2-Geräteprüfung `not-run`. FU-MOD und FU-PILOT benötigen weiterhin ihre eigenen Nutzeraufträge. Dieses Audit hat keine Produktdateien migriert, keinen Workflow gestartet und nichts veröffentlicht.

## Geordneter Migrationsweg

| Schritt | Betroffene Grenze | Erforderliche Änderung / Abschlussnachweis |
| --- | --- | --- |
| M01 | IUM04, Rechte, Betriebsbeschreibung | Quellenstand und konkrete Betriebs-/Datenflussbeschreibung abgleichen. Rollen, Rechts-/Rechteprüfung und Auslieferungsort dokumentieren; offene GOV-Fragen erhalten. |
| M02 | Runtime, Hülle, Import und Recovery | Gleiche Modul-/Versions-/Schema-/Payloadvalidierung für Load und Import. Supportmatrix explizit festlegen; Original bei Migrationsfehler unverändert exportierbar halten. Pending-Import bei Fehler/Abbruch/Löschen entwerten. F01–F03 mit Negativtests schließen. |
| M03 | Speicher, Browserports und Datenkontrolle | Vor erstem Schreiben die Speicherwahl klären. Ein- oder Mehrinstanzvertrag mit Konflikt-/Löschschutz schaffen. Export-, Clipboard- und Profilwechselpfade korrekt beschreiben. F04/F05 schließen. |
| M04 | Updateorchestrierung | Update bei flüchtigem oder nicht gesichertem Stand durch Sicherung/Abbruch absichern. Mehrere offene Clients und abgelehnte Flush-Promises testen. F06 schließen. |
| M07 | Neues Modulmanifest, Registry, Adapter | Aus einem freigegebenen FU-MOD-Design einen eigenen V2-Vertrag ableiten: Lernfunktionen, Pattern, Hilfen, Produkte, Feedback, Wiedereinstieg, getrennte Reifeachsen und Coveragebelege. Fachlogik selektiv einbinden; V1-IDs/UE-Phasen nicht umetikettieren. F07 schließen. |
| M05 | Build, CI und Auslieferung | Explizites V2-Buildziel, geprüfter Node/npm-Stand und V2-/Aktivierungs-/Produktgates; Plattform- und neue Modulprüfungen vollständig wiederholen. F08 nachweisen. |
| M06 | Reale Zielumgebung | Konkreten Kandidaten auf tatsächlichen Geräten, Policies, Schulnetz und LMS mit Datenschutz-/Rechtenachweisen prüfen. FU-PILOT erstellt seine Instrumentbindung in eigenem Auftrag. |

`M00` im Inventar bedeutet begrenzte Beibehaltung ohne Änderung im Audit. Auch diese Dateien müssen bei einer späteren Einbindung mit dem tatsächlichen V2-Modul getestet werden. M02–M04 lassen sich technisch vorbereiten, bevor ein Modul gebaut wird; M07 benötigt dessen fachliches Design. Kein Schritt in dieser Tabelle gilt bereits als beauftragt oder implementiert.

**Versionsentscheidung zur Abnahme:** Keine automatische Migration von `IUM-5-CORE-05` 0.1.0 / Payloadschema 1 in ein neues V2-Modul. Formatversion, Modulidentität/-version, Payloadschema, IndexedDB-Datenbankschema und Service-Worker-/Buildrevision sind unterschiedliche Achsen. Ein späterer Migrationsvertrag muss jede unterstützte Kombination benennen und nicht unterstützte Stände verlustfrei ablehnen. Die Planungsbezeichnung V2 erzwingt für sich allein keine neue Exportformatnummer.

## GOV und tatsächliche Datenflüsse

| Datenfluss | Technischer Befund | Verantwortliche Rolle / gesperrter Einsatz |
| --- | --- | --- |
| Portalaufruf → Host/Proxy | Kein Applikationskonto und keine persönliche Telemetrie im geprüften Kern. Hosting-, Proxy- und LMS-Protokolle sind damit nicht ausgeschlossen. | `GOV-Q-OPERATOR`: Jan koordiniert Betreiber/Hosting und Datenschutzreview vor öffentlichem Betrieb. |
| Lernhandlung → RAM oder IndexedDB | Freitexte und Lernprodukte können sensibel sein; Standardpfad schreibt lokal. Ein Slot pro Modul/Origin; andere Personen im selben Profil können ihn wiederfinden. | `GOV-Q-SCHOOL`: Schule/verantwortliche Stelle legt Zweck, Profilmodell, Zugriff, Information und Löschfrist vor Nutzung fest. TECH-F04/F05 zuvor schließen. |
| Export → Download oder Zwischenablage | Expliziter Export; Browserport versucht bei Downloadblockade automatisches Clipboard-Schreiben und zeigt Kopierfeld. Dateien/Clipboard können geräte- oder kontobedingt synchronisiert werden. | Datenschutzreview muss Downloadziel, Clipboard-/Gerätesync, LMS-Weitergabe und Löschgrenzen bestätigen. App-Löschen entfernt keine Exportkopien. |
| App-Löschen → aktueller Speicher | Lokaler Store wird gelöscht; offene andere Runtime-Instanzen können alte Daten zurückschreiben. Browsercache/Service Worker und externe Kopien sind andere Speicher. | TECH-F04; Betrieb erst mit überprüftem Lösch-/Mehrtabvertrag. |
| Asset/Code → Build → Browsercache | Eigener Code MIT, eigene Inhalte CC BY-SA 4.0 nach bestehendem Rahmen; Dependencyprüfung ist keine Inhaltsrechteprüfung. | `GOV-Q-RIGHTS`: Rechteprüfende bestätigen Quelle, Urheber, Lizenz/Erlaubnis, Bearbeitung und Auslieferungsort konkreter Assets/Logos. |
| Produkt → Nutzungs-/Pilotbeobachtung | Kein FU-TECH-Einsatz mit Lernenden, keine neuen realen Daten erhoben. | `GOV-Q-REVIEWERS`, `GOV-Q-SCHOOL` und CUR-Q-002 bleiben offen. Prüfende und geschützte Belegablage vor betroffenem Einsatz bestimmen. |

Diese Rollenklärung benennt die noch benötigten Nachweise; sie behauptet keine bereits erteilte Betreiber-, Schul-, Datenschutz- oder Rechtefreigabe. Ohne sie bleibt der jeweilige Betrieb gesperrt. CUR-Q-002 und die weiteren Eigenbezugsfragen werden nicht durch technische Datensparsamkeit oder fiktive Beispiele geschlossen.

## Anlassbezogener Quellenrecheck

Am 06.09.2026 wurden folgende Primärquellen erneut online gelesen. Das ist ein begrenzter Technik-/GOV-Recheck, keine erneute Vollprüfung sämtlicher 18 IUM04-Quellen. Historische Claims werden nicht geändert. Die folgenden Folgerungen sind die Einordnung dieses Audits.

| Primärquelle | Aussagegrenze und Folge |
| --- | --- |
| [WHATWG Storage Standard](https://storage.spec.whatwg.org/) | Living Standard, ausgewiesener Stand 15.03.2026. Browserpersistenz und erfolgreicher IndexedDB-Schreibvorgang sind verschiedene Begriffe; lokale Speicherung darf nicht als garantierte dauerhafte Sicherung erscheinen. |
| [WebKit Storage Policy](https://webkit.org/blog/14403/updates-to-storage-policy/) | Herstellerbeitrag vom 10.08.2023, ausdrücklich ab Safari 17. Quota, Eviction und Framepartitionierung begründen reale Tests; kein Nachweis für das heute konkrete Schulgerät. |
| [W3C Service Workers](https://w3c.github.io/ServiceWorker/) | Beim Abruf Editor’s Draft vom 12.08.2026. Lifecycle-/Clientmodell ist technische Referenz, keine automatische Lernstandsmigration und keine Konformitätsfreigabe des Produkts. |
| [Apple: Filter content](https://support.apple.com/guide/deployment/filter-content-dep1129ff8d2/web) | MDM, Filter und globale Proxies können Zugriffe beeinflussen. Schulkonfiguration und LMS müssen tatsächlich geprüft werden. |
| [Node.js Releases](https://nodejs.org/en/about/previous-releases) | Node 22 beim Abruf als LTS geführt. Lokal geprüft: 22.23.2/npm 10.9.8; CI-Pin 22.20.0 bleibt ein anderer, hier nicht neu ausgeführter Stand. |
| [WCAG 2.2, Konformität](https://www.w3.org/TR/WCAG22/#conformance-reqs) | Konformität betrifft vollständige Seiten und Prozesse. Automatisierte Accessibilityfälle tragen allein keinen umfassenden WCAG-AA-Anspruch. |
| [CC BY-SA 4.0 Lizenztext](https://creativecommons.org/licenses/by-sa/4.0/legalcode.de) | Rechte und Bedingungen am jeweiligen Inhalt prüfen; Lizenzrahmen ersetzt keine Prüfung weiterer betroffener Rechte. |
| [Datenschutz an Schulen BW](https://it.kultus-bw.de/,Lde/Datenschutz%2Ban%2BSchulen) | Amtlicher Einstieg für die zuständige Betriebsprüfung. Dieser Audit entscheidet keine konkrete Rechtsgrundlage oder Anwendbarkeit im Einzelfall. |

## Empfohlene Abnahme

Den Audit als vollständige Bestands-/Migrationsbewertung annehmen, mit acht offen ausgewiesenen Befunden und den unveränderten Einsatzgrenzen. Danach einen konkret abgegrenzten technischen Nacharbeitsauftrag aus M02–M04/M05 entscheiden und FU-MOD gesondert beauftragen. Die Nutzerabnahme ist noch ausstehend. Reviewart: KI-Selbstprüfung, kein unabhängiger externer Review.
