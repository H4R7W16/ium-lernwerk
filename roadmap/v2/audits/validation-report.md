# IUM-V2-AUD – Gegenprüfung und Validierung

Stand 2026-09-06. Ausgangscommit `9f52cdc6f5e36b72b7a3fd9e64501ccfc4af2135`. Autor/Prüfer: Codex. Prüfart: KI-gestützter Dokumentenselbstreview. Keine unabhängige menschliche Prüfung oder neue tatsächliche Nutzung behauptet. Die GOV-Nutzerabnahme liegt explizit vor; die Audit-Nutzerabnahme steht aus.

## Prüfumfang

25 historische Artefaktfamilien mit genau einer Entscheidung, 59 unterschiedliche V1-Dateien am versiegelten Commit, vier ausschließlich im eingefrorenen LXP05-Kandidaten untersuchte Dateien, zwölf konkrete Nachfolgetasks und 16 weitergegebene Fragen. Die V2-Anforderungs- und Grundlagenbelege werden pro Familie benannt. Herkunft und Textanker werden gegen Git geprüft; ergänzende Belege sind als solche kenntlich.

Die Entscheidungen lauten 1 retain, 15 adapt, 5 replace, 4 reference-only und 0 drop. Keine Datei wird gelöscht oder als Folge des Audits in eine neue Produktfassung übernommen. `retain` betrifft ausschließlich den quellentreuen IUM05-Extraktionsbestand im angegebenen historischen Geltungsbereich.

## Prüfung nach Familien

| Familie | Ergebnis |
| --- | --- |
| IUM00–IUM04: Forschung | Quellen-/Claimhygiene und begrenzte Designfolgen bleiben nutzbar; Anpassung an V2-Verträge, Jahrgang und konkrete Lernhandlung. Datierte Rechts-/Technikfolgen benötigen vor Verwendung passende Rechecks. |
| IUM05–IUM10: Curriculum/Planung | Extraktionsdaten erhalten; alte Steuerungs-, Kandidaten- und Zeitfassungen ersetzen; recordgenaue Lückenanalyse adaptieren; historischer Abschlussbericht nur als Referenz. |
| IUM11–IUM15: Technik/Gates | Instrumente und technische Systemgrenzen adaptieren; Geräte-Teilbefunde als Referenz erhalten; frühere Entwicklungserlaubnis hebt V2-Freeze nicht auf. |
| IUM16–IUM20: Modul/Pilot | Modulspezifikation ersetzen, alter Plan nur Referenz, Fachlogik und Instrumente selektiv adaptieren. Konkrete Folgeaufträge bleiben gesperrt. |
| LXP01–LXP04 | Die vier freigegebenen LXF01-Entscheidungen und ihre primären Nachfolger unverändert bestätigt. |
| LXP05 gesondert | Keine Übernahmeentscheidung. Vier versionierte Belege und vier begrenzte Lehren mit V2-Antworten und Folgeaufträgen dokumentiert. |

## Querschnittliche Gegenfälle

1. **Früher done = heute retain?** Nein. IUM08 und IUM17 bleiben Referenzen; jede Entscheidung besitzt einen tatsächlichen Artefaktanker und V2-Bezug.
2. **278 extrahierte Records = volle V2-Abdeckung?** Nein. IUM05 retain erhält Daten/Herkunft, nicht Modulmapping, Jahresplanung oder Coverage. `unassessed` bleibt bestehen.
3. **Working-40 = neues V2-Ziel?** Nein. IUM10 replace verlangt neue R5/R6/R7-Zeitentscheidungen; Fallbackzeit und ausgefallene Kompetenz werden nicht verschleiert.
4. **Fiktiver Schutzfall = Eigenbezug erledigt?** Nein. CUR-Q-002 bleibt als eine Frage mit zwei Quellen erhalten. Querschnittliche Werkzeugnutzung erzeugt keinen künstlichen Zeit-/Aufgabenblock.
5. **IUM06 replace widerspricht LXF01 adapt?** Nein. Ersetzt wird der steuernde Gesamtverbund; einzelne Claims, Prinzipien und Profilbefunde werden in getrennte V2-Verträge adaptiert. Die vier LXP-Entscheidungen stimmen dagegen auf derselben Ebene exakt überein.
6. **Abgeschlossener Nachfolger = fertiges Produkt?** Nein. Sechs completed-foundation-Nachfolger belegen nur die ausgeführte Grundlagenarbeit. Roadmaps und konkrete Produkt-/Prüfinstrumentarbeit sind getrennt registriert.
7. **Grüne Technik = complete device-verified?** Nein. IUM14 enthält begrenzte reale Teilbeobachtungen und offene Konfigurations-/Umgebungsnachweise. Automatisierung ergänzt diese nicht.
8. **Implementiertes Pilotpaket = reale Pilotierung?** Nein. IUM11 und IUM20 sind Instrumente, keine durchgeführten V2-Piloten. Gruppenschwellen und Löschfristen werden nicht zu pauschalen Rechtsvorgaben.
9. **LXP05-Code ist vorhanden = darf übernommen werden?** Nein. Der eingefrorene Kandidat bleibt außerhalb der 25er-Menge. Auch formal gute Bausteine werden hier weder integriert noch zur Wiederverwendung freigegeben.
10. **GOV-Freigabe = institutionelle Fragen geschlossen?** Nein. Der additive Abnahmebeleg akzeptiert den dokumentierten Scope mit fünf offenen Folgefragen; alle bleiben in der Fragenübergabe erhalten.

## Technische Verifikation

Frische Prüfungen am 2026-09-06:

- 20 neue Audit-Tests bestanden; Negativfälle wurden zuerst mit fehlendem Validator rot ausgeführt. Der Integrationstest liest die tatsächlichen V1- und LXP05-Gitobjekte.
- 208 fokussierte Tests für Audit, Governance und bisherige V2-Verträge bestanden.
- `npm run test:python`: alle 883 Tests bestanden (118,657 Sekunden). Die ausgegebenen IUM11-Ablehnungen gehören zu erfolgreichen Negativtests.
- `npm run verify:v2`: gesamtes integriertes V2-Gate bestanden, einschließlich der bisherigen LXF07-/GOV-Prüfbindungen.
- Alle fünf neuen JSON-Instanzen gegen Draft-2020-12-Schema mit AJV geprüft; keine Schemafehler.
- 59 V1-Dateien gegen den archivierten Gitstand und vier separate LXP05-Belege gegen den Kandidaten geprüft. Alle 25 Inventarentscheidungen, zwölf Nachfolgetasks und 16 Fragen vollständig; 85 Audit-Prüfeingänge über SHA-256/UTF-8/LF gebunden.
- Repo-Diff auf Scope und Whitespace geprüft. Lokale Auditlinks und die zwölf Nachfolge-Task-Notizen lösen auf. Die bestehenden 35 LXF07- und 25 GOV-Prüfeingänge bleiben unverändert.

Der aktuelle Prüfumfang erfordert keine Änderung an Produktcode, Buildpfaden, V1-Dateien oder Abhängigkeiten. Neue Produktbuilds, Browser-, Realgeräte-, Nutzungs- oder Unterrichtstests wurden deshalb nicht ausgeführt und werden nicht behauptet. Die Frontmatter- und Handoff-Prüfung des Vaults sowie der finale Commit werden in der Session dokumentiert.

## Übergabe

Alle vier Task-Akzeptanzkriterien sind dokumentarisch behandelt: vollständige 25er-Menge, konkrete Nachfolger für adapt/replace, reale Artefaktbelege statt früherer Taskstatus und dokumentierte Gegenprüfung. Nach bestandenem technischen Gate geht der operative Task in `review`; Nutzerabnahme bleibt separat. R5 beginnt erst nach dieser ausdrücklichen Abnahme. Der finale lokale Commit und Pushstatus stehen im Vault-Handoff.
