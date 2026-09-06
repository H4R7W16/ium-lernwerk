# IUM-V2-CUT – Implementation Plan

> Ausführung inline mit `superpowers:executing-plans`: gemeinsame Status- und Nachweisdateien, keine autorisierte parallele Agentenarbeit.

**Ziel:** Einen vollständigen, überprüfbaren Cutover-Bericht gemäß bestehendem Task und V2-Spezifikation liefern. Die konkrete Nutzerentscheidung über den aktiven Stand bleibt ausstehend; die DASH-Freigabe autorisiert die Ausführung des CUT-Tasks, nicht die noch nicht vorgelegte Auswahlentscheidung.

**Architektur:** Neue, additive Dokumente unter `roadmap/v2/cutover/` binden die 17 Vorgängergates an tatsächlich vorhandene Git-Commits und ausgewählte historische Artefaktdigests. Ein separater aktueller Inputvertrag schützt die Entscheidungsvorlage vor unbemerkter Änderung ihrer Grundlagen. Versiegelte frühere Status-/Roadmap-Dateien werden nicht umgeschrieben. Ein eigener Validator prüft CUT zusätzlich zum vorhandenen V2-Gate. Das Dashboard zeigt den CUT-Review und die neue Berichtsevidenz, während der aktive Status unverändert V1/building bleibt.

- [x] DASH-Freigabe als Acceptance und im Vault dokumentieren; CUT übernehmen, sauberen isolierten Branch prüfen.
- [x] 17 Freigaben und Git-Artefakte auditieren; LXF05-/SRC-Nutzerfreigabe bei Bedarf aus Initiative und Entscheidungsnotizen ergänzend belegen.
- [x] Aktuelle Kriterienmatrix für acht Projektanforderungen, vier Grundlagen, 25 Auditfamilien, drei Jahrgänge und Dashboard erstellen.
- [x] Offene Grundlagen-, Kapazitäts-, Eigenbezugs-, Reflexions-, Technik-, Nutzungs- und Pilotbedingungen mit Eigentümer, Risiko, Auslöser und Nachweis weiterführen. Planerisch erfüllte Teilbedingungen separat vom historischen Snapshot ausweisen.
- [x] Drei konkrete Optionen vorbereiten: V2 als Planungs-/Entwicklungsbaseline annehmen, Entscheidung vertagen, Paket zurückweisen. Keine Option öffnet Produktion, LXP05, Push, Merge, Hosting, Veröffentlichung oder Pilotierung.
- [x] CUT-Vertrag und Negativtests zuerst schreiben; fehlende/gefälschte Gatebelege, veränderte Kandidatengrundlage, unbekannte Status, übersprungene Nutzerentscheidung und verlorene offene Bedingungen müssen scheitern.
- [x] Dashboard für CUT-in-progress/review nach belegter DASH-Abnahme öffnen; Bericht und Statusregister aktualisieren. Vorhandene lokale Vorschau nicht unterbrechen; eigener Port für Tests und CUT-Vorschau.
- [x] V2/CUT-Validator, Dashboardtests, Browser-/Accessibility-/Druckgate, vollständige Python- und Plattformregression sowie Typecheck, Astro-Check und das IUM5-Verifikationsgate als 24-Schritte-Obermenge der 19 Phase-1-Prüfschritte prüfen. Resultate als tatsächliche aktuelle Prüfläufe dokumentieren.
- [ ] Bericht und konkrete Entscheidungsnotiz fertigstellen, lokalen Commit nach Fetch/Pull sichern und Dashboard aus sauberem Commit regenerieren.
- [ ] CUT in Review übergeben; Task, Initiative, Kanban, Roadmap, Projekt, Session und Entwicklungshistorie synchronisieren. Konkrete Entscheidung über die empfohlene Option erst danach vorlegen.

## Vorläufiger technischer Befund

`roadmap/v2/status.json` ist Teil mehrerer unveränderlicher Inputbindungen; die bisherigen Validatoren und Dashboardgrenzen verlangen bewusst V1/building. Ein direktes Umetikettieren auf V2 würde historische Nachweise beschädigen. Der Bericht muss deshalb eine additive, ausdrücklich genehmigte Aktivierung mit eigenem aktuellen Baseline-Zeiger und historischen Referenzen beschreiben. Das ist eine getrennte Folge der konkreten Cutover-Entscheidung, keine implizite Änderung durch Erstellung des Berichts. Keine Aktivierungsdatei wird in dieser Vorbereitung als angenommen ausgegeben.

## Verifikation und Handoff

30 CUT- und 30 Dashboardtests, sechs Dashboard-Browsergates sowie IUM5 24/24 (996 Python-/132 Plattformtests) bestanden. Details und Umgebungsbefund im CUT-Prüfbericht. Die beiden letzten Schritte werden nach dem lokalen Commit im Session-Handoff belegt; kein selbstreferenzieller Commit-Hash im Repo-Plan.
