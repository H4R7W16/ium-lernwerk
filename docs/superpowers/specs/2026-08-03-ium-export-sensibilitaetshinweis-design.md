# IuM Phase 1 – Sensibilitätshinweis beim Export

**Status:** zur Schriftprüfung nach freigegebener Designentscheidung

**Datum:** 2026-08-03

## Ausgangslage

Der Plattformvertrag beschreibt den lokalen JSON-Export ausdrücklich als sensibel, weil Freitext oder Lernprodukte enthalten sein können. Die aktuelle Prüffassung bietet jedoch nur die Schaltfläche `Exportieren`; ein sichtbarer Sensibilitätshinweis fehlt. Download und Inhalt wurden am realen iPad erfolgreich geprüft, das Exportkriterium bleibt wegen dieses Produktdefekts offen.

## Ziel

Vor der Exporthandlung wird dauerhaft und ohne zusätzliche Interaktionshürde verständlich darauf hingewiesen, dass die erzeugte Datei sensible Inhalte enthalten kann und vor dem Teilen geprüft werden muss. Der Hinweis ist sichtbar, per Screenreader der Export-Schaltfläche zugeordnet und verändert den bestehenden Exportablauf nicht.

## Betrachtete Ansätze

1. **Dauerhaft sichtbarer Inline-Hinweis – gewählt.** Geringe Bedienlast, immer auffindbar und barrierefrei mit der Exportaktion verknüpfbar.
2. **Bestätigungsdialog vor jedem Export – verworfen.** Erzeugt wiederholte Reibung und Gewöhnungseffekte, obwohl keine zusätzliche Entscheidung oder Einstellung angeboten wird.
3. **Nur längere Schaltflächenbeschriftung oder Tooltip – verworfen.** Eine lange Beschriftung verschlechtert die Aktionsklarheit; Tooltips sind auf Touchgeräten und für assistive Technik kein verlässlicher alleiniger Informationskanal.

## Oberflächen- und Accessibility-Design

Direkt vor der Aktionsgruppe der technischen Systemprobe erscheint ein normaler Absatz mit der festen Formulierung:

> Exportdateien können Freitext oder Lernprodukte enthalten. Prüfe sie vor dem Teilen und veröffentliche sie nicht ungeprüft.

Der Absatz erhält eine stabile ID. Die Schaltfläche `Exportieren` referenziert diese ID über `aria-describedby`. Der Hinweis bleibt als Text sichtbar und wird nicht ausschließlich durch Farbe, Symbol, Tooltip oder versteckte Screenreader-Beschriftung vermittelt. Es erscheint kein zusätzlicher Dialog.

## Verhalten und Datenfluss

Die Änderung ergänzt ausschließlich statisches Markup und die semantische Beziehung zur vorhandenen Export-Schaltfläche. Serialisierung, Dateiname, lokaler Download, Copy-Fallback, Speicherung, Import, Fehlerbehandlung und Fokusführung bleiben unverändert. Es entstehen keine Konten, Serverdaten, Telemetrie, Drittanfragen oder neuen lokalen Zustände.

## Prüfung

Die Umsetzung erfolgt testgetrieben:

- Ein Komponententest fordert den exakten sichtbaren Hinweistext, eine eindeutige Hinweis-ID und die passende `aria-describedby`-Referenz der Export-Schaltfläche.
- Der bestehende Browsertest bestätigt weiterhin Download, Dateiname und verlustfreien Inhalt; zusätzlich darf vor dem Export kein Dialog entstehen.
- Die vollständigen Phase-1-, Browser-, Offline- und Accessibility-Prüfungen müssen unverändert grün bleiben.
- Nach Veröffentlichung wird auf dem verwalteten iPad geprüft, dass der Hinweis sichtbar ist, mit VoiceOver beim Export verständlich angesagt wird und der Download weiterhin funktioniert.

## Akzeptanzkriterien

- Der festgelegte Hinweis steht sichtbar unmittelbar beim Exportbereich.
- `Exportieren` ist programmatisch genau mit diesem Hinweis beschrieben.
- Der Export bleibt eine direkte, bewusst ausgelöste Handlung ohne vorgeschalteten Dialog.
- Download, Dateiname und JSON-Inhalt bleiben unverändert.
- Automatisierte Prüfungen und der reale iPad-Nachtest bestehen.
- Erst danach darf das Exportkriterium im Geräteprotokoll geschlossen werden.

## Nicht im Umfang

Nicht Bestandteil dieser Korrektur sind Verschlüsselung, Kennwortschutz, automatische Inhaltsanalyse, neue Dateiverwaltung, Freigabesperren, MDM-Änderungen oder eine allgemeine Neugestaltung der Aktionsgruppe.
