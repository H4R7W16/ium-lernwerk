# IUM11-Rettungsdesign für die Publikationsgrenze

**Status:** Entwurf zur schriftlichen Freigabe

**Datum:** 2026-08-02

**Scope:** Rückbau der überdehnten CommonMark-/HTML-Prüfung in IUM11-Implementierungstask 8

## 1. Ausgangslage

Der freigegebene IUM11-Architekturreset hat die ungeeignete semantische Klassifikation freier deutscher Prosa durch einen deterministischen Publikationsvertrag ersetzt. Dieser Kern ist tragfähig: Ein Vertragsobjekt wird aus den kanonischen Quellen kompiliert, als JSON serialisiert und als byteidentischer Faktenblock in README, Lehrkräfteanleitung und Reviewanleitung veröffentlicht.

Bei der anschließenden Prüfung wurde die automatisierte Textgrenze jedoch schrittweise zu einem eigenen partiellen CommonMark-/HTML-Parser erweitert. Er versucht inzwischen, unter anderem Fenced Code, eingerückten Code, Listenfortsetzungen, Setext-Überschriften, HTML-Kommentare und rohe HTML-Container semantisch zu unterscheiden. Wiederholte Ausnahmerunden haben gezeigt, dass diese Eigenimplementierung die Blockcontainer-Regeln von CommonMark nicht verlässlich abbildet. Neue lokale Korrekturen erzeugten jeweils neue Fehlklassifikationen.

Das Problem liegt nicht im generierten Publikationsvertrag, sondern in einer zu weit behaupteten automatischen Garantie: Aus den Bytes beliebiger Markdown-Dokumente sollte ohne vollständigen Parser abgeleitet werden, welche Inhalte gerendert sichtbar sind. Diese Garantie wird zurückgenommen.

## 2. Ziel und ehrliche Garantiegrenze

Task 8 wird auf einen kleinen, deterministischen und prüfbaren Vertrag zurückgeführt:

1. **Automatisiert garantiert** werden die kanonischen Quelldaten, das geschlossene Vertragsobjekt, die deterministische Serialisierung, byteidentische Faktenblöcke, eine exakt festgelegte Dokumentstruktur sowie das Fehlen reservierter maschinenlesbarer Zweitdeklarationen in den festgelegten Bytebereichen.
2. **Redaktionell abgesichert** wird die korrekte sichtbare Darstellung im GitHub-kompatiblen Renderer. Sie wird vor der Abnahme anhand einer expliziten Review-Checkliste geprüft und nicht mehr durch einen selbst gebauten CommonMark-/HTML-Parser behauptet.

Damit bleibt die maschinelle Prüfung dort fail-closed, wo sie vollständig spezifiziert werden kann. Markdown-Sichtbarkeit und freie Prosa bleiben ausdrücklich Gegenstand des Reviews.

## 3. Nichtziele

Das Rettungsdesign:

- verändert weder Inhalte noch Werte von `pilot/pilot-protocol.json`, `roadmap/time-model.json` oder `pilot/docs/publication-contract.json`;
- verändert keine Produkt-, Verfügbarkeits-, Zeit-, Pilot-, Privacy- oder Coverageachse;
- führt keinen externen CommonMark- oder HTML-Parser ein;
- entwickelt keinen eigenen vollständigen oder partiellen Markdown-Renderer;
- bewertet keine Grammatik, Negation oder semantische Aussage freier Prosa;
- startet keine reale Pilotierung, Statushochsetzung, Veröffentlichung, Phase 1 oder Lernmaterialproduktion;
- gestaltet Lehrkräfte- oder Reviewanleitung inhaltlich nicht neu;
- verändert keine früheren Commits und schreibt keine Git-Historie um.

## 4. Unverändert erhaltener Kern

Folgende Teile des Architekturresets bleiben verbindlich:

- `compile_publication_contract(...)` und die geschlossene Vertragsstruktur;
- die bisherigen kanonischen Quellen und Governancekonstanten;
- `pilot/docs/publication-contract.json` als generiertes Artefakt;
- UTF-8 ohne BOM, LF-Zeilenenden, sortierte JSON-Schlüssel, Zwei-Leerzeichen-Einrückung und genau ein finaler Zeilenumbruch;
- der deterministisch gerenderte Markdown-Faktenblock;
- der byteidentische Faktenblock in `README.md`, `pilot/docs/teacher-guide.md` und `pilot/docs/review-guide.md`;
- Build, `--check`, vollständige Vorvalidierung und atomare Einzeldateiersetzung;
- Dateikarte, Privacygrenzen, Statusgrenzen und die Schwellen der Klassenbänder;
- die reservierten lexikalischen Formen für SemVer, Empfehlungscode, die sechs Urteilachsen, gesperrte Vertragswerte, Variantenkennung und numerische Kerndeklarationen;
- die Aussage, dass flexible Vertiefungs-, Transfer- und Projektmodule sichtbar erhalten bleiben und keine fehlende Kernzeit oder gescheiterte Kernintegration ersetzen.

Eine kleine Unicode-bewusste Prüfung von Bezeichnergrenzen darf erhalten bleiben. Sie klassifiziert nur einzelne reservierte Token und ist kein Markdown- oder Sprachparser.

## 5. Kanonisches Dokumentprofil

Die drei Veröffentlichungen sind source-controlled Dokumente mit einer bewusst engen Byte-Struktur. Der Build darf fehlende Strukturanker nicht stillschweigend erzeugen oder erraten. Bei fehlenden, doppelten, vertauschten oder falsch platzierten Ankern scheitert er vor dem ersten Schreibvorgang.

### 5.1 README

`README.md` enthält genau einmal die Zeile:

```markdown
## IUM11-Pilotinstrument
```

Unmittelbar danach folgen genau eine Leerzeile und der generierte Faktenblock. Der erwartete Präfix des Abschnitts lautet damit bytegenau:

```text
## IUM11-Pilotinstrument\n\n<GENERIERTER-FAKTENBLOCK>
```

Nach der handgepflegten IUM11-Prosa steht genau einmal und am Zeilenanfang der neue Endanker:

```markdown
<!-- IUM11-PUBLICATION-SCOPE:END -->
```

Auf den Endanker folgen genau eine Leerzeile und die bereits vorhandene Überschrift:

```text
<!-- IUM11-PUBLICATION-SCOPE:END -->\n\n## Zentrale Einstiege
```

Der lexikalische README-Prüfbereich beginnt unmittelbar nach dem Endmarker des generierten Faktenblocks und endet unmittelbar vor dem Endanker. Der übrige README-Text wird nicht als IUM11-Publikationsprosa geprüft. Die Bereichsbestimmung sucht keine „nächste sichtbare H2“ und interpretiert weder Markdown noch HTML.

### 5.2 Lehrkräfteanleitung

`pilot/docs/teacher-guide.md` beginnt bei Byte 0 exakt mit:

```text
# Lehrkräfteanleitung zum IUM11-Pilotinstrument\n\n<GENERIERTER-FAKTENBLOCK>
```

### 5.3 Reviewanleitung

`pilot/docs/review-guide.md` beginnt bei Byte 0 exakt mit:

```text
# Reviewanleitung zum IUM11-Pilotinstrument\n\n<GENERIERTER-FAKTENBLOCK>
```

In beiden Anleitungen umfasst der lexikalische Prüfbereich den gesamten Text außerhalb des exakten generierten Faktenblocks. Es wird nicht geprüft, ob weitere Zeichenfolgen als „sichtbare H1“ interpretiert würden; geprüft wird ausschließlich der bytegenaue kanonische Präfix.

## 6. Automatisierte Textgrenze

Die Strukturprüfung arbeitet auf den UTF-8-/LF-Bytes der Dateien. Die lexikalische Prüfung dekodiert den Inhalt als UTF-8 und untersucht ausschließlich die durch diese exakten Strukturanker begrenzten Zeichenbereiche. Sie maskiert keine Fences, eingerückten Codeblöcke, Listen, Kommentare oder HTML-Container.

Außerhalb des generierten Faktenblocks bleiben die bereits freigegebenen reservierten maschinenlesbaren Formen verboten:

- SemVer-Zeichenfolgen;
- Empfehlungscodes mit `eligible-for-`;
- Zuweisungen zu `status`, `availabilityStatus`, `timeFeasibilityStatus`, `sequenceEvidenceStatus`, `pilotStatus` oder `semanticCoverageStatus`;
- die reservierten englischen Vertragswerte;
- die technische Variantenkennung;
- die festgelegten numerischen Kerndeklarationen.

Diese Prüfung verhindert eine zweite maschinenlesbare Vertragsquelle. Sie behauptet weder Sichtbarkeit noch Unsichtbarkeit und macht keine Ausnahme aufgrund vermuteter Markdown- oder HTML-Semantik. Enthält ein Codebeispiel oder Kommentar im Prüfbereich eine reservierte Form, muss es umformuliert oder außerhalb dieses bewusst engen Publikationsbereichs platziert werden.

## 7. Redaktionelle Sichtbarkeitsprüfung

Die Reviewanleitung erhält eine verbindliche Checkliste. Vor Task-8-Abnahme werden alle drei Dokumente in einem GitHub-kompatiblen Renderer geprüft:

1. Die vorgesehene Abschnitts- beziehungsweise Dokumentüberschrift ist sichtbar.
2. Die gesamte generierte Tabelle ist sichtbar und weder als Code noch als Kommentar oder versteckter HTML-Inhalt gerendert.
3. Faktenblock, erläuternde Prosa und Links erscheinen in der vorgesehenen Reihenfolge.
4. Die Aussagen der Prosa widersprechen dem Faktenblock nicht.
5. Der Satz zu den flexiblen Vertiefungs-, Transfer- und Projektmodulen bleibt sichtbar erhalten.

Das Ergebnis wird im Task-8-Review dokumentiert. Diese redaktionelle Prüfung ist eine bewusste menschliche Qualitätsgrenze und keine behauptete Parserfunktion.

## 8. Rückbau

Aus `scripts/ium11_publication.py` werden der `HTMLParser`-Import und die vollständige selbst gebaute Markdown-/HTML-Sichtbarkeitslogik entfernt. Dazu gehören insbesondere:

- Fence- und Indented-Code-Bereichserkennung;
- Maskierungs- und Positionslogik für vermutete Markdownbereiche;
- HTML-Kommentar- und Raw-HTML-Containerparser;
- ATX-, Setext-, Thematic-Break- und „sichtbare Überschrift“-Scanner;
- die Suche nach dem README-Bereich über eine semantisch interpretierte nächste Überschrift.

Die Bereichsbestimmung wird durch kleine Funktionen für die exakten Anker, ihre Anzahl, Reihenfolge und Position ersetzt. Es verbleibt kein Code, der eine CommonMark- oder HTML-Blockstruktur modelliert.

Die adversarial Tests, deren einziger Vertragszweck die Interpretation beliebiger CommonMark-/HTML-Konstrukte ist, werden entfernt. Das ist kein Verlust einer weiterhin behaupteten Garantie, sondern die testseitige Umsetzung der engeren und ehrlichen Systemgrenze.

## 9. Fehlerverhalten

Automatisch fail-closed bleiben:

- fehlende, doppelte, verschachtelte oder vertauschte Faktenblockmarker;
- ein fehlender, doppelter oder falsch platzierter README-Endanker;
- eine abweichende README-Abschnittsüberschrift oder ein nicht unmittelbar folgender Faktenblock;
- ein abweichender Guide-H1-Präfix oder ein nicht unmittelbar folgender Faktenblock;
- ein nicht byteidentischer Faktenblock oder ein abweichendes JSON-Artefakt;
- eine reservierte maschinenlesbare Form im festgelegten lexikalischen Prüfbereich;
- Quellen-, Vertrags-, Fingerprint-, Dateikarten-, Privacy- oder Statusdrift;
- ein Schreibfehler oder ein durch `--check` erkannter gemischter Artefaktstand.

Nicht automatisch bewertet werden:

- die CommonMark-Bedeutung von Fences, Einrückung, Listen oder Setext;
- die HTML-Bedeutung von Kommentaren, Tags oder Containern;
- die tatsächliche Sichtbarkeit beliebiger handgepflegter Markdown-Konstrukte;
- semantische Widersprüche in freier deutscher Prosa.

## 10. Teststrategie

### 10.1 Erhaltene Tests

- Vertragscompiler, Feldmengen, Ableitungen und Eingabeunveränderlichkeit;
- deterministische JSON- und Markdown-Serialisierung;
- byteidentische Artefakte in allen drei Veröffentlichungen;
- Build-Idempotenz, `--check`, Read-only-Verhalten und atomare Ersetzung;
- Markerzahl, Markerreihenfolge, Dateikarte, Quellenbindung, Privacy und Status;
- alle reservierten lexikalischen Formen einschließlich Unicode-Bezeichnergrenzen;
- Schwellen und Klassenbänder der Lehrkräfteanleitung;
- vollständige IUM11-, IUM10-, IUM09- und Phase-0-Regression.

### 10.2 Neue oder angepasste Tests

- exakter README-Präfix aus H2, Leerzeile und Faktenblock;
- genau ein README-Endanker in korrekter Reihenfolge;
- exakte Nachbarschaft von Endanker und `## Zentrale Einstiege`;
- exakter Byte-0-Präfix beider Guides;
- Fehlschlag bei fehlenden, doppelten, vertauschten oder verschobenen Strukturankern;
- Fehlschlag bei reservierten Formen vor dem README-Endanker;
- Nachweis, dass spätere README-Abschnitte nicht Teil des lokalen IUM11-Prüfbereichs sind;
- Nachweis, dass Build und `--check` eine fehlende kanonische Struktur nicht synthetisieren.

### 10.3 Zu entfernende Tests

Entfernt werden Tests, deren einziger Zweck die semantische Erkennung von Fenced Code, eingerücktem Code, Listenfortsetzungen, Setext-Überschriften, HTML-Kommentaren oder Raw-HTML-Containern ist. Bleibt ein Test zusätzlich für Marker-, Byte- oder Tokenverträge relevant, wird er auf diesen Vertrag reduziert statt gelöscht.

## 11. Umsetzung und Git-Historie

Die Rettung wird als normaler nachfolgender Cleanup-Commit umgesetzt. Es gibt kein `reset`, kein `rebase`, kein `amend`, keinen Force-Push und keine manuelle Bearbeitung von `.git/`. Die fehlerhaften Entwicklungsrunden bleiben als nachvollziehbare Geschichte erhalten.

Die Umsetzung erfolgt testgetrieben in dieser Reihenfolge:

1. Tests auf das kanonische Dokumentprofil und die neue README-Endmarke umstellen.
2. Exakte Anker- und Bereichslogik implementieren.
3. Partiellen CommonMark-/HTML-Parser und ausschließlich daran gebundene Tests entfernen.
4. Reviewcheckliste ergänzen und die drei Dokumente kanonisch bauen.
5. Fokussierte Tests, Vollsuite, Buildchecks und alle Validatoren ausführen.
6. Cleanup committen und gegen diese Spezifikation reviewen.

## 12. Reviewvertrag und Schleifenbremse

Der erneute Task-8-Review prüft ausschließlich die in diesem Dokument definierte Systemgrenze. Gegenbeispiele, die eine Interpretation beliebiger CommonMark- oder HTML-Semantik verlangen, sind kein Implementierungsbefund, sondern ein Widerspruch zu dieser ausdrücklich freigegebenen Nichtfunktion.

Es gibt nach der Implementierung genau einen vollständigen Review und höchstens eine klar abgegrenzte Korrekturrunde. Entsteht danach erneut die Forderung nach einem Markdown-/HTML-Parser oder nach einer wesentlich erweiterten Garantie, stoppt Task 8 und geht als neue Architekturentscheidung an den Auftraggeber zurück. Ausnahmerunden dürfen diese Grenze nicht stillschweigend erweitern.

Critical- oder Important-Befunde innerhalb des hier festgelegten Vertrags blockieren weiterhin die Abnahme. Minor-Befunde werden nach Auswirkung auf den Vertragszweck bewertet; sie lösen nicht automatisch eine weitere Architektur- oder Parserrunde aus.

## 13. Akzeptanzkriterien

Das Rettungsdesign ist umgesetzt, wenn:

1. der selbst gebaute CommonMark-/HTML-Parser einschließlich `HTMLParser`-Abhängigkeit vollständig entfernt ist;
2. der Publikationsvertrag, JSON, drei byteidentische Faktenblöcke und alle fachlichen Status-/Privacygrenzen unverändert erhalten sind;
3. README und Guides dem exakten kanonischen Dokumentprofil entsprechen;
4. die lexikalische Textgrenze ausschließlich exakt bestimmte Textbereiche prüft und keine Markdown-Sichtbarkeit behauptet;
5. die Reviewanleitung die verbindliche redaktionelle Sichtbarkeitscheckliste enthält;
6. der Satz zu flexiblen Vertiefungs-, Transfer- und Projektmodulen sichtbar erhalten bleibt;
7. fokussierte Tests, Vollsuite, Buildchecks, Node-Syntax sowie IUM11-, IUM10-, IUM09- und Phase-0-Validatoren grün sind;
8. der abschließende Review keine offenen Critical- oder Important-Befunde innerhalb dieses Vertrags meldet;
9. reale Pilotierung, Statushochsetzung, Release und Phase 1 weiterhin ausgeschlossen bleiben.
