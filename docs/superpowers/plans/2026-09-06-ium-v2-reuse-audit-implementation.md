# IUM-V2-AUD – Umsetzungsplan

Auftrag vom 2026-09-06: GOV freigegeben, Übernahmeaudit ausführen. Grundlage: freigegebene Re-Baseline-Spezifikation Abschnitt 12 und die gleichnamige Vault-Task-Notiz. Kontextstufe Kritisch; Inline-Ausführung im vorhandenen Feature-Branch `feat/ium-v2-rebaseline`, keine Subagenten. Sauberer Checkout, Fetch und Fast-forward-Pull vor Beginn geprüft.

- [x] GOV-Freigabe dokumentieren und AUD übernehmen.
- [x] IUM00–IUM20 und LXP01–LXP04 mit tatsächlichen Artefaktbelegen am versiegelten V1-Commit zuordnen; fehlende historische Task-Notizen als Einschränkung ausweisen.
- [x] Für jede der 25 Familien genau eine Entscheidung (`retain`, `adapt`, `replace`, `reference-only`, `drop`) mit präzisem Geltungsbereich, Begründung, V2-Anforderungen, fundamentspezifischen Evidenzen und konkreten Nachfolgetasks dokumentieren. Abgeschlossene Grundlagenarbeit von noch gesperrter Produktionsarbeit unterscheiden.
- [x] LXP05 am versiegelten Kandidatencommit als gesonderten Fehler-/Erfahrungsbestand auswerten; keine Übernahmeentscheidung oder Integration für diesen Branch.
- [x] Maschinenlesbares Inventar, begrenzte Nachfolgeaufträge, Schema, Auditbericht und Reviewstatus erstellen. GOV-Abnahme additiv und datiert erfassen; vorhandene LXF-/GOV-Review-Snapshots bleiben unverändert.
- [x] Negativtests zunächst rot ausführen; separaten Auditvalidator in `verify:v2` integrieren. Vollständigkeit, eindeutige Entscheidungen, reale Artefaktanker, Anforderungs-/Nachfolgereferenzen, LXP05-Trennung und unveränderte Freigabegrenzen prüfen.
- [x] Querschnittliche Gegenprüfung dokumentieren; fokussierte und gesamte Python-Regression, V2-Gate, Schema-Instanzen, Git-/Hash-/Linkprüfung ausführen. Produkt-/Builddateien bleiben unberührt; kein neuer Produktbuild erforderlich.
- [x] Reviewpaket für lokale Sicherung und Vault-Übergabe vorbereitet. Der anschließend ausgeführte Fetch/Pull, Commit, Pushstatus und finale Vault-Abgleich werden in der Session `2026-09-06 - Codex Session - IUM-V2-AUD Übernahmeaudit` dokumentiert.

Der Auditauftrag autorisiert die Bewertung und konkrete Planung der Nachfolgearbeit. Er autorisiert keine Umsetzung neuer Module oder Plattformänderungen. Nachfolger außerhalb der bestehenden R5/R6/R7/DASH/CUT-Folge werden nur als gesperrte, separat zu beauftragende Folgetasks dokumentiert; sie ändern die laufende Gatefolge nicht.

Prüfgrenze: Die Auditentscheidung ist ein begründeter Dokumentenreview, keine neue Quellenstudie, Echtgeräteprüfung, Unterrichtspilotierung oder Wirksamkeitsprüfung. Kein Gesamtfortschritt und keine Gesamtampel. R5 beginnt erst nach ausdrücklicher Auditabnahme.
