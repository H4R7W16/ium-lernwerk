---
package: digitale-lernumgebungen-oer
status: curated
curated: 2026-07-28
source: ../raw/04-digitale-lernumgebungen-oer.md
---

# Digitale Lernumgebungen und OER für IuM 5–7

## Scope, Rechtsvorbehalt und Evidenzstatus

Dieses Paket kuratiert Anforderungen an ein öffentliches, statisch auslieferbares, konto- und backendfreies Lernwerk für schulische iPads und Desktopbrowser. Es trennt:

- **geltendes Recht und behördliche Orientierung** in EU beziehungsweise Deutschland;
- **normative technische Standards und fortgeschriebene Entwürfe**;
- **empirische Forschung** mit benannter Population und Kontext;
- **Projektentscheidungen** als Input für die Phase-1-Spezifikation.

Rechtsstand und schnell veränderliche Technikstände sind auf **2026-07-28** datiert. Der Bericht ist keine Rechtsberatung. Ob eine Vorschrift auf Betreiber, Schule, Hosting, lokale Speicherung oder einen konkreten Datenfluss anwendbar ist, bleibt einer zuständigen Einzelfallprüfung vorbehalten.

Alle vierzehn retained Claims `CLAIM-DLE-*` stehen im `claim-ledger.json` auf `reviewed`; keiner ist `standard`. Die achtzehn registrierten Quellen `SRC-DLE-*` wurden an ihren Originalfundstellen geprüft.

## Quellen- und Statusmatrix

| Quelle | Aussageart | Status / Herausgeber am 2026-07-28 | Verwendung |
| --- | --- | --- | --- |
| `SRC-DLE-WCAG22-2024` | technischer Standard | W3C Recommendation 12.12.2024, mit Errata | AA-Baseline, Tastatur, Touch, Fokus; keine Lernwirkung |
| `SRC-DLE-WAI-USERS-2020` | professionelle Orientierung | W3C WAI, aktualisiert am 05.05.2020 | Nutzerbeteiligung zusätzlich zur Standardprüfung |
| `SRC-DLE-GDPR-2016` | Recht, EU | geltende Verordnung (EU) 2016/679 | Datenminimierung, Art. 25 |
| `SRC-DLE-EDPB-DPBDD-2020` | Behördenleitlinie, EU | EDPB, finale Version 2.0 vom 20.10.2020 | Auslegung Datenschutz durch Technikgestaltung |
| `SRC-DLE-TDDDG-25-2024` | Recht, Deutschland | § 25 TDDDG, geltend; Einzelfallprüfung offen | Endgerätespeicherung und -zugriff |
| `SRC-DLE-WHATWG-STORAGE-2026` | technischer Living Standard | WHATWG, Stand 15.03.2026 | `best-effort`, Persistenz, Quota, Eviction |
| `SRC-DLE-WHATWG-HTML-STORAGE-2026` | technischer Living Standard | WHATWG, abgerufen 28.07.2026 | Policy-bedingter Speicherfehler |
| `SRC-DLE-SERVICE-WORKERS-2026` | technischer Entwurf | W3C Candidate Recommendation Draft 23.07.2026, work in progress | Offlinefähigkeit, Lifecycle, Cache |
| `SRC-DLE-APP-MANIFEST-2026` | technischer Entwurf | W3C Working Draft 23.07.2026, ausdrücklich instabil | Installationsmetadaten, keine Offlinezusage |
| `SRC-DLE-HTTP-CACHE-2022` | technischer Standard | IETF Standards Track, RFC 9111 / STD 98 | Frische, Revalidierung, Netzlast |
| `SRC-DLE-UNESCO-OER-2019` | internationale Empfehlung | UNESCO General Conference, 25.11.2019 | OER-Begriff und Nachnutzungsraum |
| `SRC-DLE-CC-BY-4` | Lizenztext | Creative Commons, kanonische Version 4.0 | BY-Nachnutzung und Attribution |
| `SRC-DLE-CC-BY-SA-4` | Lizenztext | Creative Commons, kanonische Version 4.0 | BY-SA-Nachnutzung und ShareAlike |
| `SRC-DLE-CC-COMPAT-2026` | fortschreibbare Lizenzorientierung | Creative Commons, abgerufen 28.07.2026 | versions- und richtungsspezifische Kompatibilität |
| `SRC-DLE-APPLE-RESTRICTIONS-2026` | Herstellerdokumentation | Apple, abgerufen 28.07.2026 | Safari-/Web-Clip-Einschränkung auf MDM-Geräten |
| `SRC-DLE-APPLE-WEBFILTER-2026` | Herstellerdokumentation | Apple, abgerufen 28.07.2026 | Filter- und Allowlist-Risiken |
| `SRC-DLE-WSG-DRAFT-2026` | nicht normativer Entwurf | W3C Group Note Draft 28.07.2026, nicht W3C-endorsed | vorsichtige Nachhaltigkeitscheckliste |
| `SRC-DLE-IPAD-REVIEW-2021` | systematischer Review | 43 Studien, davon 21 ausschließlich mit 9- bis 14-Jährigen; übrige mit teils breiteren Altersstichproben | gemischte und inkonsistente Befunde, keine Kausal- oder Nulleffektschätzung |

## Provenienz-Erratum zum versiegelten Rohbericht

Prompt und Rohbericht aus Commit `5687231` bleiben als Provenienzartefakte bytegenau unverändert. Der Rohbericht fasst die Population und das Ergebnis des iPad-Reviews zu breit: Nicht alle 43 eingeschlossenen Studien untersuchten ausschließlich 9- bis 14-Jährige, sondern nur 21; die übrigen schlossen teils breitere Altersstichproben ein. Die Ergebnisse sind als gemischt beziehungsweise inkonsistent zu beschreiben, nicht als kausaler Nullbefund. Zudem waren die meisten Studien explorativ und qualitativ, Interventionen häufig kurz; Längsschnitt- und Within-Subject-Experimente fehlten weitgehend. Für die Kuration ersetzen die korrigierte Quellenmatrix, der folgende Abschnitt zu `CLAIM-DLE-014` und der Claim-Ledger-Eintrag die zu breite Raw-Aussage.

## Retained Claims

### CLAIM-DLE-001 – WCAG 2.2 AA als technische Baseline, nicht als Gesamtwirksamkeitsnachweis

**Befund.** WCAG 2.2 ist eine W3C Recommendation mit testbaren, technologieunabhängigen Erfolgskriterien. W3C empfiehlt Version 2.2 für neue und aktualisierte Accessibility-Policies und erklärt zugleich, dass der Standard nicht jedes Bedürfnis von Menschen mit Behinderungen abdeckt.

**Geltung und Quelle.** Internationaler technischer Standard, Recommendation vom 12. Dezember 2024, Stand 2026-07-28. [Originalquelle](https://www.w3.org/TR/WCAG22/)

**Einschränkung.** AA-Konformität beweist weder altersangemessene schulische Usability noch fachliches Lernen. Die rechtliche Verbindlichkeit hängt von Betreiber, Veröffentlichung und anwendbarem Recht ab.

**Phase-1-Folge.** WCAG 2.2 AA wird vollständiges technisches Gate; Usability und Lernwirksamkeit erhalten getrennte Prüfungen.

### CLAIM-DLE-002 – Touch und Tastatur als gleichwertige Funktionspfade prüfen

**Befund.** WCAG 2.2 fordert unter anderem Tastaturbedienbarkeit nicht pfadabhängiger Funktionen, Ausstieg aus jeder Tastaturfalle, sichtbaren und nicht vollständig verdeckten Fokus, eine Ein-Zeiger-Alternative für nicht wesentliches Ziehen sowie mindestens 24 × 24 CSS-Pixel große Zeigerziele oder eine der normativ definierten Ausnahmen.

**Geltung und Quelle.** WCAG `2.1.1`, `2.1.2`, `2.4.7`, `2.4.11`, `2.5.7` und `2.5.8`; Level A beziehungsweise AA. [Originalquelle](https://www.w3.org/TR/WCAG22/)

**Einschränkung.** Die genannten Kriterien sind kein vollständiger Auszug aller AA-Anforderungen. „Touchfähig“ belegt keine Tastatur- oder Assistive-Technology-Bedienbarkeit.

**Phase-1-Folge.** Drag-and-drop, Canvas, Sortieren und Verbinden erhalten fachlich gleichwertige Alternativen. QA prüft vollständige Aufgabenpfade getrennt mit Tastatur, Touch und assistiven Technologien.

### CLAIM-DLE-003 – Standardprüfung durch echte Nutzeraufgaben ergänzen

**Befund.** W3C WAI empfiehlt, Menschen mit Behinderungen früh und über den Entwicklungsprozess hinweg einzubeziehen und Nutzerbeteiligung mit WCAG-Konformitätsprüfung zu kombinieren.

**Geltung und Quelle.** Professionelle WAI-Orientierung für Webprojekte, nicht Teil der normativen WCAG-Konformitätsanforderungen. [Originalquelle](https://www.w3.org/WAI/planning/involving-users/)

**Einschränkung.** Die Orientierung ist kein kontrollierter Wirksamkeitsnachweis und nennt keine repräsentative Stichprobe für IuM 5–7. Nutzerfeedback ersetzt keine technische Vollprüfung.

**Phase-1-Folge.** Repräsentative Lernaufgaben werden mit der Zielaltersgruppe und unterschiedlichen Zugangsbedürfnissen erprobt; Befunde zu Bedienbarkeit und Lernen bleiben getrennt.

### CLAIM-DLE-004 – Datenvermeidung als Designprinzip, nicht als Compliance-Etikett

**Befund.** Art. 5 Abs. 1 lit. c DSGVO verlangt bei personenbezogenen Daten Datenminimierung. Art. 25 verlangt geeignete Maßnahmen zur wirksamen Umsetzung der Grundsätze und datenschutzfreundliche Voreinstellungen; die finale EDPB-Leitlinie 4/2019 konkretisiert die lebenszyklusbezogene und nachweisbare Gestaltung.

**Geltung und Quellen.** EU-Recht und behördliche Orientierung, geprüft zum 2026-07-28. [DSGVO](https://eur-lex.europa.eu/eli/reg/2016/679/oj), [EDPB-Leitlinie](https://www.edpb.europa.eu/documents/guideline/guidelines-42019-on-article-25-data-protection-by-design-and-by-default_en)

**Einschränkung.** Konto- und Backendfreiheit verhindern nicht automatisch personenbezogene Freitexte, Hosting-Logs, Drittrequests oder personenbezogene Exporte und belegen keine DSGVO-Compliance. Verantwortlichkeit und Rechtsgrundlage bleiben offen.

**Phase-1-Folge.** Keine Namen, Konten oder Telemetrie im Kern; Datenarten, Zweck, Speicherort, Löschung, Export und Hostingflüsse werden vor öffentlichem Betrieb dokumentiert und rechtlich geprüft.

### CLAIM-DLE-005 – Endgerätespeicherung nach § 25 TDDDG gesondert prüfen

**Befund.** § 25 TDDDG stellt Speicherung von Informationen in Endeinrichtungen und Zugriff auf dort vorhandene Informationen grundsätzlich unter Einwilligung; Ausnahmen betreffen Nachrichtenübertragung und unbedingt erforderliche Vorgänge für einen ausdrücklich gewünschten digitalen Dienst.

**Geltung und Quelle.** Bundesrecht Deutschland, Rechtsstand geprüft am 2026-07-28. [Amtlicher Gesetzesdienst](https://www.gesetze-im-internet.de/ttdsg/__25.html)

**Einschränkung.** Ob lokale Lernstandspeicherung im konkreten Schulbetrieb unbedingt erforderlich ist, wer Anbieter oder Endnutzer ist und welche Einwilligungsregeln greifen, wird hier nicht entschieden.

**Phase-1-Folge.** Nicht notwendige Speicherung vermeiden; Zwecke und Datenarten offenlegen; die TDDDG-Einordnung vor Deployment prüfen. Kein pauschaler Banner wird aus dem Claim abgeleitet.

### CLAIM-DLE-006 – Browserstorage ist verfügbarkeits- und persistenzunsicher

**Befund.** WHATWG setzt lokale Storage-Buckets zunächst auf `best-effort`; unter Speicherdruck können sie gelöscht werden. Persistenz hängt von Permission und User Agent ab, Quota ist implementierungsdefiniert. Der HTML Standard erlaubt einen `SecurityError`, wenn Origin oder Browserpolicy Persistenz nicht zulassen.

**Geltung und Quellen.** WHATWG Living Standards, Storage-Stand 15.03.2026 und HTML-Abruf 28.07.2026. [Storage Standard](https://storage.spec.whatwg.org/), [HTML Web Storage](https://html.spec.whatwg.org/multipage/webstorage.html)

**Einschränkung.** `localStorage` ist nicht der vorgesehene Lernstandspeicher; sein Fehlervertrag belegt nur, dass API-Präsenz keine Speicherzusage ist. Auch `persistent` ersetzt kein Backup außerhalb des Browsers.

**Phase-1-Folge.** Schreib-/Lese-/Lösch-Probe, sichtbarer flüchtiger Modus, versionierte atomare Speicherung und nutzergesteuerter Export. Es wird nie erfolgreicher Speicherzustand vorgetäuscht.

### CLAIM-DLE-007 – Installierbarkeit, Offlinefähigkeit und Offlinekorrektheit trennen

**Befund.** Web Application Manifest beschreibt Start- und Darstellungsmetadaten; Service Workers stellen Fetch-, Cache- und Lifecycle-Mechanismen für offlinefähige Anwendungen bereit. Weder ein Manifest noch eine Service-Worker-Registrierung beweist vollständiges korrektes Offlineverhalten.

**Geltung und Quellen.** App Manifest: instabiler Working Draft vom 23.07.2026; Service Workers: Candidate Recommendation Draft vom 23.07.2026, work in progress. [Manifest](https://www.w3.org/TR/appmanifest/), [Service Workers](https://www.w3.org/TR/service-workers/)

**Einschränkung.** Beide Dokumente können sich ändern; Browserimplementierungen und schulische Policies variieren. Installationsoberflächen sind keine standardübergreifende Garantie.

**Phase-1-Folge.** Getrennte Abnahmekriterien für Installation, Kernressourcen offline, Lernstand offline, externe Ressourcen, Erstladung, Netzverlust und Wiederanbindung.

### CLAIM-DLE-008 – Update- und Cachefehler als eigener Vertrag testen

**Befund.** RFC 9111 unterscheidet frische, veraltete und revalidierte HTTP-Antworten; Service Workers besitzen zusätzlich Installations-, Warte- und Aktivierungszustände sowie CacheStorage. Korrekte Kombinationen alter und neuer Ressourcen ergeben sich nicht automatisch.

**Geltung und Quellen.** IETF Standards Track RFC 9111 von 2022 sowie W3C Service Workers Candidate Recommendation Draft vom 23.07.2026. [RFC 9111](https://www.rfc-editor.org/rfc/rfc9111.html), [Service Workers](https://www.w3.org/TR/service-workers/)

**Einschränkung.** Die Standards schreiben keine projektspezifische atomare Release- oder Lernstandsmigration vor. Browsercache, Service-Worker-Cache und lokale Lernstände sind verschiedene Zustände.

**Phase-1-Folge.** Versionierter Cache-/Release-/Migrationsvertrag mit Tests für Teilcache, Altclient, neue Assets, laufende Arbeit, Rollback und inkompatiblen Import.

### CLAIM-DLE-009 – OER erfordert echten Bearbeitungs- und Weitergaberaum

**Befund.** Die UNESCO-Empfehlung von 2019 beschreibt OER als Lern-, Lehr- und Forschungsmaterialien in der Gemeinfreiheit oder unter einer offenen Lizenz, die kostenlosen Zugang, Wiederverwendung, Umnutzung, Bearbeitung und Weiterverbreitung erlaubt.

**Geltung und Quelle.** Internationale UNESCO-Empfehlung an Mitgliedstaaten vom 25.11.2019. [Originalquelle](https://www.unesco.org/en/legal-affairs/recommendation-open-educational-resources-oer)

**Einschränkung.** Die Empfehlung lizenziert kein Projektmaterial, ist kein deutsches Gesetz und kein Wirksamkeitsnachweis. Kostenloser Lesezugriff allein erfüllt den beschriebenen Nachnutzungsraum nicht.

**Phase-1-Folge.** Quellformate, bearbeitbare Assets, vollständige Rechtekette und dokumentierte lokale Nutzung gehören zur OER-Auslieferung.

### CLAIM-DLE-010 – CC BY 4.0 assetgenau attribuieren

**Befund.** CC BY 4.0 erlaubt Vervielfältigung, öffentliche Weitergabe und Bearbeitung. Beim Teilen sind die bereitgestellten Urheber-, Copyright-, Lizenz-, Haftungsausschluss- und Werkangaben soweit praktikabel zu erhalten; Änderungen und Lizenzbezug sind kenntlich zu machen.

**Geltung und Quelle.** Kanonischer internationaler Lizenztext Creative Commons Attribution 4.0. [Legal Code](https://creativecommons.org/licenses/by/4.0/legalcode.en)

**Einschränkung.** Die Lizenz deckt nur Rechte ab, die die lizenzgebende Person einräumen kann; Persönlichkeits-, Datenschutz-, Marken-, Patent- und Drittmaterialrechte können fortbestehen.

**Phase-1-Folge.** Jedes importierte Asset erhält Titel, Urheber, Quelle, Lizenzversion/-link, Änderungsvermerk und Rechteprüfung.

### CLAIM-DLE-011 – ShareAlike und Kompatibilität versions- und richtungsspezifisch behandeln

**Befund.** CC BY-SA 4.0 erlaubt Teilen und Bearbeiten unter Attribution und verlangt beim Teilen eigener Bearbeitungen eine zulässige Adapterlizenz. Die offizielle Kompatibilitätsliste nennt BY-SA 4.0/spätere oder portierte Versionen und ausgewiesene kompatible Lizenzen; GPLv3-Kompatibilität ist ausdrücklich nur einseitig.

**Geltung und Quellen.** Kanonischer CC-BY-SA-4.0-Lizenztext und offizielle Kompatibilitätsliste, geprüft am 2026-07-28. [Legal Code](https://creativecommons.org/licenses/by-sa/4.0/legalcode.en), [Kompatible Lizenzen](https://creativecommons.org/compatible-licenses/)

**Einschränkung.** Bearbeitung, Sammlung, technische Modifikation und Schrankenanwendung sind einzelfallabhängig. Die Kompatibilitätsliste kann erweitert werden; der Claim ist keine Rechtsberatung.

**Phase-1-Folge.** Keine pauschale Lizenzampel. Jede Kombination wird mit Version, Richtung, Werkart und Bearbeitungsstatus dokumentiert; `NC`/`ND` gelangt nicht ohne Einzelfallentscheidung in den offenen Kern.

### CLAIM-DLE-012 – Schulbrowser als datiertes Konfigurationsziel behandeln

**Befund.** Apple dokumentiert, dass MDM Safari und damit Web Clips deaktivieren sowie Webzugriffe durch Allow-/Deny-Listen oder WebKit-Filter beschränken kann.

**Geltung und Quellen.** Aktuelle Apple-Herstellerdokumentation für verwaltete Geräte, abgerufen am 2026-07-28. [Restrictions](https://developer.apple.com/documentation/devicemanagement/restrictions), [WebContentFilter](https://developer.apple.com/documentation/devicemanagement/webcontentfilter)

**Einschränkung.** Das belegt keine konkrete Schulkonfiguration, keine universelle iPad-Supportmatrix und keine Eigenschaften von Chromium oder Firefox.

**Phase-1-Folge.** Reale verwaltete iPads und benannte Browserhauptversionen bilden die Abnahmematrix; MDM, Filter, Download, Storage, Einbettung und Web-Clip-Nutzung werden separat protokolliert.

### CLAIM-DLE-013 – Netzlast messen; Nachhaltigkeitsdraft nicht zum Standard erklären

**Befund.** RFC 9111 beschreibt Wiederverwendung frischer Antworten und Revalidierung als Mittel zur Reduktion von Latenz und Netzwerkaufwand. Die Web Sustainability Guidelines bieten breitere Empfehlungen, sind am Stichtag aber nur ein nicht W3C-endorsed Group Note Draft ohne vorläufigen Interoperabilitäts- oder Implementierungsbericht.

**Geltung und Quellen.** IETF Standards Track RFC 9111; W3C Group Note Draft vom 28.07.2026. [RFC 9111](https://www.rfc-editor.org/rfc/rfc9111.html), [WSG Draft](https://www.w3.org/TR/2026/DNOTE-web-sustainability-guidelines-20260728/)

**Einschränkung.** Weniger Transfers beweisen keine konkrete Umweltwirkung. WSG kann ersetzt oder obsolet werden und ist kein Konformitätsstandard.

**Phase-1-Folge.** Gemessene Roh-, Transfer-, Cache- und Offlinegrößen, begründete Performancebudgets, wenige Drittrequests und regelmäßige Wartungsprüfung; keine pauschalen Nachhaltigkeitslabels.

### CLAIM-DLE-014 – Gerätedigitalisierung nicht mit Lernwirkung verwechseln

**Befund.** Ein systematischer Review identifizierte 43 Studien aus 2010–2019 zur iPad- oder Mobilgerätenutzung in schulischen Lernkontexten. Die berichteten akademischen Outcomes waren über Fächer und Umsetzungen gemischt beziehungsweise inkonsistent; der Review schätzt weder einen kausalen Effekt noch einen quantitativen Nulleffekt.

**Population und Kontext.** Nur 21 der 43 Studien untersuchten ausschließlich Schülerinnen und Schüler im Alter von 9 bis 14 Jahren; die übrigen schlossen teils breitere Altersstichproben ein. Die Studien lagen in schulischen Lernbereichen wie Mathematik, Englisch und Naturwissenschaften; Review von Boon, Boon und Bartle. [Original-/Repositoryquelle](https://doi.org/10.1007/s13384-020-00400-0)

**Einschränkung.** Die meisten Studien waren explorativ und qualitativ, Interventionen häufig kurz; Längsschnitt- und Within-Subject-Experimente fehlten weitgehend. Hinzu kommen heterogene Fächer, Altersstichproben, Gerätenutzungen und Pädagogiken sowie der Suchstand März 2019. Der Review untersucht weder das IuM-Lernwerk noch WCAG-Konformität, Local First oder PWA-Technik und erlaubt keine kausale oder pauschale Nullfolgerung.

**Phase-1-Folge.** Jede digitale Funktion braucht eine fachlich-didaktische Lernfunktion und separate Erprobung; bloße iPad-Verfügbarkeit ist kein Qualitätskriterium.

## Priorisierte Phase-1-Anforderungen und QA-Folgen

| Prio | Spezifikationsinput | Verbindliche QA-Folge |
| --- | --- | --- |
| P0 | WCAG 2.2 AA über vollständige Seiten/Prozesse | automatisierte und manuelle Prüfung; Tastatur, Fokus, Reflow, Semantik, Kontrast, Status und Fehler |
| P0 | gleichwertige Tastatur-/Touchpfade | keine Drag-only-Kernhandlung; vollständige Aufgaben mit beiden Eingaben und Assistive Technology |
| P0 | datenvermeidender Local-First-Vertrag | keine Konten/Namen/Telemetrie; Dateninventar, Zweck, Speicherort, Lösch- und Fehlerpfad |
| P0 | flüchtiger Modus bei Speicherfehler | blockierte Policy, Quota und Eviction provozieren; kein falscher Speichererfolg; sofortiger Export |
| P0 | portabler Export/Import | versioniertes Format; Schema-, Typ-, Größen- und Integritätsprüfung vor vollständiger Übernahme |
| P0 | Offlinekern und sicheres Update | Erstladung, Netzverlust, Teilcache, Altclient, neues Deployment, Rollback und Wiederanbindung |
| P0 | assetgenaue OER-Rechtekette | Quelle, Urheber, Lizenzversion/-link, Änderungen, Drittmaterialstatus und Kompatibilitätsentscheidung |
| P0 | reale schulische Browsermatrix | verwaltetes iPad plus datierte Chromium-/Firefox-Ziele; MDM, Filter, Download, Einbettung, Storage |
| P1 | geringe Bandbreite und statische Nachhaltigkeit | gemessene Transfer-/Cache-/Offlinebudgets; externe Requests inventarisiert; kalter und warmer Start |
| P1 | progressive Verbesserung | Navigation und Kerninhalt bleiben bei Ausfall nicht wesentlicher Skripte verfügbar |
| P1 | schulische Accessibility-/Usability-Erprobung | Zielaltersgruppe und unterschiedliche Zugangsbedürfnisse; Bedien- und Lernoutcomes getrennt |
| P1 | Recheck- und Wartungsvertrag | Owner, Trigger, Datum und Nachweis für Recht, Standards, Browser, MDM, Lizenzen und Links |

Die Tabelle ist ausschließlich Input für die Phase-1-Spezifikation. Dieses Paket erzeugt keinen Portalcode, keine PWA-Konfiguration, keine Komponenten, Abhängigkeiten oder Buildartefakte.

## Offene Risiken und Recheck-Trigger

| Risiko | Trigger |
| --- | --- |
| DSGVO-/TDDDG-Anwendbarkeit, Betreiber, Logs, Hosting und Freitext ungeklärt | vor öffentlichem Betrieb und bei jeder Datenflussänderung; zuständige Rechts-/Datenschutzprüfung |
| öffentliche Accessibility-Rechtslage nicht abschließend bestimmt | sobald Betreiber und Veröffentlichungsform feststehen |
| App Manifest, Service Workers und WSG ändern Reifegrad/Inhalt | vor Phase-1-Freeze und spätestens 2026-10-28 |
| WHATWG Storage oder Zielbrowser ändern Persistenz-/Quota-Verhalten | vor Phase-1-Freeze, bei Browserhauptversion und spätestens 2026-10-28 |
| reale iPad-/MDM-/Filterkonfiguration unbekannt | je Schulprofil sowie bei iPadOS-, Safari- oder MDM-Hauptupdate |
| CC-Kompatibilitätsliste oder Drittmaterialstatus ändert sich | bei jedem Import, Lizenzwechsel und spätestens 2026-10-28 |
| WCAG-Errata oder Accessibility-Ziel ändert sich | vor jedem öffentlichen Release |
| Cache-/Lernstandsschema erzeugt Mischzustände | bei jedem Schema-, Cache- oder Deploymentvertrag; vollständiger Regressionstest |
| empirische Übertragung auf IuM 5–7 ungeprüft | Pilotierung jeder zentralen digitalen Lernfunktion |

## Kurationsentscheidung

Retained werden nur Aussagen, die an eine direkte Originalquelle gebunden, in Geltung und Reifegrad eingegrenzt und von den Projektfolgen getrennt sind. Nicht retained sind universelle Browser-Supportaussagen, pauschale „PWA funktioniert offline“-Behauptungen, ein allgemeines Cookie-Banner, automatische Lizenzampeln, ungemessene Nachhaltigkeitsversprechen und die Annahme, WCAG- oder iPad-Einsatz belege Lernwirksamkeit.
