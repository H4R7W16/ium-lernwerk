# FU-TECH – Prüfnachweis und Aussagegrenzen

Prüfdatum: 06.09.2026. Produktinput: `32b523a657a3e6717a83fd9aaa755c8deed9adbf`. Plattform: Windows; Node **22.23.2**, npm **10.9.8**, bestehender Lockstand. Automatisierte Prüfungen verwenden ausschließlich synthetische Daten. Keine echte Geräte-/Schulnetz-/LMS-Prüfung, keine Lernendenbeteiligung, keine neue Accessibility-Konformitätserklärung und keine unabhängige Begutachtung.

## Ergebnis je Prüfschicht

| Prüfschicht | Tatsächliches Ergebnis | Aussagegrenze |
| --- | --- | --- |
| Vertragsgenerierung, Paketgrenzen, Typecheck, Astro | Bestanden; sieben Workspaces, Astro 15 Dateien/0 Fehler | Unveränderter V1-Technikstand. |
| Vitest Plattform | **132/132 bestanden**, 25 Testdateien | Vorhandene Tests; schließen die zusätzlich gefundenen F01–F08 nicht. |
| Produkt-, Fixture- und Unterpfadbuild | Bestanden | Lokale Builds, keine Bereitstellung. |
| Buildqualität | Keine gemeldeten Verstöße; keine Drittanbieter-URLs oder Basispfadverstöße im geprüften Fixture-Ausgabestand | Kein gemessener Schulnetz- oder neuer V2-Produktbeleg. |
| Abhängigkeitslizenzen | **647 Pakete**, 647 SBOM-Komponenten, neun geprüfte Ausnahmen, keine ungültigen Einträge | Keine Prüfung aller Asset-/Marken-/Persönlichkeitsrechte und kein aktueller Vulnerabilityscan. |
| Standard-Plattformbrowserlauf | Je sechs Chromium- und WebKitfälle bestanden; sechs Firefoxfälle scheiterten vor Seitenanlage | Gesamtlauf bei Schritt 11/24 nicht bestanden; hängenden Abschluss beendet. Kein `verify:ium5 24/24` behauptet. |
| Vollständiger Chromium-Plattformnachlauf | **23/23 bestanden**, Exit 0, 46,2 s: Plattform, Offline und Accessibility | Bestehende Testdateien unverändert; Server separat auf dem im Test festgelegten Port 4321 gestartet. |
| Erweiterter IUM5-Browserlauf | **53 bestanden, fünf WebKitfehler**, Exit 1; Chromium 29/29, WebKit 24/29 | Werkstatt, Zustand und Accessibility gemeinsam auf beiden Engines. Der reguläre Gatevertrag beschränkt Zustand/Accessibility auf Chromium; die WebKit-Ausweitung ist zusätzliche Auditevidenz. |
| Gezielter WebKit-Nachlauf | **Vier bestanden, ein Fokusfehler**, Exit 1 | Fünf vorher fehlgeschlagene Fälle mit einem Worker wiederholt. Vier schwankende Ergebnisse bleiben als Unsicherheit dokumentiert. |
| IUM5 offline/update, Chromium | **3/3 bestanden**, Exit 0, 24,9 s | Lokale installierte Produktsimulation, vollständiger/defekter Kandidat; kein Test der F06-Verlustkonstellation auf realem Gerät. |
| Pythonregression | **1.017/1.017 bestanden**, 147,806 s | Bestehende Validatoren/Verträge einschließlich historischer Siegel. |
| IUM11-Projektionen, IUM11/10/09 und Phase 0 | Bestanden | Historische Produkt-/Planungsverträge, keine V2-Modulfreigabe. |
| V2 und Aktivierung | Beide CLI-Prüfungen bestanden, Aktivierung zusätzlich mit tatsächlichem Vaultpfad | Aktive Planungsbaseline und historische Inputs intakt. |
| Dashboard-Unit-Tests | **32/32 bestanden**, 130,932 s | Keine neue HTML-Browserprüfung. Historische Nachfolgerprojektion bleibt separat dokumentiert. |
| Befundprobe | **Sechs Beobachtungen reproduziert**, Exit 0 | `findingObserved: true` bestätigt den Mangel, nicht dessen Behebung. F01 hat zwei Fälle; F02/F03/F04/F06 je einen. |
| Auditvollständigkeit und Hashes | **52 eindeutige Dateien**, vier Familien, acht Migrationskategorien, **61 Inputhashes** und alle **14** ursprünglichen Primär-/Zusatzbelege geprüft | Dateientwicklung seit diesem Input erfordert neuen Review. |
| Git-Produktvergleich | `git diff --exit-code HEAD` vor Aufnahme der neuen Auditdateien leer | Keine bestehende Produkt-, Schema-, Workflow- oder Testdatei geändert. |

Die Zählungen verschiedener Läufe werden nicht addiert: Mehrfach geprüfte Fälle sind keine zusätzlichen unabhängigen Nachweise. Das Gesamturteil ist **Audit ausgeführt, technische Übernahme bedingt, vollständige Browsermatrix offen**.

## Prüflaufdetails und Umgebungsgrenzen

Der vollständige Start erfolgte mit `npm run verify:ium5`. Die Schritte 1–10 waren erfolgreich. Firefox scheiterte in allen sechs Plattformfällen mit `browserContext.newPage: Cannot read properties of undefined (reading '_page')`. Ein separater minimaler Firefoxstart mit leerem Kontext reproduzierte denselben Fehler ohne Aufruf des Projekts. Der vollständige Lauf blieb beim Abschluss hängen und wurde beendet. Ursache des Firefoxprüfpfads bleibt offen.

Auch der erste separate Plattform-Offline-/Accessibilitylauf erreichte 17 erfolgreiche Fallausgaben, blieb aber im Serverabschluss hängen. Deshalb wurden die lokalen Server anschließend getrennt vom Playwright-Runner gestartet; die Produkt- und Testdateien wurden dafür nicht geändert. Temporäre Konfigurationen unter `reports/fu-tech/` entfernen nur den automatischen `webServer`, setzen das Ausgabeverzeichnis und wählen die jeweilige Browsermatrix.

Ein zunächst verwendeter Ausweichport 4331 war für diese Tests ungeeignet: Vier Netzprüfungen vergleichen hart gegen Origin 4321, der iframe-Fall verwendet ebenfalls ausdrücklich 4321. Dieser Konfigurationsfehler ergab 18 erfolgreiche und fünf fehlgeschlagene Fälle und wird **nicht als Produktmangel** gewertet. Nach Rückkehr zum vorgesehenen Port 4321 bestand der vollständige Chromiumlauf mit 23/23 Fällen. Der erfolgreiche Nachlauf ersetzt diese ungültige Konfiguration, nicht die offenen Firefox-/WebKitbefunde.

Der neue IUM5-WebKit-Fokusbefund ist eine Abweichung zwischen Pointerklick und erwarteter Fokusposition. Die Fehlerursache und Bedeutung für den tatsächlichen Tastatur-/Screenreaderpfad sind weiter zu untersuchen. Die vier zunächst fehlgeschlagenen und später bestandenen Fälle werden nicht stillschweigend als stabil verifiziert bezeichnet. Einzelheiten: [F08](findings.md#tech-f08--aktuelle-technische-zielmatrix-bleibt-unvollständig-mittel).

## Reproduktion

Im Repository mit passender Node-22-/npm-10-Laufzeit:

```powershell
npm run verify:ium5
python -B scripts/validate_v2_rebaseline.py
python -B scripts/validate_v2_activation.py --vault ../../Vault
npm run test:dashboard
node --import tsx roadmap/v2/follow-ups/technical/probe.mts
```

Die dokumentierten Browsernachläufe verwendeten unveränderte Testdateien:

- Plattform: `platform.spec.ts`, `offline.spec.ts`, `accessibility.spec.ts`, Chromium, Origin `http://127.0.0.1:4321`, ein Worker.
- IUM5: `ium5-workbench.spec.ts`, `ium5-state.spec.ts`, `ium5-accessibility.spec.ts`, Chromium/WebKit, Origin `http://127.0.0.1:4322`.
- Gezielter Nachlauf: die fünf in F08 benannten WebKitfälle, ein Worker.
- IUM5 offline: `ium5-offline.spec.ts`, Chromium, ein Worker, Origin 4322.

Inputhashes lassen sich ohne projektspezifische Hilfssoftware erneut prüfen (Befehl im Repo):

```powershell
python -c 'import json,pathlib,hashlib; d=json.loads(pathlib.Path("roadmap/v2/follow-ups/technical/inventory.json").read_text(encoding="utf-8")); r=d["records"]+d["contracts"]; assert all(hashlib.sha256(pathlib.Path(x["path"]).read_text(encoding="utf-8-sig").encode()).hexdigest()==x["sha256"] for x in r); print(len(r), "Inputhashes korrekt")'
```

Python normalisiert beim Textlesen CRLF zu LF; Hashformat ist UTF-8 ohne BOM. Das Inventar bindet den tatsächlichen Auditinput, nicht einen zukünftigen Commit seiner eigenen Dateien.

## Belegablage

`validation.json` hält Zählungen, Grenzen und SHA-256 der lokalen Logs. Die ausführlichen Logs und Browsertraces liegen **nicht versioniert** unter `reports/fu-tech/`. Sie sind vollständig synthetisch. Der Befundlauf samt Ergebnis, Dateiinventar und diese Auswertung sind dagegen Teil des Audits. Ein späterer Repo-Klon kann die Probes und Inputprüfung reproduzieren; ohne die lokale Logablage besitzt er die kuratierte Auswertung, nicht die vollständigen Rohtraces.

## Noch erforderliche reale Nachweise

Die vorhandenen iPad-Teilbeobachtungen vom 03.08.2026 sind historische IUM14-Evidenz zu anderen Kandidaten; Geräte-/Policyangaben bleiben dort teilweise unbekannt. Sie werden nicht gelöscht oder nachträglich als neuer V2-Lauf gewertet.

Vor betroffenem Betrieb: konkreter Kandidatenhash, Gerät/OS/Browser, MDM/Web-Clip, tatsächliches Schulnetz/Proxy, Storage-/Löschpolicy, LMS-Einbettung, Export-/Clipboardablage, Offline-/Update-/Recovery- und Mehrtabfälle sowie VoiceOver/Tastatur dokumentieren. Prüfende, Betreiber-/Schulverantwortung und Rechtefreigaben sind gemäß GOV vorher zu benennen. FU-PILOT ist ein eigener Spezifikationsauftrag, keine durch diesen Audit ausgelöste Durchführung.
