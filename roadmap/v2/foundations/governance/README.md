# Governancefundament V2

Stand: 2026-09-05, Ausgangscommit `d11a8bc69775525ec0162516275bb39f5dc9c441`. LXF07 wurde vom Nutzer fachlich freigegeben. Dieses Paket konsolidiert die Governance als Dokumentenvertrag zur Nutzerabnahme; es ist keine Betriebsfreigabe. Maßgeblich sind [Vertrag](governance-contract.json), [Status](status.json), [Inventar](inventory.md) und [Prüfbericht](validation-report.md).

## Verantwortlichkeiten und Entscheidungsrechte

Jan entscheidet als Auftraggeber über die Projektabnahme und nachfolgende Arbeitsaufträge. Codex erstellt Dokumente, führt technische Prüfungen aus und kennzeichnet seinen Selbstreview. Daraus entsteht weder eine unabhängige menschliche Fachprüfung noch eine Ernennung Jans zum Betreiber oder datenschutzrechtlich Verantwortlichen einer Einrichtung.

Die folgenden Rollen sind verbindliche Prüfaufgaben; ihre Besetzung für einen konkreten Einsatz ist noch offen (`assignedTo: null`). Eine Person kann mehrere Rollen übernehmen, muss ihre Rollen und mögliche Interessenkonflikte offenlegen. Ein benötigter unabhängiger Review darf nicht vom Autor selbst als unabhängig bescheinigt werden.

| Achse / Entscheidung | Prüfverantwortung | Freigabe und Grenze |
| --- | --- | --- |
| Curriculare Abdeckung | subject-didactics-reviewer | Jan nimmt Projektentscheidung ab; offizieller Plan und überprüftes Mapping bleiben maßgeblich. |
| Quellen und Evidenz-/Designkonzept | source-reviewer, subject-didactics-reviewer | Jan nimmt Fundament/Material ab; geprüfte Forschung verleiht dem Produkt keine eigene Wirksamkeit. |
| Implementierung und technische Verifikation | technical-reviewer | Exakte Revision und Testmatrix; tatsächliche Geräte-/Netzprüfung gesondert. |
| Accessibility | accessibility-reviewer | Konkreter Umfang und Einschränkungen; Betreiber entscheidet über erforderliche rechtliche Erklärung nach Prüfung. |
| Nutzungsprüfung und Unterrichtspilot | teacher-reviewer, privacy-reviewer | Separater Projektauftrag und konkrete schulische Einsatzentscheidung vor Erhebung. |
| Wirkungsnachweis | effect-reviewer | Methodisch belastbarer, kontextbezogener Nachweis und redaktionelle Abnahme; kein Automatismus aus Pilotabschluss. |
| Datenschutz und Betrieb | privacy-reviewer berät; operator / school-controller entscheiden im jeweiligen Zuständigkeitsbereich | Konkrete Stellen vor Betrieb/Einsatz benennen; Rechenschaft lässt sich nicht an Codex delegieren. |
| Rechte und Lizenzierung | rights-reviewer | Rechteinhaber bzw. befugte Stelle müssen Rechte einräumen können; Projektabnahme ersetzt das nicht. |
| Veröffentlichung und Cutover | integration-reviewer bereitet vor; Jan entscheidet Projektauftrag, zuständiger Betreiber die Betriebsfreigabe | Separater Nachweis, separate Freigabe, keine Summenampel. |

Die LXF06-Rollen `source-reviewer`, `subject-didactics-reviewer`, `accessibility-reviewer`, `teacher-reviewer`, `privacy-reviewer` und `integration-reviewer` bleiben erhalten. Die GOV-Rollen ergänzen sie für Technik, Rechte, Wirkung und Betrieb. Die dokumentierte LXF07-Nutzerabnahme bleibt gültig; offene spätere Rollen machen sie nicht rückwirkend zu einer institutionellen Prüfung.

## Sieben Aussagearten und ihr aktueller Stand

Alle öffentlichen V2-Produktaussagen bleiben in diesem Vertragsstand gesperrt. `foundation-only` bezeichnet einen begrenzten Fundamentbefund, keine einsatzfähige Oberfläche. `not-established` bedeutet: Der benötigte V2-Nachweis liegt nicht vor. Ein stärkerer Claim kann nicht durch viele schwächere Nachweise ersetzt werden.

| Aussage | Erforderlicher Mindestnachweis | Tatsächlicher V2-Stand |
| --- | --- | --- |
| curricular zugeordnet | Geprüftes Mapping konkreter Inhalte auf genaue Bildungsplananforderungen, Jahrgang, Niveau und Erfüllungsform; Lücken sichtbar | Quellenfundament geprüft; Modul-/Jahresabdeckung `unassessed`. |
| evidenzorientiert gestaltet | Geprüfte Quelle → begrenzter Claim → reviewed Designvertrag → nachgewiesene Umsetzung im behaupteten Gegenstand | LXF-Fundament reviewed; Materialien noch nicht produziert. |
| barrierearm entwickelt | Accessibility-Review am benannten Gegenstand, manuelle und automatisierte Methoden, assistive Nutzung, Einschränkungen und Ersatzwege | Dokumentenreview des Fundaments; kein Audit einer implementierten V2-Oberfläche. |
| technisch verifiziert | Bestandene benannte Prüfungen am exakten Commit bzw. eindeutig gebundenen Arbeitsstand, Umgebung und Datum | LXF07-Bericht dokumentiert Fundamentprüfung; keine pauschale V2-Produkt- oder Realgerätefreigabe. |
| mit Nutzenden geprüft | Dokumentierter Walkthrough oder Usability-Test mit tatsächlichen Teilnehmenden, Aufgaben, Kontext, Befunden und Grenzen | Nicht erfolgt. KI-Perspektivwechsel ist kein Teilnehmernachweis. |
| unterrichtlich pilotiert | Tatsächlich durchgeführter Unterrichtspilot mit Lerngruppe, Kontext, Verfahren und ausgewerteten Ergebnissen | `not-started`; ein Protokoll oder synthetisches Beispiel zählt nicht als Durchführung. |
| lernwirksam | Belastbarer Wirkungsnachweis mit geeigneten Lernmaßen, methodisch begründetem Vergleich, Unsicherheit und Übertragungsgrenzen | Nicht vorhanden. Nutzung, Zustimmung, Designreview und Zufriedenheit reichen nicht. |

Die pauschalen Formulierungen „wissenschaftlich bewiesen“, „für alle geeignet“, „vollständig barrierefrei“ und „garantiert lernwirksam“ sind projektweit ausgeschlossen. Der Validator prüft die strukturierten Sperren; beliebige deutsche Prosa benötigt weiterhin redaktionellen Fachreview. Er behauptet keine vollständige automatische Spracherkennung.

Zulässige **interne Statusbeschreibung**: „Das V2-Lern-/Experience-Fundament ist nach dokumentiertem KI-Selbstreview und fachlicher Nutzerabnahme reviewed. Curriculare V2-Abdeckung bleibt unassessed; reale Nutzungsprüfung und Unterrichtspilot sind nicht erfolgt.“ Vor einer öffentlichen Verwendung sind genaue Formulierung, Gegenstand, Nachweise und Publikationsauftrag gesondert abzunehmen.

## Freigabegates und Beleggrenzen

1. **Dokumentenabnahme:** GOV-Selbstreview und Vertragsprüfungen abschließen, offene Fragen mit Eigentümer und Trigger dokumentieren; Jan nimmt dieses konkrete Paket ab.
2. **Übernahmeaudit:** Erst danach IUM-V2-AUD; keine V1-Aussage oder Lizenzentscheidung allein aufgrund ihres Alters als V2-Nachweis übernehmen. Anschließend R5 → R6 → R7 → DASH → CUT gemäß Re-Baseline.
3. **Konkrete Material-/Produktaussage:** Gegenstand, Version, Jahrgang, Wortlaut, Evidenz, Einschränkungen und Fachprüfende festhalten. Offene relevante Findings sperren die betroffene Aussage.
4. **Realer Einsatz:** Vor Nutzungsprüfung/Pilot konkrete Schule, Zuständigkeiten, Datenflüsse, Schutzmaßnahmen und Einsatzentscheidung klären. Ein Entwicklerauftrag öffnet dieses Gate nicht.
5. **Veröffentlichung/Betrieb:** Separater ausdrücklicher Auftrag, Betreiberentscheidung, geprüfte Rechte-/Datenschutz-/Accessibility-Hinweise, tatsächliches Auslieferungsartefakt und Rücknahmeplan. Push, Preview, Hosting, Veröffentlichung und Cutover sind unterschiedliche Handlungen.

Eine spätere Entscheidungsnotiz benötigt Gate-ID, Datum, Entscheider mit Rolle, exakten Commit und ggf. Artefakthash, betroffenen Gegenstand/Kanal, zulässigen Wortlaut, Beleg-IDs, Prüfer/Prüfart, Einschränkungen, offene Findings, Entscheidung und Recheck-Trigger. Leere Vorlagen und noch geplante Prüfungen sind kein Nachweis. Bei Änderungen wird der betroffene Claim auf gesperrt bzw. erneut zu prüfen gesetzt; ein alter Review wird nicht stillschweigend auf einen neuen Stand übertragen.

**Öffentlich geeignete Belege:** Rechtegeprüfte Projektdokumente, synthetische Fixtures, technische Prüfsummen und aggregierte Zusammenfassungen ohne Personenbezug. Die Eignung ist noch kein Veröffentlichungsauftrag. Ein öffentliches Git-Repository, CI-Artefakt oder Pages-Link ist kein interner Belegspeicher; `noindex` schafft keine Zugriffskontrolle.

**Geschützte Belege:** Reale Beobachtungsprotokolle, Lernprodukte, Exporte, Kontaktdaten, Einwilligungen, Audio/Video und personenbezogene Fehlerberichte bleiben außerhalb des öffentlichen Repositories, GitHub-Artefakten und dieser allgemeinen Planungsablage. Eine spätere zuständige Stelle legt einen zugriffsgeschützten Speicher, Zugangsrechte, Zweck, Löschfrist und zulässige veröffentlichte Zusammenfassung fest. Auch kleine Aggregate oder Freitext können identifizierbar sein. Die historische Mindestzahl zehn aus V1 ist keine Anonymitätsgarantie und wird nicht als V2-Rechtsregel übernommen.

## Datenschutz und geschützter Eigenbezug

Die V2-Projektgrenzen bleiben: keine persönliche Telemetrie, keine institutionelle Sammlung privater Reflexionen und keine realen Evidenzpakete im Repository. Lokale Lernstände und bewusst ausgelöste Exporte können trotzdem sensible Angaben enthalten. Geteilte Browserprofile, Gerätesynchronisation, Downloads, LMS und Hostingprotokolle sind eigene Datenflüsse, die vor Einsatz zu prüfen sind. Ein flüchtiger Modus ist keine pauschale Aussage über das gesamte Gerät oder den Hostingdienst.

Die [DSGVO](https://eur-lex.europa.eu/eli/reg/2016/679/oj?locale=de), insbesondere Artikel 5, 6, 13, 24, 25, 28, 32 und 35, begründet die Prüfung von Zweck, Rechtsgrundlage, Information, Verantwortung, Schutzmaßnahmen und gegebenenfalls Auftragsverarbeitung bzw. Folgenabschätzung. Welche Pflichten im konkreten Betrieb greifen, bleibt dessen verantwortlicher Stelle zugeordnet. Die [amtliche Schuldatenschutz-Seite BW](https://it.kultus-bw.de/,Lde/Datenschutz%2Ban%2BSchulen) bietet dafür aktuelle Rechtsgrundlagen und Umsetzungshinweise. Einwilligung wird nicht pauschal als Universallösung vorgeschrieben.

**CUR-Q-002 bleibt offen:** `LH26-E-DP-003` verlangt Reflexion eigener Mediennutzung. Persönliche Inhalte dürfen nicht als Abgabe, Beobachtungs- oder Bewertungsnachweis eingesammelt werden. Ein fiktiver Fall kann einen Schutzweg bieten; er belegt den curricularen Eigenbezug nicht. IUM-V2-CUR muss vor einem betroffenen Modul gemeinsam mit Datenschutz- und Fachdidaktikprüfung eine tragfähige Lösung dokumentieren. Bis dahin bleibt die entsprechende Abdeckung offen. GOV schließt den Zielkonflikt nicht durch Umbenennung.

## Lizenzierung und öffentliche Wahrnehmung

Der bestehende Lizenzrahmen trennt [eigenen Code unter MIT](../../../../LICENSE) und [eigene Inhalte unter CC BY-SA 4.0](../../../../LICENSE-CONTENT.md). Datei- und Assetangaben können abweichen; [Assetregister](../../../../apps/lernwerk-portal/public/asset-licenses.json) und [Abhängigkeitsregel](../../../../license-policy.json) sind getrennte Nachweise. Ein erfolgreicher Dependency-Check klärt keine Rechte an Bildern, Quellen oder Marken.

Der [CC-BY-SA-Lizenzvertrag](https://creativecommons.org/licenses/by-sa/4.0/legalcode.de) verlangt die einschlägigen Zuschreibungen, Lizenz- und Änderungsangaben und bei Bearbeitungen die passenden Weitergabebedingungen. Er verleiht nicht automatisch Persönlichkeits-, Datenschutz- oder Markenrechte. Fremde Forschung, amtliche Materialien und externe Lernspiele behalten ihren eigenen Nutzungsstatus; kostenlos zugänglich bedeutet nicht frei nachlizenzierbar. Ungeklärtes Drittmaterial wird nicht eingebettet oder kopiert. Links und eigene begrenzte Zusammenfassungen sind anhand des konkreten Materials zu prüfen.

Für jedes einzubindende Asset dokumentiert der Rechte-Review Herkunft/Version, Urheber bzw. Rechteinhaber, Lizenz oder Erlaubnis, Bearbeitung, erforderliche Hinweise und Auslieferungsort. Institutionelle Namen/Logos sowie Aussagen wie „offiziell empfohlen“ oder „vom Land zertifiziert“ benötigen eine belegte Berechtigung; curriculare Zuordnung und Quellenverlinkung sind dafür kein Nachweis.

## Accessibility und rechtliche Einordnung

Barrieren müssen am konkreten Produkt und Nutzungsweg geprüft werden. Die [WCAG 2.2, Abschnitte 5.2–5.3](https://www.w3.org/TR/WCAG22/#conformance-claims), unterscheiden Anforderungen an Konformität von freiwilligen Konformitätsaussagen mit benannter Version, Stufe, Datum, Seitenumfang und Technologien. Automatisierte Tests allein tragen keinen solchen Gesamtanspruch.

Die konkrete Anwendbarkeit gesetzlicher Pflichten, etwa des baden-württembergischen L-BGG bei einem öffentlichen Betreiber, wird vor Veröffentlichung geklärt (GOV-Q-OPERATOR). Die Landesrechtseiten lieferten bei dieser Prüfung keinen auslesbaren Normtext; deshalb wird hier keine aktuelle projektspezifische Rechtspflicht oder Ausnahme abschließend behauptet. „Barrierearm“ umgeht keine anwendbaren Pflichten. Eine spätere Erklärung muss tatsächliche Grenzen und Kontaktwege korrekt nennen.

## Recheck und offene Fragen

Der Vertrag benennt sechs Auslösergruppen: Recht/Betrieb, Quellen, Produkt/Umgebung, Rechte, Aussageumfang und Vorfälle. Bei unbesetzter Prüfrolle koordiniert Jan die Besetzung; bis zum Nachweis bleibt das betroffene Gate geschlossen. Es wird keine Hintergrundüberwachung eingerichtet. Die Prüfung erfolgt anlassbezogen und vor dem jeweiligen Freigabegate, mit Datum, Quelle, Version und Ergebnis.

Fünf offene Fragen stehen mit Eigentümer, Risiko, Trigger und gesperrtem Gate im Vertrag: Betreiber, Schule/Verarbeitung, konkrete Prüfende, CUR-Q-002 und Rechte/Marken. Sie verhindern keine dokumentarische GOV-Abnahme oder das anschließende Übernahmeaudit; ihre dort dokumentierte Weitergabe ist aber verpflichtend. Eine GOV-Abnahme schließt diese Fragen nicht stillschweigend.

## Validierung

`npm run verify:v2` prüft zuerst die vorhandenen V2-Verträge einschließlich des unveränderten LXF07-Prüfumfangs und danach Governance. Die Governance-Prüfung kontrolliert Pflichtdateien, geschlossene Datenformen, vollständige Rollen/Aussagearten, feste Mindestnachweise und Sperren, auflösbare Belege und SHA-256-Bindung der geprüften Eingänge (UTF-8, auf LF normalisierte Zeilenenden). Der Vertrag selbst und seine Lesefassung werden mitgebunden. Beabsichtigte Änderungen benötigen erneuten Review; bloßes Neuberechnen von Hashes ist keine Abnahme.
