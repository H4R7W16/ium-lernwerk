---
review: IUM5-GATE-B-ENGINEERING-ACCESSIBILITY-PRIVACY
reviewedCommit: 2b4353d5d1a786d4d1ceddba71e3a7b2bdfe28d9
verdict: APPROVED AFTER FIXES
reviewedAt: 2026-08-03
---

# IUM5 Gate B - Engineering-, Accessibility- und Privacyreview

## Aussagegrenze

Geprüft wurde der Implementierungsbereich `3c38799c76ebf0536501dd64adfdd97935fe5594..2b4353d5d1a786d4d1ceddba71e3a7b2bdfe28d9`. Es wurde kein Pages-Workflow ausgeführt, kein Preview deployed und keine reale Evidenz erhoben. Ein grünes Review verändert weder `status: working` noch `device-verified: not-run`.

## Prüfgegenstand

- geschlossene Protokoll- und JSON-Schemaverträge, lokale Referenzen und rekursives `additionalProperties: false`;
- fail-closed Schema-, Privacy-, Evidenz- und Entscheidungsvalidierung;
- Unterdrückung kleiner Rückmeldungsaggregate und Datenschutzvorrang;
- orthogonale Trennung von Buildprofil und Publikationsmodus;
- Previewisolation, Metadaten, Nichtfreigabebanner, `noindex`, Buildidentität, Service Worker und Qualitätsbudgets;
- manueller main-only Pages-Workflow mit Bestätigung und Least Privilege sowie Vier-Job-CI ohne Deployment;
- technische Sechs-Zeilen-Matrix, Offline-/Updatepfad, Barrierefreiheit, Netzwerkgrenze, Löschung und unveränderte Legacyverträge;
- einseitiger, skriptfreier und netzunabhängiger Druckbogen.

## Evidenz

| Evidenz | Ergebnis |
| --- | --- |
| `npm ci` | 665 Pakete geprüft, 0 Schwachstellen |
| `npm run verify:ium5` | 24/24 Schritte erfolgreich |
| `npm run verify:ium5:gate-b` | 8/8 Schritte erfolgreich |
| `npm run test:platform` | 25 Testdateien, 132 Tests erfolgreich |
| vollständige Browser-/Offline-/Accessibility-Suites | 93 Fälle erfolgreich; Chromium, Firefox und WebKit enthalten |
| `python -B -m unittest discover -s tests -p "test_*.py"` | 669 Tests erfolgreich |
| Gate-B-Preview-Qualitätsbericht | keine Drittanbieter-URL, kein Testidentifier, keine Basispfadverletzung, keine Budgetverletzung |
| `python -B scripts/validate_ium5_gate_b.py protocol` und `synthetic` | Protokoll sowie sechs Beispiele mit drei erwarteten Entscheidungsresultaten gültig |
| Git-Diff der Schutzdateien | `module.yaml`, Geräteprotokoll und bestehender Fixture-Workflow unverändert |

## Stärken

- Der Validator arbeitet rein lesend, löst nur lokale Schema-Referenzen auf und lehnt unbekannte Felder rekursiv ab. Verbotene Feldnamen und sensible Stringmuster werden vor semantischer Bewertung geprüft.
- Datenschutz hat in der reinen Entscheidungsfunktion Vorrang. Fehlende oder widersprüchliche Evidenz bleibt `not-evaluable`; `limited-accepted` kann keine positive Empfehlung erzeugen.
- `PublicationMode` ist unabhängig vom Inhaltsprofil, aber nur drei explizite Kombinationen sind erlaubt. Ungültige Paare scheitern vor Registry, Assets und Astro.
- Jede Preview-HTML-Seite trägt Nichtfreigabe, `noindex`, SHA, Preview-ID, `working` und `not-run`. Fixture und Preview bleiben gegenseitig isoliert; es wurde kein neuer Speicher- oder Netzwerkkanal eingeführt.
- Pages ist nur manuell, main-only und bestätigungspflichtig. Schreibrechte auf Pages und OIDC existieren ausschließlich im getrennten Deployjob; CI bleibt ohne Deployment und bei vier Jobs.
- IUM11 besitzt wieder nur seinen eigenen Publikationsnamespace und schützt weiterhin unerwartete IUM11-Dateien, ohne das neue Gate-B-Paket abzuweisen.

## Befunde und verifizierte Korrekturen

### EAP-01 - Wichtig - eingebetteter 40-Zeichen-Geheimniskandidat wurde nicht erkannt

- Vorbefund auf Commit `fd72620`: Der Privacy-Scanner erkannte einen Kandidaten nur dann, wenn der gesamte String exakt 40 alphanumerische Zeichen lang war. Ein innerhalb eines längeren Werts abgegrenztes Token blieb unentdeckt.
- Reproduzierender Test: `test_sensitive_string_patterns_are_rejected` enthält nun `token=<40 Zeichen>;redacted` und war vor der Korrektur rot.
- Korrektur: Commit `2b4353d` verwendet Token-Grenzen und `search`, während ein vollständig typisierter, kleingeschriebener SHA ausschließlich an `build.buildRevision` zulässig bleibt.
- Verifikation: 29 Gate-B-Validatorfälle und 669 Python-Tests grün; vollständige 24/24- und 8/8-Ketten grün.

### EAP-02 - Mittel - Druckkontrolle und Beschriftung konnten getrennt umbrechen

- Vorbefund und Auswirkung entsprechen FD-01.
- Korrektur: Commit `fd72620` mit untrennbaren `option-pair`-Gruppen.
- Verifikation: DOM-Vertrag, einseitiger A4-Render und visuelle Prüfung bei 100 %/200 % grün.

## Offene Befunde

- Kritisch: keine.
- Wichtig: keine.
- Mittel: keine.
- Gering: keine blockierenden Hinweise.

## Urteil

`APPROVED AFTER FIXES`

Das Gate-B-Paket ist technisch, barrierebezogen und datenschutzseitig für den schriftlichen Implementierungshandoff geeignet. Das Urteil ist keine Deployment-, Geräte-, Pilot-, LMS- oder Releaseentscheidung.
