# IUM-V2-GOV – Dokumentenreview

Stand: 2026-09-05. Ausgangscommit: `d11a8bc69775525ec0162516275bb39f5dc9c441`. Prüfer und Autor: Codex. Prüfart: KI-gestützter Dokumentenselbstreview, keine unabhängige menschliche oder institutionelle Prüfung. Die LXF07-Nutzerfreigabe ist separat im Status festgehalten; die GOV-Nutzerabnahme steht aus.

## Prüfumfang und Ergebnis

Der Vertrag umfasst sieben Aussagearten, 13 Rollen, sechs Recheck-Gruppen, fünf offene Folgefragen und vier am Original bzw. amtlichen Portal geprüfte Quellen. Inventar und Lesefassung behandeln die im aktuellen Repo-/Vault-Bestand gefundenen Governance-Regelgruppen. Es fand keine Liveprüfung eines produktiven Internetauftritts oder tatsächlichen Schulbetriebs statt.

| Akzeptanzkriterium | Dokumentenbefund | Grenze |
| --- | --- | --- |
| Öffentliche Aussagen nicht aus schwächerer Evidenz ableiten | Jede Aussageart besitzt einen festen Mindestnachweis, Prüfrolle, konkrete Bestandsbelege und aktuelle Sperre. | Neue öffentliche Formulierungen benötigen redaktionellen Review und gesonderten Auftrag. |
| Pauschale Wirkung und Barrierefreiheit ausschließen | Vier verbotene Pauschalaussagen im Vertrag; WCAG-Aussageumfang und fehlender Wirkungsnachweis ausdrücklich beschrieben. | Keine automatische semantische Prüfung beliebiger Prosa. |
| Rollen und Freigabegates eindeutig | Projektabnahme, Fachprüfungen, institutionelle Betriebsentscheidung und Schuleinsatz getrennt. Unbesetzte spätere Rollen offen ausgewiesen. | Keine Institution oder menschliche Fachprüfung erfunden. |
| Lizenzen, Datenschutz und Publikation konsistent | MIT/CC-BY-SA/Assetausnahmen und Drittmaterial getrennt; reale Daten außerhalb öffentlicher Ablagen; technische Architektur nicht als Rechtsfreigabe behandelt. | Betreiber-/Schulprüfung und konkrete Rechteketten bleiben vor Einsatz erforderlich. |

## Konkrete Gegenfälle

1. **„Mit Nutzenden geprüft, weil drei Walkthroughs bestanden sind“:** zurückgewiesen. LXF07 enthält KI-Dokumentenwalkthroughs, keine tatsächlichen Teilnehmenden. `usage` bleibt `not-established`.
2. **„V2 ist curricular vollständig, weil die Curriculumgrundlage reviewed ist“:** zurückgewiesen. V2-Coverage ist unassessed; ein Fundamentreview ersetzt kein Materialmapping.
3. **„Lernwirksam, weil LXF02 geprüfte Forschung enthält“:** zurückgewiesen. Forschungsbefunde tragen begrenzte Designentscheidungen; der eigene Produkt-Wirkungsnachweis fehlt.
4. **„Vollständig barrierefrei, weil automatische Tests grün sind“:** zurückgewiesen. Dokumenten-, Automatik-, Assistenztechnik- und Realgeräteprüfung bleiben getrennt; pauschale Formulierung verboten.
5. **„Jan ist automatisch Betreiber und schulisch Verantwortlicher“:** zurückgewiesen. Belegt ist die Auftraggeberrolle; konkrete institutionelle Zuständigkeit bleibt unbesetzt.
6. **„Keine personenbezogenen Daten, weil Local-First“:** zurückgewiesen. Exporte, Browserprofile, Hosting und LMS benötigen eigene Betrachtung.
7. **„Privater Medienbezug ist durch einen erfundenen Fall erledigt“:** zurückgewiesen. CUR-Q-002 bleibt offen; kein fingierter Eigenbezug.
8. **„Alle Inhalte sind MIT bzw. frei, weil das Repo offen ist“:** zurückgewiesen. Inhaltelizenzen, Assetausnahmen und Drittmaterialrechte separat prüfen.
9. **„Noindex macht reale Pilotbelege intern“:** zurückgewiesen. Ein öffentlicher Previewlink schafft keine Zugriffskontrolle; reale Pakete bleiben außerhalb des Repositories.

## Technische Verifikation

Frisch bestanden: 21 Governance-Tests und 167 bestehende V2-Tests (zusammen 188), die gesamte Python-Regression mit 863 Tests, `npm run verify:v2`, beide Instanzen gegen das Governance-Schema mit AJV 2020 sowie `git diff --check`. Die neuen Negativtests wurden zunächst mit fehlendem Validator rot ausgeführt. Drei alte Testfixtures wurden um die jetzt verpflichtenden Governance-Dateien ergänzt; ihre Aussage zu optionalen historischen Quellen bleibt erhalten.

LXF07-Eingangsmenge bleibt genau 35 Dateien; Governance bindet 25 eigene Prüfeingänge getrennt. Sämtliche Governance-Referenzen sind lokale Dokumentenbelege oder registrierte Primärquellen, keine realen personenbezogenen Evidenzpakete. Technische Prüfungen betreffen Dokumenten- und Datenverträge. Produktcode, Buildpfade, Abhängigkeiten und V1-Artefakte wurden nicht verändert; Plattform-, Browser- und Realgerätetests wurden für dieses Paket nicht neu ausgeführt. Frühere LXF07-Produktprüfungen sind historischer Nachweis und werden hier nicht als neue Testläufe ausgegeben.

## Offene Fragen und Übergabe

GOV-Q-OPERATOR, GOV-Q-SCHOOL, GOV-Q-REVIEWERS, CUR-Q-002 und GOV-Q-RIGHTS bleiben mit Verantwortungsrolle, Risiko, Trigger und betroffenen Gates offen. Ihre Weitergabe an AUD und spätere Tasks ist Bestandteil des reviewten Vertrags. Die konkrete Gesetzesanwendung wurde nicht abschließend geprüft; zwei Landesrecht-BW-Seiten waren nicht auslesbar und werden nicht als primär gelesene Normnachweise ausgegeben.

Dokumentarischer Befund: `concept: reviewed`, operativer Task `review`, GOV-Nutzerabnahme `pending`. Inhalt `frozen`, Pilot `not-started`, Veröffentlichung `closed`. IUM-V2-AUD folgt ausschließlich nach expliziter GOV-Nutzerabnahme. Der finale lokale Commit wird im Vault-Handoff festgehalten; dieser Bericht bindet den Ausgangscommit und den via Status gehashten tatsächlich geprüften Dateistand, ohne einen selbstreferenziellen Commit-Hash vorzutäuschen.
