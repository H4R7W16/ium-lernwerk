# Datenvertrag für Quellen und Claims

Dieser Vertrag definiert die maschinenprüfbaren Grunddaten von Phase 0. Die JSON-Dateien verwenden UTF-8 und jeweils `schemaVersion: 1`.

## Quellenregister

`source-register.json` enthält ein Objekt mit dem Array `sources`. Jeder Eintrag benötigt diese Felder:

| Feld | Typ | Bedeutung |
| --- | --- | --- |
| `id` | String | Eindeutige Kennung, beginnend mit `SRC-`. |
| `package` | String | Recherchepaket oder `official` für amtliche Quellen. |
| `sourceKind` | Enum | Art der Quelle. |
| `title` | Nichtleerer String | Vollständiger Titel der Quelle. |
| `authors` | Array | Autorinnen, Autoren oder herausgebende Institutionen. |
| `year` | Zahl oder `null` | Veröffentlichungsjahr. |
| `url` | String oder `null` | Direkte Fundstelle. |
| `doi` | String oder `null` | DOI, soweit vorhanden. |
| `license` | String | Lizenz- oder Nutzungsstatus. |
| `accessed` | String | Abrufdatum im ISO-Format. |
| `verificationStatus` | Enum | Umfang der Quellenprüfung. |
| `relevance` | Nichtleeres Array | Relevante Entscheidungs- oder Inhaltsbereiche. |

Zulässige `sourceKind`-Werte sind `official`, `systematic-review`, `meta-analysis`, `empirical-study`, `research-synthesis`, `handbook`, `professional-standard` und `secondary`. Zulässige `verificationStatus`-Werte sind `primary-checked`, `metadata-checked` und `secondary-only`.

## Claim-Ledger

`claim-ledger.json` enthält ein Objekt mit dem Array `claims`. Jeder Eintrag dokumentiert:

| Feld | Typ | Bedeutung |
| --- | --- | --- |
| `id` | String | Eindeutige Kennung für den Claim. |
| `package` | String | Zugehöriges Recherchepaket. |
| `statement` | String | Kuratierte, überprüfbare Aussage. |
| `scope` | String | Reichweite der Aussage. |
| `status` | Enum | Bearbeitungs- und Prüfstatus. |
| `evidenceLevel` | Enum | Stärke oder normative Art der Evidenz. |
| `sourceIds` | Array | Ausschließlich IDs aus dem Quellenregister. |
| `limitations` | String | Übertragungsgrenzen, Unsicherheiten oder Einschränkungen. |
| `designImplications` | Array | Von der Evidenz getrennte mögliche Designfolgen. |

Zulässige `status`-Werte sind `draft`, `working`, `reviewed` und `standard`. Zulässige `evidenceLevel`-Werte sind `low`, `medium`, `high` und `normative`.

Deterministische Claim-Präfixe sind `CLAIM-INF-`, `CLAIM-MED-`, `CLAIM-LP-` und `CLAIM-DLE-`. Quellen-IDs beginnen mit `SRC-`. Identifikatoren bleiben ASCII-stabil, auch wenn der sichtbare Text deutsche Umlaute verwendet.

Ein Claim mit Status `reviewed` oder `standard` benötigt mindestens eine registrierte Quelle, nichtleere `limitations` und mindestens eine zitierte Quelle mit `verificationStatus: primary-checked`. Dies ist die technische Mindestschwelle dafür, dass die Aussage gegen eine Originalquelle geprüft wurde. `metadata-checked` und `secondary-only` bleiben im Register zulässige Statuswerte, reichen jedoch nicht für einen Claim in diesen beiden Statusstufen.

`validate_source_register` liefert weiterhin eine mengenkompatible Sammlung der Quellen-IDs. Im regulären Pfad enthält sie zusätzlich die Prüfstatus-Metadaten, damit `validate_claim_ledger` die Mindestschwelle durchsetzen kann. Ein übergebener einfacher ID-`set` bleibt für bestehende Aufrufe zulässig; er kann nur die Registrierung, nicht jedoch den Prüfstatus einer Quelle abbilden.
