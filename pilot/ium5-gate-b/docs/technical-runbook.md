# IUM5 Gate B – Technisches Runbook

Dieses Runbook ist eine ausführbare Checkliste für eine später gesondert autorisierte Prüffassung. Es ist kein Nachweis einer realen Durchführung.

```yaml
workflow-execution-authorized: false
status-mutation: forbidden
public-url-control: link-is-not-access-control
retention: 30-days-after-decision
```

## Zweck und Nichtfreigabegrenze

| Rolle | Eingabe | Aktion | Erwartete Evidenz | Fehlerzweig | Bereinigung |
| --- | --- | --- | --- | --- | --- |
| Koordination | schriftlicher Prüfauftrag | Umfang auf IUM-5-CORE-05, Gate B und `working` begrenzen | Auftrag nennt Build, Rollen und Prüffenster | Auftrag fehlt oder verlangt eine Statusänderung: stoppen | keine Veröffentlichung; lokale Notizen verwerfen |

Eine öffentliche URL ist keine Zugriffskontrolle: Jede Person mit Link kann die Prüffassung aufrufen. Sie bleibt ausdrücklich „keine Unterrichts- oder Produktfreigabe“. Dieser Implementierungsauftrag autorisiert das Starten des Workflows nicht.

## Autorisierungsprüfung

| Rolle | Eingabe | Aktion | Erwartete Evidenz | Fehlerzweig | Bereinigung |
| --- | --- | --- | --- | --- | --- |
| beauftragende Stelle | Prüfauftrag und Preview-ID | Nichtfreigabe bestätigen; Pattern der Preview-ID prüfen; `main` als Quelle prüfen | Bestätigung und gültige ID liegen außerhalb des Repositories vor | eine Bedingung fehlt: nicht starten | keine Artefakte erzeugen |
| Engineering | Zielkonfigurationen und Richtlinienzugang | Zugang zu Geräten, Netz und LMS vorab bestätigen | sechs prüfbare Matrixzeilen oder genau eine begrenzte Ausnahme | mehr als eine Zeile nicht prüfbar: stoppen | temporäre Sitzungen schließen |

## Exakte Buildidentität

| Rolle | Eingabe | Aktion | Erwartete Evidenz | Fehlerzweig | Bereinigung |
| --- | --- | --- | --- | --- | --- |
| Engineering | vollständiger Commit-SHA und Preview-ID | lokal `IUM_BUILD_REVISION` und `IUM_PREVIEW_ID` setzen; `npm run verify:ium5:gate-b` ausführen | Banner und Metadaten enthalten exakt dieselbe Identität | SHA, ID oder Build widersprechen sich: nicht veröffentlichen | Umgebungsvariablen löschen; Buildverzeichnis neu erzeugen |

Kein Kurz-SHA, kein Branchname und kein Zeitstempel ersetzt die vollständige Buildidentität.

## Veröffentlichung und Rollback

| Rolle | Eingabe | Aktion | Erwartete Evidenz | Fehlerzweig | Bereinigung |
| --- | --- | --- | --- | --- | --- |
| autorisierte betreibende Rolle | bestätigter Auftrag und grüner Verifikationslauf | manuellen Workflow `ium5-gate-b-preview.yml` mit Bestätigung und Preview-ID starten | Pages-Artefakt stammt aus dem erwarteten SHA; Nichtfreigabebanner erscheint auf jeder Route | Build-, Qualitäts- oder Pages-Schritt schlägt fehl: nicht pilotieren | fehlgeschlagenes Artefakt nicht verwenden |
| autorisierte betreibende Rolle | Abbruchentscheidung | Pages-Prüffassung deaktivieren oder durch den letzten ausdrücklich akzeptierten Prüfbau ersetzen | URL liefert keine ungekennzeichnete oder widersprüchliche Fassung | Rollback nicht eindeutig: Zugriff aussetzen | Browser-/PWA-Caches der Prüfgeräte kontrolliert leeren |

## Technische Sechs-Zeilen-Matrix

| Matrix-ID | Ziel | Mussbefund |
| --- | --- | --- |
| `TECH-IPAD-TOUCH` | verwaltetes iPad, Safari, Touch | Kernpfad, lokale Datenaktionen und Touchbedienung funktionieren |
| `TECH-IPAD-VO` | verwaltetes iPad, Safari, VoiceOver | Struktur, Fokus, Status, Szene, Laufspur und Fehler sind verständlich |
| `TECH-DESKTOP-CHROMIUM` | verwalteter Desktop, Chromium, Tastatur | Kernpfad, Reflow, Zoom und Dateidialoge funktionieren |
| `TECH-DESKTOP-FIREFOX` | verwalteter Desktop, Firefox, Tastatur | Kernpfad, Reflow, Zoom und Dateidialoge funktionieren |
| `TECH-NET-OFFLINE-UPDATE` | Schulnetz, Offline und Update | Erstladen, Offline-Neuladen und fail-closed Update funktionieren ohne Drittanfragen |
| `TECH-LMS-ROUTE` | reale schulische LMS-Route | Link oder Einbettung sowie eigener-Tab-Fallback sind nachvollziehbar |

Pro Zeile dokumentiert Engineering nur geschlossene Prüfcodes, Ergebnis, Schweregrad, Status und einen privaten Evidenzverweis. Alle sechs Zeilen müssen dieselbe Buildidentität betreffen.

## Evidenzhygiene

Reale Evidenzpakete und Rohbelege bleiben außerhalb des Git-Repositories. Erfasst werden nur geschlossene Kategorien und technische Reproduktionsschritte ohne Personen- oder Gerätebezug. Das öffentliche Repository enthält ausschließlich die synthetischen Beispiele.

### Verboten

<!-- PRIVACY-PROHIBITED-EXAMPLES:START -->
Nicht als Felder oder Arbeitsaufträge verwenden: `Name:`, `Schule:`, `Klasse:`, `Datum:`, `Freitext`, `Screenshot der Lernenden`, `IP-Adresse`, `Geräte-ID`, `Einzelantwort`.
<!-- PRIVACY-PROHIBITED-EXAMPLES:END -->

Ein unerwarteter Drittrequest, eine verbotene Datenspur oder Telemetrie beendet den Lauf. Der Befund wird nur mit geschlossenem Störungscode und privatem Evidenzverweis weitergegeben.

## Begrenzte Ausnahme

Genau eine nicht verfügbare technische Zielzeile darf ausschließlich für den explorativen Lauf als `limited-accepted` behandelt werden. Erforderlich sind Entscheidung der beauftragenden Stelle, derselbe Preview-Build, mindestens eine kompensierende Kontrolle, geschlossene Abbruchcodes und sofortiger Fallback. Die Bestätigungsrunde verlangt vollständige technische Evidenz; die Ausnahme kann niemals eine positive Gesamtempfehlung erzeugen.

## Abbruchbedingungen

Sofort stoppen bei falscher Buildidentität, fehlender Kennzeichnung, Start- oder Interaktionsverlust, Zustandsverlust, Import-/Exportfehler, nicht funktionsfähigem Offline-/Updatepfad, Barrierefreiheitsblocker, Netz-/LMS-Blocker, Datenschutzverletzung oder Zusammenbruch der vorgesehenen Lernzeit. Die prüfende Rolle setzt den geschlossenen Code, schützt nur den minimalen privaten Beleg und aktiviert den vorbereiteten Fallback. Es gibt keine spontane Erweiterung des Datensatzes.

## Löschung und Übergabe

| Rolle | Eingabe | Aktion | Erwartete Evidenz | Fehlerzweig | Bereinigung |
| --- | --- | --- | --- | --- | --- |
| Engineering | abgeschlossene technische Matrix | geschlossenes technisches Paket an die Reviewrollen übergeben | Prüfsumme, SHA und Preview-ID stimmen überein | Widerspruch: Paket `not-evaluable` | lokale Kopien auf notwendige Arbeitskopie reduzieren |
| Koordination | abschließende Entscheidung | Löschung realer digitaler Pakete spätestens 30 Tage nach der Entscheidung terminieren und bestätigen | Status `deleted`; Papieraggregate `destroyed` oder `not-used` | Löschung nicht bestätigt: keine positive Empfehlung | Backups und temporäre Exporte in den Löschumfang aufnehmen |
