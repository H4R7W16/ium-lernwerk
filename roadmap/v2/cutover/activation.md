# V2 als Planungs- und Entwicklungsbaseline aktiv

Am 6. September 2026 ausdrücklich freigegeben: **„V2-Aktivierung freigegeben.“** Angenommener CUT-Commit: `0032509af1dfe758548f34f37bb633bae403a9fa`.

V2 ist die aktive Planungs-/Entwicklungsbaseline für die weitere Arbeit. V1 bleibt bestehender Produktstand und unveränderliche Archivreferenz. Die ursprüngliche 18er-Gatefolge ist nach erfolgreicher technischer Umsetzung abgeschlossen. Das ist keine Behauptung eines fertigen V2-Lernprodukts.

[decision.json](decision.json) bindet die Auswahl an den angenommenen CUT-Bericht und alle 46 Bedingungseinträge. Zwei Planungsbedingungen erfüllt, 41 offen, drei Folgeaufträge gesperrt. Neun unterschiedliche Nachweisfragen, lokale Kapazität und tatsächliches Vorwissen bleiben offen. Keine zusätzliche Reife- oder Coverage-Anhebung.

[active-baseline.json](active-baseline.json) ist der aktuelle entscheidungsgebundene Baseline-Zeiger. Geschützte fachliche Inputs müssen weiterhin mit dem freigegebenen CUT-Stand übereinstimmen. Nur ausdrücklich aufgeführte Statusleser und Tests werden im Aktivierungsschritt migriert. Ihre aktuellen Digests und die neuen Aktivierungsdateien sind separat gebunden.

Der unveränderte [CUT-Bericht](README.md) und [review.json](review.json) dokumentieren den historischen Entscheidungsstand **vor** dieser Annahme. Ihre Formulierung „Entscheidung ausstehend“ ist kein aktueller Status. Ebenso bleibt `roadmap/v2/status.json` der versiegelte historische V1/building-Snapshot. Aktuelle Werkzeuge lesen den neuen Zeiger über `scripts/validate_v2_activation.py`; die historischen Validatoren prüfen weiterhin die damaligen Grundlagen.

## Grenzen und nächste Arbeit

Inhaltsproduktion, LXP05-Integration, Unterrichtspilot, Hosting, Veröffentlichung, Push und Merge bleiben geschlossen. FU-TECH, FU-MOD und FU-PILOT benötigen ihre eigenen Aufträge und Abhängigkeiten. Als nächster Auftrag bietet sich FU-TECH zur Prüfung vorhandener technischer Bausteine gegen V2 an; er wurde nicht begonnen.

## Prüfung und Reproduktion

- `npm run verify:v2:cutover`: bestehendes V2-Gate plus aktuelle entscheidungsgebundene Aktivierung; bei fehlendem/ungültigem Beleg kein stiller Rückfall auf V1.
- `python -B scripts/validate_v2_activation.py --vault <Vault-Verzeichnis>`: aktive Baseline, geschützte Inputs, tatsächliche Freigaben und Bedingungen prüfen.
- `python -B scripts/validate_v2_cutover.py --historical-review --require-verified`: damaligen CUT-Prüfstand aus dem angenommenen Git-Commit lesen.
- Vollständige Pythonregression und aktuelle Dashboard-/Browsergates werden im Aktivierungs-Handoff dokumentiert. Technische Tests ersetzen keine Lern- oder Nutzungsbewährung.

Der Aktivierungscommit und die tatsächlichen Prüfergebnisse stehen im Session-Handoff; kein selbstreferenzieller zukünftiger Commit-Hash in diesem Dokument.
