# IUM11 Publication Boundary Rescue Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Den überdehnten partiellen CommonMark-/HTML-Parser entfernen und IUM11-Task 8 auf einen exakten, deterministischen Publikationsvertrag mit redaktioneller Sichtbarkeitsprüfung zurückführen.

**Architecture:** `scripts/ium11_publication.py` prüft nur noch geschlossene Vertragsdaten, exakte UTF-8-/LF-Dokumentanker und reservierte lexikalische Formen in eindeutig abgegrenzten Textbereichen. README und Guides erhalten eine kanonische Struktur; die tatsächliche Markdown-Sichtbarkeit wird mit einer verpflichtenden Checkliste im GitHub-kompatiblen Renderer geprüft. Die Umsetzung erfolgt inline in der bestehenden Worktree und ohne weitere Subagentenschleife.

**Tech Stack:** Python 3 Standardbibliothek, `unittest`, JSON, Markdown, PowerShell, Git

## Global Constraints

- Freigegebene Spezifikation: `docs/superpowers/specs/2026-08-02-ium11-publication-boundary-rescue-design.md`.
- Kein externer CommonMark-/HTML-Parser und kein eigener partieller Markdown-/HTML-Parser.
- `compile_publication_contract(...)`, Vertragsfelder, kanonische Quellen, JSON-Artefakt, Faktenblock, Privacygrenzen, Statusgrenzen und Klassenbänder bleiben unverändert.
- Der Faktenblock bleibt byteidentisch in `README.md`, `pilot/docs/teacher-guide.md` und `pilot/docs/review-guide.md`.
- Der Satz „Flexible Vertiefungs-, Transfer- und Projektmodule bleiben“ bleibt im generierten Faktenblock und sichtbar erhalten.
- Automatische Prüfung garantiert nur exakte Struktur und reservierte lexikalische Formen; gerenderte Sichtbarkeit und freie Prosa sind redaktionelle Prüfpunkte.
- Reale Pilotierung, Statushochsetzung, Release und Phase 1 bleiben ausgeschlossen.
- Kein Reset, Rebase, Amend, Force-Push oder History-Rewrite.
- Vor jedem Commit `git fetch --prune` und `git pull --ff-only`; bei einem Fehler nicht pushen oder committen.
- Umsetzung inline in der aktuellen Session; keine neue Subagenten- oder Ausnahmerunde.

---

## File Structure

- Modify: `README.md` — erhält den expliziten Endanker des lokalen IUM11-Prüfbereichs.
- Modify: `pilot/docs/review-guide.md` — enthält die verbindliche redaktionelle Rendering-Checkliste.
- Modify: `scripts/ium11_publication.py` — ersetzt Markdown-/HTML-Interpretation durch exakte Strukturanker und lexikalische Bereichsprüfung.
- Modify: `tests/test_ium11_publication_contract.py` — fokussierte Unit- und Buildtests für das kanonische Dokumentprofil; entfernt ausschließlich Parser-Adversarialtests.
- Modify: `tests/test_validate_ium11.py` — integriert denselben engen Vertrag in den vollständigen IUM11-Validator und entfernt doppelte Parser-Adversarialtests.
- Modify: `docs/superpowers/specs/2026-08-02-ium11-publication-boundary-rescue-design.md` — dokumentiert die bereits erteilte schriftliche Freigabe.
- Do not modify: `scripts/build_ium11_publication_contract.py` — die vorhandene Schnittstelle `validate_publication_embedding(relative_path, text)` bleibt erhalten.
- Do not modify: `pilot/docs/publication-contract.json`, `pilot/pilot-protocol.json`, `roadmap/time-model.json` — Vertragswerte und kanonische Quellen bleiben unverändert.

---

### Task 1: Kanonische Dokumentanker und redaktionelles Gate

**Files:**

- Modify: `README.md`
- Modify: `pilot/docs/review-guide.md`

**Interfaces:**

- Consumes: vorhandene Überschrift `## IUM11-Pilotinstrument`, vorhandener Faktenblock und `## Zentrale Einstiege`.
- Produces: exakter README-Anker `<!-- IUM11-PUBLICATION-SCOPE:END -->` sowie überprüfbare Reviewtexte für die spätere Layoutvalidierung.

- [ ] **Step 1: README-Endanker setzen**

In `README.md` unmittelbar vor `## Zentrale Einstiege` exakt einfügen:

```markdown
<!-- IUM11-PUBLICATION-SCOPE:END -->

## Zentrale Einstiege
```

Der letzte handgepflegte IUM11-Absatz bleibt vor dem Marker unverändert.

- [ ] **Step 2: Redaktionelle Rendering-Checkliste ergänzen**

In `pilot/docs/review-guide.md` vor `## Retention und Veröffentlichung nach der Entscheidung` ergänzen:

```markdown
## Redaktionelles Publikationsgate

Prüfen Sie README, Lehrkräfteanleitung und Reviewanleitung vor der Task-8-Abnahme in einem GitHub-kompatiblen Renderer:

- Die vorgesehene Überschrift und die vollständige Faktentabelle sichtbar rendern.
- Die Faktentabelle weder als Code noch als Kommentar oder versteckten HTML-Inhalt darstellen.
- Faktenblock, erläuternde Prosa und Links in der vorgesehenen Reihenfolge anzeigen.
- Prüfen, dass die freie Prosa dem Faktenblock nicht widerspricht.
- Flexible Vertiefungs-, Transfer- und Projektmodule sichtbar erhalten.

Dokumentieren Sie das Ergebnis im Task-8-Review. Diese Prüfung ist ein redaktionelles Gate und keine automatische Markdown- oder HTML-Interpretation.
```

- [ ] **Step 3: Redaktionelle Struktur direkt prüfen**

README und Reviewanleitung vollständig lesen und prüfen, dass der Marker exakt zwischen IUM11-Prosa und `## Zentrale Einstiege` steht und die Checkliste alle fünf Punkte der freigegebenen Spezifikation abbildet. Dafür keinen Test auf konkrete Prosaformulierungen hinzufügen: Die Anleitung ist für Menschen bestimmt und ein Textänderungsdetektor würde kein Produktionsverhalten prüfen.

- [ ] **Step 4: Bestehende Publikationsprüfung ausführen**

Run:

```powershell
python -B scripts/build_ium11_publication_contract.py --check
python -B scripts/validate_ium11.py
```

Expected: alle Befehle PASS; der vorhandene Build bewahrt den neuen Marker, da er nur den Faktenblock ersetzt.

- [ ] **Step 5: Task 1 committen**

```powershell
git fetch --prune
git pull --ff-only
git diff --check
git add -- README.md pilot/docs/review-guide.md
git diff --cached --check
git commit -m "docs: add ium11 publication review gate"
```

### Task 2: Parser durch exakte Strukturprüfung ersetzen

**Files:**

- Modify: `scripts/ium11_publication.py:1-4, 502-942`
- Modify: `tests/test_ium11_publication_contract.py:10-1231`

**Interfaces:**

- Consumes: `extract_publication_block(text) -> str`, `replace_publication_block(text, block) -> str`, drei bekannte Pfade aus `PUBLICATION_PATHS`.
- Produces: `README_SCOPE_END_MARKER: str`, `validate_publication_embedding(relative_path, text) -> None` und `validate_publication_text_boundary(relative_path, text) -> None` mit unveränderten öffentlichen Signaturen.
- Internal: `_publication_layout(relative_path, text) -> tuple[str, str]` liefert `(block, inspected_text)` nach erfolgreicher exakter Strukturprüfung.

- [ ] **Step 1: Testhelfer für kanonische Veröffentlichungen ergänzen**

In `tests/test_ium11_publication_contract.py` `README_SCOPE_END_MARKER` importieren und unter `ROOT` diese Helfer ergänzen:

```python
GUIDE_HEADINGS = {
    "pilot/docs/teacher-guide.md": "# Lehrkräfteanleitung zum IUM11-Pilotinstrument",
    "pilot/docs/review-guide.md": "# Reviewanleitung zum IUM11-Pilotinstrument",
}


def canonical_readme(block, body="Erklärende deutsche Prosa."):
    return (
        "# Projekt\n\n"
        "## IUM11-Pilotinstrument\n\n"
        f"{block}\n\n{body}\n\n"
        f"{README_SCOPE_END_MARKER}\n\n"
        "## Zentrale Einstiege\n\n"
        "Späterer Inhalt.\n"
    )


def canonical_guide(relative_path, block, body="Erklärende deutsche Prosa."):
    return f"{GUIDE_HEADINGS[relative_path]}\n\n{block}\n\n{body}\n"
```

Alle erhaltenen lexikalischen Tests verwenden danach diese Helfer statt freier H1-/H2-Fixtures.

- [ ] **Step 2: Failing Unit-Tests für das exakte Profil schreiben**

Die alten Visibility-Tests durch diese Vertragsfälle ersetzen:

```python
def test_embedding_requires_exact_canonical_document_profile(self):
    block = render_publication_markdown_block(self.compile())
    valid_readme = canonical_readme(block)
    valid_teacher = canonical_guide("pilot/docs/teacher-guide.md", block)
    valid_review = canonical_guide("pilot/docs/review-guide.md", block)
    validate_publication_text_boundary("README.md", valid_readme)
    validate_publication_text_boundary("pilot/docs/teacher-guide.md", valid_teacher)
    validate_publication_text_boundary("pilot/docs/review-guide.md", valid_review)

    cases = (
        ("README.md", valid_readme.replace(README_SCOPE_END_MARKER, "")),
        ("README.md", valid_readme.replace(
            README_SCOPE_END_MARKER,
            README_SCOPE_END_MARKER + "\n" + README_SCOPE_END_MARKER,
        )),
        ("README.md", valid_readme.replace(
            "## IUM11-Pilotinstrument\n\n" + block,
            "## IUM11-Pilotinstrument\nHinweis\n\n" + block,
        )),
        ("pilot/docs/teacher-guide.md", "Vorspann\n" + valid_teacher),
        ("pilot/docs/review-guide.md", valid_review.replace(
            GUIDE_HEADINGS["pilot/docs/review-guide.md"], "# Andere Anleitung", 1,
        )),
    )
    for relative_path, text in cases:
        with self.subTest(relative_path=relative_path, text=text[:60]):
            with self.assertRaises(IUM11PublicationError):
                validate_publication_text_boundary(relative_path, text)

def test_readme_boundary_ends_at_explicit_scope_marker(self):
    block = render_publication_markdown_block(self.compile())
    validate_publication_text_boundary(
        "README.md",
        canonical_readme(block).replace(
            "Späterer Inhalt.", "Späterer Inhalt mit available.",
        ),
    )
    with self.assertRaises(IUM11PublicationError):
        validate_publication_text_boundary(
            "README.md",
            canonical_readme(block, "IUM11 ist available."),
        )
```

- [ ] **Step 3: Red-Zustand gegen die alte Parserarchitektur belegen**

Run:

```powershell
python -B -m unittest tests.test_ium11_publication_contract.IUM11PublicationRenderTests.test_embedding_requires_exact_canonical_document_profile tests.test_ium11_publication_contract.IUM11PublicationRenderTests.test_readme_boundary_ends_at_explicit_scope_marker
```

Expected: mindestens der fehlende README-Endanker und der nichtkanonische Guide-Präfix werden vom alten Parser fälschlich akzeptiert, daher FAIL.

- [ ] **Step 4: Exakte Konstanten und Layoutfunktion implementieren**

In `scripts/ium11_publication.py` ergänzen:

```python
README_HEADING = "## IUM11-Pilotinstrument"
README_SCOPE_END_MARKER = "<!-- IUM11-PUBLICATION-SCOPE:END -->"
README_NEXT_HEADING = "## Zentrale Einstiege"
GUIDE_HEADINGS = {
    "pilot/docs/teacher-guide.md": "# Lehrkräfteanleitung zum IUM11-Pilotinstrument",
    "pilot/docs/review-guide.md": "# Reviewanleitung zum IUM11-Pilotinstrument",
}


def _exact_line_count(text, line):
    return text.split("\n").count(line)


def _publication_layout(relative_path, text):
    normalized_path = str(relative_path).replace("\\", "/")
    _require("\r" not in text, f"{relative_path}: publication text must use LF")
    block = extract_publication_block(text)
    block_start = text.index(block)
    block_end = block_start + len(block)

    if normalized_path == "README.md":
        _require(
            _exact_line_count(text, README_HEADING) == 1,
            "README.md: IUM11 section heading must occur once",
        )
        _require(
            text.count(README_SCOPE_END_MARKER) == 1,
            "README.md: IUM11 scope end marker must occur once",
        )
        expected_prefix = f"{README_HEADING}\n\n{block}"
        _require(
            expected_prefix in text,
            "README.md: publication block must immediately follow IUM11 heading",
        )
        scope_end = text.index(README_SCOPE_END_MARKER)
        _require(
            block_end < scope_end,
            "README.md: IUM11 scope end marker must follow publication block",
        )
        expected_suffix = f"{README_SCOPE_END_MARKER}\n\n{README_NEXT_HEADING}"
        _require(
            text.startswith(expected_suffix, scope_end),
            "README.md: IUM11 scope end marker must precede central entries",
        )
        return block, text[block_end:scope_end]

    heading = GUIDE_HEADINGS.get(normalized_path)
    _require(heading is not None, f"unsupported publication path: {relative_path}")
    _require(
        text.startswith(f"{heading}\n\n{block}"),
        f"{relative_path}: publication block must immediately follow canonical H1",
    )
    return block, text[:block_start] + text[block_end:]
```

`validate_publication_embedding(...)` ruft nur `_publication_layout(...)` auf. `validate_publication_text_boundary(...)` verwendet den zurückgegebenen `inspected_text` und behält die vorhandene Schleife über `RESERVED_OUTSIDE_BLOCK_PATTERNS` einschließlich Unicode-Bezeichnergrenze unverändert.

- [ ] **Step 5: Partiellen Parser vollständig entfernen**

Aus `scripts/ium11_publication.py` entfernen:

```python
from html.parser import HTMLParser
```

Sowie vollständig die Definitionen:

```text
_fence_opening
_fenced_code_ranges
_leading_indentation_width
_indented_code_ranges
_position_in_ranges
_mask_ranges
_html_comment_ranges
_HTML_VOID_TAGS
_RawHtmlContainerParser
_raw_html_container_ranges
_markdown_visibility_ranges
_position_enclosed_by_comment
_atx_heading_level
_is_thematic_break
_is_html_block_start
_is_setext_paragraph_text
_visible_heading_spans
_readme_ium11_section_span
_readme_ium11_section
_visible_h1_spans
```

Danach muss dieser Scan ohne Treffer enden:

```powershell
rg -n "HTMLParser|_fence_opening|_markdown_visibility_ranges|_visible_heading|_RawHtmlContainerParser|setext|indented_code|raw_html" scripts/ium11_publication.py
```

- [ ] **Step 6: Unit-/Buildtests auf den neuen Vertrag begrenzen**

In `tests/test_ium11_publication_contract.py` vollständig entfernen:

```text
test_readme_scope_uses_commonmark_fence_info_rules
test_markdown_visibility_masks_only_commonmark_indented_code_before_html
test_setext_scope_requires_commonmark_paragraph_text
test_readme_boundary_uses_visible_commonmark_h2
test_guides_count_visible_atx_and_setext_h1
test_builder_rejects_raw_html_wrapped_structures_before_writing
test_builder_allows_unrelated_raw_html_outside_publication_structures
test_builder_rejects_block_after_visible_setext_h2_before_writing
test_builder_rejects_commonmark_indented_h2_and_h1_headings
test_builder_accepts_four_space_pseudo_headings
```

`test_boundary_requires_exactly_one_readme_section_and_one_marker_pair` durch `test_embedding_requires_exact_canonical_document_profile` ersetzen. `test_builder_rejects_shifted_or_hidden_blocks_before_writing` auf fehlende/doppelte/vertauschte Faktenmarker, exakte H1/H2-Präfixe und den README-Endanker reduzieren. Alle lexikalischen, Byte-, Build-, Read-only-, Idempotenz- und Atomizitätstests bleiben erhalten.

- [ ] **Step 7: Fokussierte Datei grün ausführen**

Run:

```powershell
python -B -m unittest tests.test_ium11_publication_contract
python -B scripts/build_ium11_publication_contract.py --check
```

Expected: PASS. `rg` aus Step 5 liefert Exitcode 1 wegen null Treffern; das ist hier das gewünschte Ergebnis.

- [ ] **Step 8: Task 2 committen**

```powershell
git fetch --prune
git pull --ff-only
git diff --check
git add -- scripts/ium11_publication.py tests/test_ium11_publication_contract.py
git diff --cached --check
git commit -m "refactor: narrow ium11 publication boundary"
```

### Task 3: Vollvalidator auf den engen Vertrag umstellen

**Files:**

- Modify: `tests/test_validate_ium11.py:1287-2049`
- Verify only: `scripts/validate_ium11.py:1274-1346`

**Interfaces:**

- Consumes: unveränderte öffentliche Funktionen `validate_publication_text_boundary(...)`, `extract_publication_block(...)`, `render_publication_markdown_block(...)`.
- Produces: vollständige IUM11-Integrationstests ohne CommonMark-/HTML-Parseranspruch.

- [ ] **Step 1: Failing Integrationstest für nichtkanonische Struktur schreiben**

Bei den Publikationsintegrationstests ergänzen:

```python
def test_full_validator_rejects_noncanonical_publication_layout(self):
    mutations = (
        (
            "README.md",
            lambda text: text.replace(
                "<!-- IUM11-PUBLICATION-SCOPE:END -->", "", 1,
            ),
        ),
        (
            "README.md",
            lambda text: text.replace(
                "## IUM11-Pilotinstrument\n\n",
                "## IUM11-Pilotinstrument\nHinweis\n\n",
                1,
            ),
        ),
        (
            "pilot/docs/teacher-guide.md",
            lambda text: "Vorspann\n" + text,
        ),
        (
            "pilot/docs/review-guide.md",
            lambda text: text.replace(
                "# Reviewanleitung zum IUM11-Pilotinstrument",
                "# Andere Reviewanleitung",
                1,
            ),
        ),
    )
    for relative_path, mutate in mutations:
        with self.subTest(relative_path=relative_path):
            with tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self.copy_publication_fixture(root)
                path = root / relative_path
                path.write_text(mutate(path.read_text(encoding="utf-8")), encoding="utf-8")
                with self.assertRaises(IUM11ValidationError):
                    validate_ium11_script._validate_publication_contract(
                        root,
                        self.protocol,
                        self.time_model,
                        self.ium10_result,
                    )
```

Die vorhandene Signatur von `_validate_publication_contract(root, compiled_protocol, time_model, ium10_result)` bleibt unverändert; keine neue Produktionsschnittstelle einführen.

- [ ] **Step 2: Red-Zustand oder Integrationsabdeckung belegen**

Run:

```powershell
python -B -m unittest tests.test_validate_ium11.IUM11PublicationTests.test_full_validator_rejects_noncanonical_publication_layout
```

Expected nach Task 2: PASS. Vor Task 2 hätte mindestens der fehlende Endanker nicht ausgelöst. Der Test dient hier als Integration der bereits testgetrieben implementierten Unit-Schnittstelle, nicht als zweite Produktionsimplementierung.

- [ ] **Step 3: Doppelte Parser-Adversarialtests entfernen**

In `tests/test_validate_ium11.py` vollständig entfernen:

```text
test_full_validator_rejects_raw_html_wrapped_publication_structures
test_full_validator_allows_unrelated_raw_html_outside_structures
test_full_validator_uses_visible_commonmark_h2_boundaries
test_full_validator_uses_commonmark_fence_info_for_readme_scope
test_full_validator_masks_only_commonmark_indented_code_before_html
test_full_validator_setext_scope_requires_commonmark_paragraph_text
test_validator_rejects_commonmark_indented_h2_and_h1_headings
```

`test_validator_rejects_shifted_or_hidden_publication_blocks` durch `test_full_validator_rejects_noncanonical_publication_layout` ersetzen. Beibehalten werden Blocktampering, CRLF/CR, fehlende/doppelte Faktenmarker, reservierte Formen, Unicode-Bezeichnergrenzen, deutsche Prosa, README-Scope, JSON-Drift und Repository-Dateikarte.

- [ ] **Step 4: README-Scope-Integration an den Endanker binden**

`test_readme_boundary_is_scoped_to_the_ium11_section` so anpassen, dass ein reserviertes Token vor `README_SCOPE_END_MARKER` scheitert und dasselbe Token nach `## Zentrale Einstiege` akzeptiert wird. Der Test darf keine „nächste sichtbare H2“ oder Markdownmaskierung mehr voraussetzen.

Kernform:

```python
marker = "<!-- IUM11-PUBLICATION-SCOPE:END -->"
before = text.replace(marker, "IUM11 ist available.\n\n" + marker, 1)
after = text.replace("## Zentrale Einstiege", "## Zentrale Einstiege\n\navailable", 1)
```

- [ ] **Step 5: Vollvalidator-Tests grün ausführen**

Run:

```powershell
python -B -m unittest tests.test_validate_ium11
python -B scripts/validate_ium11.py
```

Expected: PASS; keine Produktionsänderung außerhalb `scripts/ium11_publication.py` erforderlich.

- [ ] **Step 6: Task 3 committen**

```powershell
git fetch --prune
git pull --ff-only
git diff --check
git add -- tests/test_validate_ium11.py
git diff --cached --check
git commit -m "test: align ium11 validator with exact publication scope"
```

### Task 4: Gesamtnachweis und Abschlussreview

**Files:**

- Verify: `scripts/ium11_publication.py`
- Verify: `README.md`
- Verify: `pilot/docs/teacher-guide.md`
- Verify: `pilot/docs/review-guide.md`
- Verify: `pilot/docs/publication-contract.json`
- Modify locally, intentionally untracked: `.superpowers/sdd/2026-08-01-ium11-grade7-working-40-pilot-implementation/progress.md`

**Interfaces:**

- Consumes: die drei vorherigen Commits und die freigegebene Rettungsspezifikation.
- Produces: reproduzierbarer Gesamtnachweis und ein auf genau diesen Vertrag begrenzter Task-8-Reviewstatus.

- [ ] **Step 1: Parserfreiheit und Erhaltungsgrenzen statisch prüfen**

Run:

```powershell
rg -n "HTMLParser|_markdown_visibility_ranges|_visible_heading_spans|_RawHtmlContainerParser|_fenced_code_ranges|_indented_code_ranges" scripts/ium11_publication.py
rg -n "Flexible Vertiefungs-, Transfer- und Projektmodule bleiben" README.md pilot/docs/teacher-guide.md pilot/docs/review-guide.md
rg -n "IUM11-PUBLICATION-SCOPE:END|GitHub-kompatiblen Renderer" README.md pilot/docs/review-guide.md
```

Expected: erster Scan null Treffer; zweiter Scan genau drei Faktenblocktreffer; dritter Scan findet README-Endanker und Reviewcheckliste.

- [ ] **Step 2: Generierte Artefakte prüfen**

Run:

```powershell
python -B scripts/build_ium11_publication_contract.py --check
```

Expected: `IUM11 publication contract is current`; `git status --short` davor und danach identisch.

- [ ] **Step 3: Vollständige Regression ausführen**

Run:

```powershell
python -B -m unittest discover -s tests -p "test_*.py"
python -B scripts/build_ium11_cockpit.py --check
node --check pilot/cockpit/assets/app.js
python -B scripts/build_ium11_publication_contract.py --check
python -B scripts/validate_ium11.py
python -B scripts/validate_ium10.py
python -B scripts/validate_ium09.py
python -B scripts/validate_phase0.py
git diff --check
```

Expected: sämtliche Tests und Validatoren PASS; keine Build- oder Syntaxdrift.

- [ ] **Step 4: Vertragstreuen Abschlussreview durchführen**

Den Diff ausschließlich gegen `docs/superpowers/specs/2026-08-02-ium11-publication-boundary-rescue-design.md` prüfen:

```text
- Kein Parsercode verblieben.
- Exakte Anker, Reihenfolge, LF und Guide-Präfixe fail-closed.
- Reservierte lexikalische Formen weiterhin fail-closed.
- JSON/Faktenblöcke und fachliche Werte unverändert.
- Rendering-Checkliste vorhanden.
- Keine Forderung nach Interpretation beliebiger CommonMark-/HTML-Semantik.
```

Genau ein vollständiger Review und höchstens eine abgegrenzte Korrekturrunde sind zulässig. Eine neue Parserforderung stoppt die Aufgabe als Spezifikationskonflikt.

- [ ] **Step 5: Fortschrittsledger aktualisieren**

In der durch `.superpowers/sdd/.gitignore` absichtlich ungetrackten Datei `.superpowers/sdd/2026-08-01-ium11-grade7-working-40-pilot-implementation/progress.md` dokumentieren:

```markdown
Task 8 rescue: exact publication boundary implemented under the approved
2026-08-02 rescue specification. The custom CommonMark/HTML parser and its
adversarial contract were removed. Automated guarantees are limited to
canonical structure, byte-identical generated artifacts, and reserved lexical
forms; rendered visibility is covered by the editorial review gate.
```

Keine Statushochsetzung über den tatsächlichen Reviewbefund hinaus eintragen.

- [ ] **Step 6: Abschlusszustand ausgeben**

Task 4 erzeugt planmäßig keine getrackte Änderung und keinen zusätzlichen Commit. Falls ein Nachweis scheitert, zum verursachenden Task zurückkehren und den dortigen Test-/Commitzyklus wiederholen. Bei grünem Nachweis ausgeben:

```powershell
git status --short --branch
git log -4 --oneline
```

Expected: sauberer Worktree; Branch nur um die dokumentierten Rettungscommits voraus. Nicht pushen, bis der Nutzer den geprüften Abschlussstand erhalten hat.
