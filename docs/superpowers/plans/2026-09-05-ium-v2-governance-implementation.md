# IUM-V2-GOV – Umsetzungsplan

Stand: 2026-09-05. Auftrag: LXF07 fachlich freigegeben; IUM-V2-GOV ausführen. Grundlage: freigegebene Re-Baseline-Spezifikation, Abschnitt 11, und gleichnamige Vault-Task-Notiz. Dies konkretisiert den bestehenden Auftrag ohne neue Produktentscheidung.

Ausführung: sequenziell durch Codex im bestehenden Branch `feat/ium-v2-rebaseline`; keine Subagenten. `git status`, Fetch und Fast-forward-Pull sind vor Arbeitsbeginn geprüft. Kontextstufe Kritisch.

- [x] LXF07-Freigabe dokumentieren und GOV operativ übernehmen.
- [x] Tatsächlichen Repo-/Vault-Bestand zu Aussagen, Rollen, Datenschutz, Lizenzierung und Publikation inventarisieren; aktuelle amtliche Primärquellen prüfen.
- [x] Governance-Lesefassung sowie maschinenlesbaren Vertrag und getrennten Fundamentstatus erstellen. Sieben Aussagearten, zuständige Prüfrollen, Entscheidungsrechte, konkrete aktuelle Nachweise, Sperren und Recheck-Trigger verbinden. Institutionelle Rollen bleiben bis zur Benennung offen.
- [x] Negativtests zunächst rot ausführen: schwächerer Evidenztyp, vorgezogene Nutzungs-/Pilot-/Wirksamkeitsbehauptung, offene Publikation, unbesetzte Betriebsrollen, veraltete oder fehlende Referenzen, fehlerhafte Datentypen. Danach kleinen separaten Validator in `verify:v2` integrieren.
- [x] Dokumentenselbstreview mit konkreten Gegenfällen durchführen; V2-Gate, fokussierte und gesamte Python-Regression, Schema-Instanzprüfung sowie Diff-/Referenzprüfung ausführen. Kein erneuter Produktbuild nötig, solange Produkt, Abhängigkeiten und Buildpfade unverändert bleiben.
- [x] Plan und Reviewbericht für lokalen Commit abschließen; Fetch/Pull unmittelbar vor Commit und operative Vault-Übergabe werden im Session-Handoff mit Commit-Hash dokumentiert.

Schreibumfang: neue `roadmap/v2/foundations/governance/`-Dateien, Governance-Schema, separater Python-Validator und Tests, minimaler Aufruf im V2-Validator, dieser Plan und operative Vault-Notizen. Das mit 35 Hashes gebundene LXF07-Review bleibt unverändert; neue Governance-Eingänge werden erst nach dessen Prüfung validiert und verändern seinen historischen Prüfumfang nicht.

Abschluss: GOV erhält einen geprüften Dokumentenstand zur Nutzerabnahme. AUD beginnt erst nach dieser Abnahme. V1, LXP05, Inhaltsproduktion, Pilot-, Publikations- und Cutover-Sperren bleiben entsprechend dem bestehenden Auftrag erhalten. Rechtliche Anwendung am konkreten Betreiber/Einsatz ist ein späteres Gate, kein behauptetes Ergebnis dieser Dokumentenprüfung.
