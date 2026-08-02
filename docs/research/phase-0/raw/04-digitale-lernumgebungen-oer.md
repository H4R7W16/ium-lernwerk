---
package: digitale-lernumgebungen-oer
executed: 2026-07-28
status: raw
prompt: ../prompts/04-digitale-lernumgebungen-oer.md
---

# Digitale Lernumgebungen und OER für das IuM-Lernwerk

## 1. Executive Summary

Die Recherche wurde am 28. Juli 2026 gegen Originalquellen von W3C/WAI, WHATWG, IETF, EUR-Lex, Europäischem Datenschutzausschuss, Bundesministerium der Justiz, UNESCO, Creative Commons und Apple sowie gegen einen systematischen Review zur iPad-Nutzung von 9- bis 14-Jährigen geprüft. Der Bericht trennt vier Aussagearten:

1. **Recht beziehungsweise behördliche Orientierung:** DSGVO, TDDDG und EDPB-Leitlinien gelten in ihrem jeweiligen sachlichen und räumlichen Bereich; ob und wie sie auf eine konkrete Veröffentlichung, Schule oder lokale Speicherfunktion anwendbar sind, muss separat geprüft werden. Dieser Bericht ist keine Rechtsberatung.
2. **Technische Standards:** WCAG 2.2, WHATWG Storage/HTML und RFC 9111 beschreiben überprüfbare Anforderungen oder Plattformverhalten. Service Workers und Web App Manifest sind am Stichtag weiterhin Entwürfe mit unterschiedlichem Reifegrad.
3. **Empirischer Befund:** Ein systematischer Review von 43 Studien mit 9- bis 14-jährigen Schülerinnen und Schülern fand keine konsistente Verbesserung akademischer Outcomes allein durch iPad- oder Mobilgerätenutzung. Das Medium ersetzt keine didaktische Begründung.
4. **Projektentscheidung:** Konto- und Backendfreiheit, Datenvermeidung, lokale Arbeit, bewusster Export, statische Auslieferung und CC BY-SA 4.0 sind Projektentscheidungen. Die Quellen begründen Prüfbedingungen, nicht automatisch die konkrete Umsetzung.

Für Phase 1 folgt: WCAG 2.2 AA ist ein verbindlicher technischer Mindestprüfrahmen, aber kein Nachweis schulischer Bedienbarkeit oder Lernwirksamkeit. Tastatur, Touch und assistive Technologien brauchen getrennte Prüfpfade. Lokaler Browserspeicher ist nicht automatisch verfügbar und zunächst nur `best-effort`; Export bleibt deshalb die vom Browser unabhängige Sicherung. Installierbarkeit, Offlinefähigkeit und korrektes Offline-/Updateverhalten sind drei verschiedene Eigenschaften. OER-Nachnutzung benötigt eine datei- beziehungsweise assetgenaue Rechtekette. Browser- und MDM-Kompatibilität wird als datiertes Ziel auf realen schulischen Geräten geprüft.

## 2. Quellen- und Statusmatrix

Stand aller schnell veränderlichen Angaben: **2026-07-28**.

| ID | Herausgeber / Zuständigkeit | Status am Stichtag | Primärfunktion | Wesentliche Grenze |
| --- | --- | --- | --- | --- |
| `SRC-DLE-WCAG22-2024` | W3C, international | W3C Recommendation vom 12.12.2024, mit Errata | normativer technischer Accessibility-Standard | deckt nicht alle Bedürfnisse ab; keine Lernwirksamkeit |
| `SRC-DLE-WAI-USERS-2020` | W3C WAI | offizielle Orientierung, zuletzt am 05.05.2020 aktualisiert | Nutzerbeteiligung zusätzlich zur Konformitätsprüfung | kein kontrollierter Wirksamkeitsnachweis |
| `SRC-DLE-GDPR-2016` | EU, unmittelbar geltende Verordnung | geltendes EU-Recht; geprüft 2026-07-28 | Datenminimierung, Datenschutz durch Technikgestaltung | Anwendbarkeit setzt Verarbeitung personenbezogener Daten voraus |
| `SRC-DLE-EDPB-DPBDD-2020` | Europäischer Datenschutzausschuss | finale Leitlinie 4/2019, Version 2.0 vom 20.10.2020 | behördliche Auslegung zu Art. 25 DSGVO | Orientierung, kein Ersatz für Einzelfallprüfung |
| `SRC-DLE-TDDDG-25-2024` | Bundesrepublik Deutschland | geltendes Bundesrecht; geprüft 2026-07-28 | Speicherung/Auslesen von Informationen auf Endeinrichtungen | Einwilligungs- und Ausnahmetatbestände sind einzelfallabhängig |
| `SRC-DLE-WHATWG-STORAGE-2026` | WHATWG | Living Standard, Stand 15.03.2026 | Speicherarchitektur, Quota, Persistenz | Implementierungsentscheidungen der Browser bleiben relevant |
| `SRC-DLE-WHATWG-HTML-STORAGE-2026` | WHATWG | Living Standard, abgerufen 2026-07-28 | Zugriff und Fehlerverhalten von `localStorage` | `localStorage` ist nicht der geplante Lernstandspeicher; Verhalten zeigt die Verfügbarkeitsgrenze |
| `SRC-DLE-SERVICE-WORKERS-2026` | W3C Web Applications WG | Candidate Recommendation Draft vom 23.07.2026, work in progress | Fetch-Interzeption, Cache und Lifecycle | keine W3C-Endorsement-Garantie; Offlinekorrektheit bleibt Implementierungsaufgabe |
| `SRC-DLE-APP-MANIFEST-2026` | W3C Web Applications WG | Working Draft vom 23.07.2026, ausdrücklich instabil | Installations- und Startmetadaten | keine Offlinezusage; Implementierung variiert |
| `SRC-DLE-HTTP-CACHE-2022` | IETF | Internet Standards Track, RFC 9111 / STD 98 | HTTP-Caching, Frische und Revalidierung | Browsercache ersetzt weder Service-Worker-Cache noch Datensicherung |
| `SRC-DLE-UNESCO-OER-2019` | UNESCO General Conference | internationale Empfehlung vom 25.11.2019 | OER-Begriff und Politikrahmen | für Mitgliedstaaten orientierend, keine Projektlizenz |
| `SRC-DLE-CC-BY-4` | Creative Commons | kanonischer Lizenztext, Version 4.0 | Nachnutzung und Namensnennung | nur lizenzierbare Rechte; keine Rechtsberatung |
| `SRC-DLE-CC-BY-SA-4` | Creative Commons | kanonischer Lizenztext, Version 4.0 | Nachnutzung, Namensnennung, ShareAlike | Bearbeitung/Collection und Drittmaterial sind konkret zu prüfen |
| `SRC-DLE-CC-COMPAT-2026` | Creative Commons | offizielle, fortschreibbare Kompatibilitätsliste; geprüft 2026-07-28 | zulässige Adapterlizenzen für BY-SA | versions- und richtungsspezifisch; Liste kann erweitert werden |
| `SRC-DLE-APPLE-RESTRICTIONS-2026` | Apple | aktuelle Herstellerdokumentation, abgerufen 2026-07-28 | MDM-Einschränkungen für Safari/Web Clips | kein plattformübergreifender Standard |
| `SRC-DLE-APPLE-WEBFILTER-2026` | Apple | aktuelle Herstellerdokumentation, abgerufen 2026-07-28 | Allow-/Deny-Listen und WebKit-Filter | konkrete Schulkonfiguration unbekannt |
| `SRC-DLE-WSG-DRAFT-2026` | W3C Sustainable Web Interest Group | Group Note Draft vom 28.07.2026, nicht W3C-endorsed | Arbeitscheckliste für Webnachhaltigkeit | kein Standard, kein Implementierungsbericht |
| `SRC-DLE-IPAD-REVIEW-2021` | Boon, Boon und Bartle | systematischer Review, 43 Studien von 2010–2019 | akademische Outcomes bei 9- bis 14-Jährigen | heterogene Fächer, Designs und Geräteeinsätze; keine Accessibility-Studie |

### Such- und Prüfweg

Gesucht wurde über offizielle Publikationsregister und direkte Original-URLs. Maßgeblich waren die Statusabschnitte der Standards, die konsolidierten beziehungsweise amtlich bereitgestellten Rechtstexte, die kanonischen CC-Lizenztexte und die akzeptierte Manuskriptfassung des systematischen Reviews. Marketingseiten, generische PWA-Checklisten und Kompatibilitätsaggregatoren wurden nicht als Beleg für retained Claims verwendet. Für schulische Browser wurde keine universelle Supportbehauptung übernommen, weil reale Betriebssystem-, Browser-, MDM-, Filter- und Speicherprofile nicht vorliegen.

## 3. Accessibility

### 3.1 Normativer technischer Rahmen

WCAG 2.2 ist seit 12. Dezember 2024 W3C Recommendation; W3C empfiehlt Version 2.2 als Ziel für neue oder aktualisierte Accessibility-Policies. Für AA sind unter anderem diese für interaktive Lernmodule wichtigen Kriterien einschlägig:

- alle nicht pfadabhängigen Funktionen sind über eine Tastaturschnittstelle bedienbar (`2.1.1`, Level A);
- Tastaturfokus darf nicht eingeschlossen werden (`2.1.2`, Level A), muss sichtbar sein (`2.4.7`, Level AA) und darf durch autorenseitig erzeugte Inhalte nicht vollständig verdeckt werden (`2.4.11`, Level AA);
- Funktionen mit Ziehen müssen zusätzlich ohne Ziehen mit einem einzelnen Zeiger ausführbar sein, sofern Ziehen nicht wesentlich ist (`2.5.7`, Level AA);
- Zeigerziele erfüllen grundsätzlich mindestens 24 × 24 CSS-Pixel oder eine der präzise beschriebenen Ausnahmen (`2.5.8`, Level AA);
- Reflow, Kontrast, Textabstände, semantische Struktur, Name/Rolle/Wert, Fehlerkennzeichnung und Statusmeldungen gehören ebenfalls in den vollständigen AA-Prüfumfang.

Die Auswahl ist keine verkürzte Konformitätsdefinition. WCAG-Konformität gilt für vollständige Seiten und Prozesse nach den Konformitätsanforderungen des Standards; einzelne erfolgreiche Kriterien genügen nicht.

### 3.2 Grenze von WCAG

WCAG 2.2 sagt selbst, dass nicht jedes Bedürfnis von Menschen mit Behinderungen abgedeckt wird. WAI unterscheidet Accessibility, Usability und Inclusion und empfiehlt, Standardsprüfung mit der Beteiligung von Menschen mit Behinderungen zu kombinieren. Daraus folgt für das Lernwerk nicht, dass jede Nutzerbeteiligung einen empirischen Wirksamkeitsbeleg erzeugt. Es folgt ein QA-Bedarf:

- technische AA-Prüfung mit automatisierten und manuellen Verfahren;
- vollständige Tastaturpfade und Prüfungen mit Screenreader/Vergrößerung in definierten Zielbrowsern;
- aufgabenbezogene Usability-Erprobung mit Schülerinnen und Schülern der Zielaltersgruppe, darunter nach Möglichkeit Lernende mit unterschiedlichen Zugangsbedürfnissen;
- getrennte Lernwirksamkeitsprüfung der didaktischen Aufgaben.

### 3.3 Touch und alternative Eingaben

„Touchfähig“ ist kein Ersatz für Tastaturbedienbarkeit. Drag-and-drop, Canvas, Sortieren, Verbinden oder räumliches Modellieren benötigen zugängliche Alternativen mit derselben fachlichen Funktion. Ein großzügigeres internes Zielmaß als das normative Minimum kann als Projektentscheidung sinnvoll sein, darf aber nicht als WCAG-Wortlaut ausgegeben werden. Maus, Touch, Tastatur, Schaltersteuerung und assistive Technologien werden nicht über ein einzelnes Gerätetest-Szenario abgedeckt.

## 4. Privacy und Local First

### 4.1 Rechtlicher Rahmen, Europäische Union

Art. 5 Abs. 1 lit. c DSGVO verlangt bei personenbezogenen Daten eine Beschränkung auf das für den Zweck Notwendige. Art. 25 verlangt geeignete technische und organisatorische Maßnahmen zur wirksamen Umsetzung der Datenschutzgrundsätze und datenschutzfreundliche Voreinstellungen. Die finale EDPB-Leitlinie 4/2019 konkretisiert, dass diese Gestaltung über den Lebenszyklus der Verarbeitung wirksam und nachweisbar sein muss.

**Grenze:** Konto- und Backendfreiheit reduziert mögliche Datenflüsse, belegt aber weder die Nichtanwendbarkeit der DSGVO noch vollständige Compliance. Freitext kann von Lernenden freiwillig personenbezogen gefüllt werden; Hosting-Logs, externe Ressourcen, Fehlermeldungen, Exportdateien und eingebettete Inhalte können eigene Verarbeitungsvorgänge erzeugen. Verantwortlichkeit, Rechtsgrundlage, Informationspflichten, Aufbewahrung und schulrechtlicher Kontext sind vor Veröffentlichung zu prüfen.

### 4.2 Endgerätezugriff, Deutschland

§ 25 TDDDG betrifft die Speicherung von Informationen in Endeinrichtungen und den Zugriff auf bereits gespeicherte Informationen. Grundsätzlich ist Einwilligung vorgesehen; § 25 Abs. 2 enthält Ausnahmen für die Nachrichtenübertragung und für das, was unbedingt erforderlich ist, um einen ausdrücklich gewünschten digitalen Dienst bereitzustellen.

**Grenze:** Der Bericht entscheidet nicht, ob eine konkrete Lernstandspeicherung „unbedingt erforderlich“ ist, wer Endnutzer oder Anbieter ist oder wie Einwilligung im schulischen Kontext zu behandeln wäre. Die Phase-1-Spezifikation muss nicht notwendige Speicherung vermeiden, Zweck und lokale Datenarten offenlegen und die konkrete rechtliche Bewertung vor öffentlichem Betrieb auslösen. Ein pauschaler Cookie- oder Speicherbanner wird nicht aus dieser Recherche abgeleitet.

### 4.3 Technische Speichergrenzen

Der WHATWG Storage Living Standard setzt lokale Storage-Buckets zunächst auf `best-effort`. Unter Speicherdruck kann der User Agent solche Buckets löschen; eine Umstellung auf `persistent` hängt von Permission und Browserentscheidung ab. Quota und Nutzungsabschätzung sind implementierungsdefiniert. Der HTML Living Standard erlaubt beim Zugriff auf `localStorage` einen `SecurityError`, wenn Origin oder Browserpolicy die Persistenz nicht zulassen.

Für die Projektentscheidung „IndexedDB für versionierte lokale Lernstände“ folgt:

- Fähigkeitserkennung und Schreib-/Lese-/Löschtest statt bloßer API-Erkennung;
- verständlicher flüchtiger Modus, wenn Speicherung fehlt oder fehlschlägt;
- atomare, schema-validierte lokale Updates und Importvorgänge;
- nutzergesteuerter, portabler Export als von Browserpersistenz unabhängiger Sicherungsweg;
- keine Erfolgsanzeige vor nachgewiesenem Lesen des geschriebenen Zustands;
- vollständiges lokales Löschen, soweit die Webplattform dies für den Origin ermöglicht.

Lokaler Speicher und Export sind verschiedene Funktionen: Browserpersistenz kann komfortables Fortsetzen unterstützen; nur eine bewusst gespeicherte Exportdatei kann kontrolliert zwischen Geräten übertragen und außerhalb des Origin-Speichers gesichert werden.

## 5. Offline- und Updateverhalten

### 5.1 Installierbarkeit ist nicht Offlinefähigkeit

Der Web Application Manifest Working Draft beschreibt Metadaten wie Name, Icons, Start-URL, Scope und Darstellungsmodus. Er verspricht weder, dass Ressourcen offline vorliegen, noch dass eine Lernhandlung ohne Netz vollständig funktioniert. Am 23. Juli 2026 ist das Dokument ausdrücklich instabil und nicht W3C-endorsed.

Der Service Workers Candidate Recommendation Draft beschreibt `install`, `activate` und `fetch` sowie einen Request-/Response-Speicher, mit dem offlinefähige Anwendungen gebaut werden können. Das ist eine technische Fähigkeit, kein automatischer Korrektheitsnachweis. Der Draft ist work in progress und kann nicht als zeitloser Browservertrag behandelt werden.

### 5.2 Korrektes Offlineverhalten

Ein Kernmodul ist erst „offline korrekt“, wenn mindestens diese Szenarien auf den Zielgeräten bestehen:

1. erster Aufruf ohne Netz: klare Online-Erfordernis statt leerer oder falscher Oberfläche;
2. vollständige Erstinstallation und anschließend Netzverlust;
3. Netzverlust mitten in einer Interaktion;
4. fehlende einzelne Ressource oder blockierte externe Domain;
5. Speichern verfügbar, nicht verfügbar, voll oder nachträglich gelöscht;
6. alter lokaler Lernstand mit neuer Modulversion;
7. teilweise geladener neuer Release;
8. Rückkehr online und kontrollierte Aktualisierung;
9. Export und Import im Offlinezustand;
10. eingebettete Nutzung mit abweichender Origin- oder Browserpolicy.

Externe Videos, Fonts, Analyse-, CDN- oder Drittanbieterressourcen dürfen den Kernpfad nicht unbemerkt onlineabhängig machen. Onlinequellen werden sichtbar markiert.

### 5.3 Update- und Cacheverhalten

RFC 9111 trennt frische, veraltete und revalidierte HTTP-Antworten. Service Worker haben zusätzlich einen eigenen Lifecycle und CacheStorage. Daraus folgt kein bestimmtes Releaseverfahren, wohl aber ein Prüfbedarf: gehashte unveränderliche Assets, kurze beziehungsweise revalidierbare Einstiegspunkte, versionierte Caches und Lernstandsschemata sowie eine Aktivierungsstrategie, die keine laufende Arbeit unbemerkt mit inkompatiblen Ressourcen mischt.

Die genaue Cache- und Updatepolitik ist Phase-1-Spezifikation. Vor ihrer Festlegung sind Fehlerszenarien mit altem Client, neuem Deployment, Teilcache und Rollback zu modellieren. „Service Worker registriert“ und „PWA installiert“ sind keine Abnahmekriterien für sicheren Offlinebetrieb.

## 6. OER und Lizenzkompatibilität

### 6.1 OER-Begriff

Die UNESCO-Empfehlung von 2019 definiert OER als Lern-, Lehr- und Forschungsmaterialien in beliebigem Format, die gemeinfrei sind oder unter einer offenen Lizenz stehen, welche kostenlosen Zugang, Wiederverwendung, Umnutzung, Bearbeitung und Weiterverbreitung erlaubt. Die Empfehlung ist ein internationaler Politikrahmen, keine Lizenz für das Projekt und kein Lernwirksamkeitsnachweis.

Für das Lernwerk folgt: Öffentlich lesbar oder kostenlos herunterladbar ist allein noch kein belastbarer OER-Status. Repositorium, Quellformate, bearbeitbare Assets, Lizenzhinweise und Rechtekette müssen Nachnutzung tatsächlich ermöglichen.

### 6.2 CC BY 4.0

CC BY 4.0 erlaubt Vervielfältigung, öffentliche Weitergabe und Bearbeitung. Beim öffentlichen Teilen sind, soweit bereitgestellt und praktikabel, Urheberidentifikation, Copyright-Hinweis, Lizenzhinweis, Haftungsausschluss-Hinweis und Werklink zu erhalten; Änderungen und Lizenzlink sind kenntlich zu machen. Die Angaben dürfen kontextangemessen über einen Link gebündelt werden.

### 6.3 CC BY-SA 4.0 und Kompatibilität

CC BY-SA 4.0 enthält zusätzlich ShareAlike: Beim öffentlichen Teilen eigener Bearbeitungen muss eine zulässige Adapterlizenz verwendet werden. Der kanonische Text definiert dafür BY-SA 4.0, spätere/portierte Versionen oder eine von Creative Commons ausgewiesene kompatible Lizenz. Die offizielle Kompatibilitätsliste nennt am Stichtag unter anderem Free Art License 1.3 und GPLv3; die GPLv3-Kompatibilität ist ausdrücklich nur in einer Richtung gegeben.

**Grenzen:**

- Die rechtliche Einordnung als Bearbeitung, Sammlung, bloße technische Modifikation oder Nutzung aufgrund einer Schranke ist einzelfallabhängig.
- CC-Lizenzen räumen nur Rechte ein, über die die lizenzgebende Person verfügen kann. Persönlichkeits-, Datenschutz-, Marken-, Patent- und Drittmaterialrechte können fortbestehen.
- Eine abstrakte Ampel- oder Kompatibilitätsgrafik ist keine Rechtsberatung.
- `NC`- oder `ND`-Material kann die freie Bearbeitbarkeit oder den vorgesehenen Nachnutzungsraum des Kernlernwerks einschränken und wird nicht ohne dokumentierte Einzelfallentscheidung in den Kern übernommen.

### 6.4 Erforderliche Rechtekette

Jedes Asset und jede inhaltliche Einheit benötigen maschinenlesbar oder strukturiert:

- Titel beziehungsweise Bezeichnung;
- Urheberin/Urheber und gegebenenfalls weitere Attributionsempfänger;
- Originalquelle und stabilen Link;
- exakte Lizenz mit Version und Lizenzlink;
- Kennzeichnung eigener Änderungen und vorheriger Änderungen;
- Status `eigen`, `drittmaterial`, `gemeinfrei/CC0`, `gesetzliche Schranke` oder `nicht geklärt`;
- Entscheidung, ob das Element Teil einer Bearbeitung oder einer getrennten Sammlung ist;
- Recheckdatum bei dynamischen Quellen oder Kompatibilitätsregeln.

## 7. Schulische Geräte und Browser

Apple dokumentiert für verwaltete Geräte, dass MDM Safari deaktivieren und damit auch das Öffnen von Web Clips verhindern kann. Web Content Filter können Domains beziehungsweise URLs erlauben oder sperren und WebKit-Verkehr filtern. Das belegt weder die tatsächliche Konfiguration einer Schule noch eine bestimmte Safari-Funktionsunterstützung.

Ein belastbares Supportziel ist deshalb datiert und konfigurationsbezogen:

| Ziel | Nachweis in Phase 1 |
| --- | --- |
| schulisches iPad | reale verwaltete Geräte, dokumentierte iPadOS-/Safari-Version, Speicher- und Web-Clip-Policy |
| Chromium Desktop | benannte aktuelle Hauptversionen auf den schulisch relevanten Betriebssystemen |
| Firefox Desktop | benannte aktuelle Hauptversionen auf den schulisch relevanten Betriebssystemen |
| Einbettung/LMS | eigener Test je zulässiger Origin-, Sandbox-, Download- und Speicherpolicy |
| Filter/Allowlist | Kernorigin, Assets, Updates, Downloads und externe Links getrennt testen |
| Offline | kalter Start, installierter Start, Update, Quota, Löschung und Wiederanbindung |

Basiskern und Lerninhalte sollen als semantisches HTML/CSS ohne proprietäre Plug-ins lesbar bleiben. JavaScript erweitert gezielt Interaktionen. Das ist eine Projektentscheidung zur progressiven Verbesserung; sie ersetzt keine Prüfung konkreter Lernhandlungen.

## 8. Nachhaltigkeit und Wartung

RFC 9111 beschreibt, wie frische Antworten ohne erneuten Originzugriff wiederverwendet und veraltete Antworten revalidiert werden können. Das kann Latenz und Netzwerkverkehr verringern. Für statische Auslieferung sprechen daher kleine, komprimierte, cachefähige und inhaltsadressierte Assets, die Vermeidung unnötiger Drittrequests sowie eine bewusst revalidierte Einstiegsschicht.

Die Web Sustainability Guidelines sind am Stichtag nur ein W3C Group Note Draft. Sie sind nicht von W3C oder seinen Mitgliedern endorsiert, können ersetzt werden und besitzen noch keinen vorläufigen Interoperabilitäts- oder Implementierungsbericht. Sie dürfen als offene Prüfliste für Systemdenken, Datenmenge, Gerätelebensdauer, Hosting und Wartung verwendet werden, nicht als Konformitätsstandard oder Beleg einer bestimmten Umweltwirkung.

Langfristige Wartbarkeit benötigt in Phase 1:

- offene, standardnahe Dateiformate und wenige klar begründete Abhängigkeiten;
- reproduzierbaren statischen Build und dokumentierte lokale Vorschau;
- automatisierte Link-, Lizenz-, Accessibility- und Größenprüfungen;
- versionierte Module, Lernstandsschemata und Migrationsregeln;
- dokumentierte Browsermatrix und regelmäßige reale Gerätetests;
- keine unkontrollierten externen Skripte, Fonts oder CDN-Abhängigkeiten im Kernpfad;
- Performancebudgets mit gemessenen Roh-, Transfer- und Offlinegrößen statt pauschaler Nachhaltigkeitslabels.

## 9. Offene Risiken

1. **Rechtsanwendbarkeit:** Verantwortliche Stelle, Hosting, Logs, Freitext, Exporte und TDDDG-Ausnahme sind noch nicht juristisch im konkreten Betrieb geprüft.
2. **Öffentliche Barrierefreiheitsanforderungen:** Welche EU-, Bundes- oder baden-württembergischen Vorschriften für Träger und Veröffentlichung gelten, hängt vom Betreiber und Einsatz ab; WCAG 2.2 AA ist Projektziel, nicht abschließende Rechtsprüfung.
3. **Browserpersistenz:** IndexedDB-Verfügbarkeit, Quota, Eviction und Persistenzvergabe auf verwalteten iPads sind unbekannt.
4. **Offlineupdates:** Ohne spezifizierten Release- und Migrationsvertrag drohen Mischzustände aus alten Lernständen und neuen Assets.
5. **Einbettung:** Sandbox-, Storage-, Download- und Filterregeln des jeweiligen LMS können Kernfunktionen blockieren.
6. **Lizenzkette:** Drittmaterial kann unklare Rechte, unvereinbare Bearbeitungsbedingungen oder fehlende Attributionsdaten enthalten.
7. **Accessibility und Lernen:** Standardkonformität belegt weder altersangemessene Bedienbarkeit noch fachliches Lernen.
8. **Technischer Reifegrad:** App Manifest, Service Workers und WSG können sich nach dem Stichtag ändern.
9. **Empirie:** Der iPad-Review untersucht heterogene fachliche Outcomes bis 2019, nicht das konkrete IuM-Lernwerk oder seine Accessibility.

### Datierten Recheck auslösen

- vor Festschreibung der Phase-1-Architektur und danach spätestens am **2026-10-28** für Service Workers, App Manifest, WSG, WHATWG Storage und Browserziele;
- vor jedem öffentlichen Release für WCAG-Errata, Datenschutz-/TDDDG-Rechtsstand und Hostingdatenflüsse;
- bei jeder iPadOS-, Safari-, Browser- oder MDM-Hauptaktualisierung;
- bei jeder neuen Drittmaterialklasse sowie vor Lizenzwechsel für CC-Legal-Code und offizielle Kompatibilitätsliste;
- nach jedem Lernstandsschema- oder Cachevertrag-Update mit vollständigem Offline-/Migrationsregressionstest;
- sobald Betreiber, Hosting und schulischer Rollout feststehen, mit zuständiger Datenschutz- und Rechtsprüfung.

## 10. Priorisierte Anforderungen und Quellenverzeichnis

### Priorisierte Anforderungen als Input für Phase 1

| Priorität | Anforderung | Abnahmekriterium |
| --- | --- | --- |
| P0 | Vollständiges WCAG-2.2-AA-Gate | automatisierte Prüfung plus manuelle Tastatur-, Fokus-, Reflow-, Screenreader-, Status- und Fehlerpfade |
| P0 | Touch und Tastatur funktional gleichwertig | keine zwingende Drag-only-Lernhandlung; alle Kernaktionen auf Touch und Tastatur prüfbar |
| P0 | Datenvermeidung und transparente lokale Daten | keine Namen/Konten/Telemetrie; Datenarten, Zweck, Löschung und Grenzen dokumentiert |
| P0 | Speicherfehler ohne Datenillusion | flüchtiger Modus sichtbar; Schreibfehler provozierbar; Export unmittelbar verfügbar |
| P0 | Versionierter Export/Import | lokales, dokumentiertes Format; Schema-, Größen- und Integritätsprüfung vor vollständiger Übernahme |
| P0 | Offlinekern mit definiertem Updatevertrag | festgelegte Kernressourcen; Tests für Erstladung, Teilcache, Netzverlust, Altversion und Wiederanbindung |
| P0 | Assetgenaue Lizenz- und Quellenkette | jedes veröffentlichte Asset hat Quelle, Rechteinhaber, Lizenzversion, Änderungen und Status |
| P0 | Reale schulische Zielmatrix | Tests auf verwalteten iPads und benannten Desktopbrowsern mit dokumentierter Policy |
| P1 | Bandbreiten- und Größenbudgets | gemessene Transfer-/Cache-/Offlinegrößen; keine unerklärten Drittrequests |
| P1 | Progressive Verbesserung | Orientierung und Kerninhalt bleiben bei Ausfall nichtwesentlicher Skripte zugänglich |
| P1 | Nutzerbasierte Usability-Prüfung | repräsentative Lernaufgaben mit Zielaltersgruppe und unterschiedlichen Zugangsbedürfnissen |
| P1 | Wartungs- und Recheckkalender | Owner, Trigger, Datum und Prüfnachweis für Standards, Recht, Browser und Lizenzen |

Alle Anforderungen sind Spezifikationsinput. Dieser Task erzeugt weder Portalcode noch PWA-Konfiguration, Komponenten, Abhängigkeiten oder Buildartefakte.

### Originalquellen

1. W3C. *Web Content Accessibility Guidelines (WCAG) 2.2*, Recommendation 12.12.2024. https://www.w3.org/TR/WCAG22/
2. W3C WAI. *Involving Users in Web Projects for Better, Easier Accessibility*. https://www.w3.org/WAI/planning/involving-users/
3. Europäisches Parlament und Rat. *Verordnung (EU) 2016/679*, insbesondere Art. 5 und 25. https://eur-lex.europa.eu/eli/reg/2016/679/oj
4. European Data Protection Board. *Guidelines 4/2019 on Article 25 Data Protection by Design and by Default*, Version 2.0, 20.10.2020. https://www.edpb.europa.eu/documents/guideline/guidelines-42019-on-article-25-data-protection-by-design-and-by-default_en
5. Bundesministerium der Justiz. *§ 25 TDDDG – Schutz der Privatsphäre bei Endeinrichtungen*. https://www.gesetze-im-internet.de/ttdsg/__25.html
6. WHATWG. *Storage Living Standard*, Stand 15.03.2026. https://storage.spec.whatwg.org/
7. WHATWG. *HTML Living Standard – Web Storage*. https://html.spec.whatwg.org/multipage/webstorage.html
8. W3C. *Service Workers Nightly*, Candidate Recommendation Draft 23.07.2026. https://www.w3.org/TR/service-workers/
9. W3C. *Web Application Manifest*, Working Draft 23.07.2026. https://www.w3.org/TR/appmanifest/
10. Fielding, R., Nottingham, M. & Reschke, J. *RFC 9111: HTTP Caching*, 2022. https://www.rfc-editor.org/rfc/rfc9111.html
11. UNESCO. *Recommendation on Open Educational Resources (OER)*, 25.11.2019. https://www.unesco.org/en/legal-affairs/recommendation-open-educational-resources-oer
12. Creative Commons. *Attribution 4.0 International – Legal Code*. https://creativecommons.org/licenses/by/4.0/legalcode.en
13. Creative Commons. *Attribution-ShareAlike 4.0 International – Legal Code*. https://creativecommons.org/licenses/by-sa/4.0/legalcode.en
14. Creative Commons. *Compatible Licenses*. https://creativecommons.org/compatible-licenses/
15. Apple. *Restrictions – Device Management*. https://developer.apple.com/documentation/devicemanagement/restrictions
16. Apple. *WebContentFilter – Device Management*. https://developer.apple.com/documentation/devicemanagement/webcontentfilter
17. W3C Sustainable Web Interest Group. *Web Sustainability Guidelines*, Group Note Draft 28.07.2026. https://www.w3.org/TR/2026/DNOTE-web-sustainability-guidelines-20260728/
18. Boon, H. J., Boon, L. & Bartle, T. (2021). *Does iPad use support learning in students aged 9-14 years? A systematic review*. https://doi.org/10.1007/s13384-020-00400-0
