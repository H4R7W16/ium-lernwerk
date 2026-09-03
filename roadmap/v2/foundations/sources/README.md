# V2-Quellenfundament – Reviewbasis

**Stichtag:** 2026-09-03  
**Gate:** `IUM-V2-SRC-REVIEW`  
**Status:** zur fachlichen Nutzerprüfung; keine Inhalts-, Pilot- oder Releasefreigabe

## Ergebnis

Das V2-Quellenfundament verbindet den vorhandenen Quellenbestand und die später dokumentierten LXP01-Ergänzungen, ohne V1-Dateien umzuschreiben oder neue Claims vorwegzunehmen:

- 63 Phase-0-Quellen, 51 Claims und 15 Designprinzipien bleiben über Pfad, SHA-256 und Anzahl als unveränderter V1-Auditinput versiegelt.
- Die sechs LXP01-Quellen besitzen eindeutige V2-IDs und einen Migrationsstatus; eine mögliche Claim-Migration bleibt für jede Quelle bis `IUM-V2-LXF02` offen. V2-Claims wurden noch nicht angelegt.
- Die 51 vorhandenen Claims referenzieren 57 registrierte, primär geprüfte Phase-0-Quellen.
- Quelle, Claim, Projektentscheidung, Gestaltungsprinzip, Materialmuster und Prüfnachweis sind getrennt definiert und dürfen nur in den festgelegten Richtungen aufeinander verweisen.
- Der Linkaudit umfasst 69 Fundstellen: 46 liefern nach vollständiger Redirectverfolgung einen terminalen 2xx-Status, 23 antworten terminal kontrolliert mit HTTP 401 oder 403, keine ist fehlend oder ungeklärt.

Online-Erreichbarkeit belegt weder fachliche Qualität noch Lizenzfreiheit oder Lernwirksamkeit.

## LXP01-Migration und Nutzungsgrenzen

| V2-ID | Fundstelle | Prüfstatus | Lizenz-/Nutzungsgrenze | Mögliche Claim-Migration |
|---|---|---|---|---|
| `SRC-LXP-SDT-2024` | [DOI](https://doi.org/10.1016/j.lmot.2024.102015) | Metadaten geprüft | keine offene Nachnutzung belegt; Zitat und Link | offen bis LXF02 |
| `SRC-LXP-SEGMENT-2019` | [DOI](https://doi.org/10.1007/s10648-018-9456-4) | Metadaten geprüft | keine offene Nachnutzung belegt; Zitat und Link | offen bis LXF02 |
| `SRC-LXP-SIGNAL-2016` | [DOI](https://doi.org/10.1016/j.edurev.2015.12.003) | Metadaten geprüft | keine offene Nachnutzung belegt; Zitat und Link | offen bis LXF02 |
| `SRC-LXP-W3C-COGA-2021` | [W3C Supplemental Guidance](https://www.w3.org/WAI/WCAG2/supplemental/) | Primärseite geprüft | ergänzende, nicht normative WCAG-Hilfe; Nachnutzung nur unter Beibehaltung der Hinweise gemäß [W3C Document License 2023](https://www.w3.org/copyright/software-license-2023/) | offen bis LXF02 |
| `SRC-LXP-UDL30-2024` | [CAST UDL Guidelines 3.0](https://udlguidelines.cast.org/) | Primärseite geprüft | keine offene Lizenz für pauschale Übernahme belegt; Zitat und Link gemäß [CAST Terms of Use](https://www.cast.org/terms-of-use/) | offen bis LXF02 |
| `SRC-LXP-COS-2023` | [DOI](https://doi.org/10.1016/j.compedu.2023.104864) | Metadaten geprüft | keine offene Nachnutzung belegt; Zitat und Link | offen bis LXF02 |

Die frühere LXP01-Spezifikation dient hier nur als Herkunftsnachweis der sechs Quellenidentitäten. Ihre Befundtexte und Designhypothesen gelten nicht automatisch als V2-Claims.

## Bewusste Grenzen und offene Punkte

1. `SRC-LP-SIGNALING-2018` ist eine metadatengeprüfte Phase-0-Quelle ohne Claimbezug. Sie ist optional, wird im Gate nicht als Fehler behandelt und muss vor einer möglichen Verwendung in LXF02 primär geprüft werden.
2. 23 Fundstellen – darunter DOI-Ziele bei Verlagen und `SRC-MED-DCE-PLANNER-2026` – antworten beim automatisierten terminalen Abruf mit HTTP 401 oder 403. Sie sind technisch zugriffsbeschränkt; der Status `restricted` wird deshalb von `missing` getrennt und bleibt im Einzelnachweis sichtbar.
3. Der Lesehilfe-Locator wird ausschließlich im V2-Inventar ergänzt. Die direkte amtliche PDF-Fundstelle und deren Inhaltsidentität sind im Curriculumfundament dokumentiert; das V1-Register bleibt unverändert.
4. Lizenzstatus wird bei Claimreview, vor Veröffentlichung sowie bei einer Locator- oder Lizenzänderung erneut geprüft.

## Verträge und Reproduktion

- `inventory.json`: versiegelte Baseline, Locator-Override und sechs Migrationsdatensätze
- `traceability.json`: Entitätengrenzen, Claimprüfung und Pflicht-/Optionaltrennung
- `link-audit.json`: datierter, atomar geschriebener Erreichbarkeitssnapshot
- `status.json`: konservativer Reife- und Reviewstatus

Offline-Validierung:

```text
npm run verify:v2
```

Erneuter Online-Audit mit atomarer Aktualisierung:

```text
npm run verify:v2:sources:online
```

Bei einer nicht auflösbaren Pflichtquelle wird der vorhandene Snapshot nicht überschrieben. Eine nicht auflösbare optionale Quelle erzeugt eine Warnung und bleibt mit Eigentümer und Akzeptanzkriterium sichtbar.
