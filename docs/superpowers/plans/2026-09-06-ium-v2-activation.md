# Freigegebene V2-Aktivierung

Freigabe: „V2-Aktivierung freigegeben.“ Bezogen auf CUT `0032509af1dfe758548f34f37bb633bae403a9fa`, Option `accept-planning-baseline`. Ausführung mit executing-plans auf dem vorhandenen isolierten Featurebranch. Keine erneute Freigabefrage.

- [x] Sauberen Branch und alle CUT-Dateibindungen vor Änderung erneut prüfen.
- [x] Entscheidung mit den 46 fortgeführten Bedingungen und allen Einsatzgrenzen separat dokumentieren.
- [x] Additiven aktuellen Baseline-Zeiger und strikte Aktivierungsprüfung erstellen. Geschützte fachliche Inputs bleiben identisch; nur benannte Statusleser und Tests werden migriert.
- [x] Historisches CUT-Review aus dem angenommenen Git-Commit prüfen; seine damaligen Felder und Freigaben nicht rückwirkend ändern.
- [x] Dashboard, Markdownprojektion und bestehendes CUT-Kommando auf die aktuelle Entscheidung umstellen; alle 18 Gates nach erfolgreicher Aktivierung abgeschlossen.
- [x] Annahme, Vertagung, Nacharbeit, fehlende Entscheidung und Drift mit Tests prüfen; Pythonregression, V2-/Aktivierungsgate und Dashboard-/Browsergates ausführen.
Abschlusscheckpoint: Lokalen Commit nach erfolgreichem Fetch/Pull sichern; Task/Initiative und Ansichten abschließen. Der tatsächliche Commit und der ausgeführte Vault-Handoff werden außerhalb dieses Commits in `2026-09-06 - Codex Session - V2-Aktivierung` dokumentiert.

V2 wird ausschließlich aktive Planungs-/Entwicklungsbaseline. V1 bleibt bestehender Produktstand und Archiv. Produktion, LXP05, Pilot, Publikation, Push/Merge bleiben geschlossen. Die drei FU-Aufträge bleiben gesperrt und werden nicht übernommen.

Das gerade vollständig bestandene IUM5-24-Schritte-Gate wird als historischer Produktnachweis erhalten. Aktivierung ändert keine Lernplattformdateien oder Abhängigkeiten; neue Prüfungen konzentrieren sich auf Status, Nachweise und Darstellungen plus gesamte Pythonregression.

Verifikation: 1.017 Python-Tests (einschließlich 21 Aktivierungs- und 30 historischen CUT-Tests), 32 Dashboardtests und sechs Browserprüfungen bestanden. V2-/CUT-Aktivierungsprüfung erfolgreich. Alle drei Seiten des Gate-Drucks und die Desktopansicht visuell geprüft.
