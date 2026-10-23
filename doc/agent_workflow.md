# AstroPaper Agent Workflow

This is the operational manual for agents producing AstroPaper reports. The reader-facing [`README.md`](../README.md) points agents here; nothing in this file is meant for a casual visitor.

The manual documents:

- repository layout and the three-tier profile stack
- filename and cadence conventions
- report structure and the per-paper summary format
- source and skim workflow, and report-reliability framing
- the eight-step standard session workflow (including public-mirror sync)
- PDF rendering
- privacy rules for tracked files
- writing style
- a maintenance checklist for the workflow itself

---

## Repository Layout

```text
AstroPaper/
├── README.md
├── LICENSE
├── doc/
│   ├── agent_workflow.md                # this file
│   ├── template_research_profile.md     # generic public scaffold; tracked
│   ├── research_profile.md              # your customized working profile; gitignored (read by the agent each session)
│   └── research_profile.local.md        # your deep archive; gitignored (not read automatically)
├── scripts/
│   ├── render_report_pdf.sh
│   ├── report_pdf_colors.py             # PDF-only author and ID colors
│   ├── report_pdf_colors.tex
│   ├── check_report_reading.py          # full-text evidence gate
│   └── sync_public_mirror.sh
├── tests/test_report_pipeline.py
└── YYYY/
    └── MM/
        ├── arXiv_*.md
        └── pdf/                         # local-only PDF renders; gitignored
```

### `doc/`

Use `doc/` for reusable review context. The research profile is organized as a three-tier stack so that public scope, operational strategy, and personal archive stay separate. The agent reads only one profile file per session; the others are scaffolding and archive.

**Tier 1 — `doc/template_research_profile.md` (tracked, public).** Generic scaffold. Names broad fields and methodology categories but intentionally omits priority ordering, method-recurrence patterns, and instrument preference rankings. Anything tracked here is published, so it must not leak research strategy. This is what someone gets when they clone the repo fresh.

**Tier 2 — `doc/research_profile.md` (gitignored, local).** Your customized working profile — derived from Tier 1 and populated with your real priorities, recurring methods, and survey weightings. This is the file the agent actually reads every session. Kept local so your strategy does not leak.

**Tier 3 — `doc/research_profile.local.md` (gitignored, local).** Your deep archive — private notes, reading statistics, project-derived topic inventories, and anything else too heavy for the agent's session context. The agent does **not** read this file automatically; consult it manually when you need to refresh or expand Tier 2.

**Agent precedence.** Read `doc/research_profile.md` if it exists. Otherwise fall back to `doc/template_research_profile.md` (the generic scaffold) so the agent still has something to filter against on a fresh clone. Do not automatically open `doc/research_profile.local.md`; only read it if the user explicitly asks.

### `YYYY/MM/`

Use year/month folders for dated report snapshots. The `MM` folder is the month from the report filename's anchor date, usually the daily date, weekly end date, monthly month, or custom-period end date.

- `YYYY/MM/arXiv_*.md` files are the primary tracked reports.
- `YYYY/MM/pdf/` stores local PDF renders of the Markdown reports. The `**/pdf/` pattern is gitignored by default.

Current examples:

- `2026/04/arXiv_20260417w.md`

## Customize the Review

To adapt this repository for a different literature-review project:

- Replace the topic profile: adapt `doc/template_research_profile.md` (the tracked public scaffold) to your field's broad scope, copy it to `doc/research_profile.md` locally, and populate that with your actual priorities, weightings, and survey preferences. Optionally keep a deeper archive in `doc/research_profile.local.md`. Only Tier 1 is tracked.
- Change the default literature source if needed, for example from `astro-ph.GA` to another arXiv category or journal feed.
- Change the report title rule if the audience changes.
- Keep private preferences, unreleased proposals, local file paths, and collaborator-specific notes out of tracked files.
- Keep the cadence suffix and PDF rendering workflow unless there is a clear reason to change them.

The current default report title is:

```markdown
# arXiv astro-ph.GA Review for high-z galaxy/LSS/IGM/AGN astronomers
```

If the repository is reused for another field, replace this title everywhere in the report template and this manual.

## Review Cadences and File Names

Use filenames that encode the time span of the review.

Suffix meanings:

- `d` daily
- `w` weekly
- `m` monthly
- `y` yearly
- `s` seasonal
- `p` self-defined period

Recommended patterns:

- daily snapshot: `YYYY/MM/arXiv_YYYYMMDDd.md`
- weekly snapshot: `YYYY/MM/arXiv_YYYYMMDDw.md`
- monthly retrospective: `YYYY/MM/arXiv_YYYYMMm.md`
- yearly retrospective: `YYYY/MM/arXiv_YYYYy.md`, where `MM` is the report publication or anchor month, normally `12` for a year-end retrospective
- seasonal retrospective: `YYYY/MM/arXiv_YYYYQ1s.md` or another season label ending in `s`, where `MM` is the season end month
- self-defined period: `YYYY/MM/arXiv_YYYYMMDD_YYYYMMDDp.md`, where `MM` is the end-date month

The filename date should normally be the report date, anchor date, or end date. The report header must always state the exact coverage dates, especially when the request is ambiguous.

Examples:

- `2026/04/arXiv_20260420d.md` for a daily report covering 2026-04-20
- `2026/04/arXiv_20260417w.md` for a weekly report ending or anchored on 2026-04-17
- `2025/11/arXiv_20251101_20251130p.md` for a custom period from 2025-11-01 to 2025-11-30

## Report Requirements

Start with results. Use this order for new reports:

1. The standard title and a single `Coverage:` line with exact dates.
2. `## Read-First Shortlist`: a table with linked arXiv ID, first author, title, and one sentence stating the main finding or reading value. Aim for 5-8 daily entries or 8-12 weekly entries; use fewer when warranted rather than padding the list.
3. `## Key Findings`: 3-5 concise scientific takeaways, or fewer on a sparse day. Weekly takeaways should synthesize cross-day results. Avoid repeating the shortlist verbatim.
4. Topic-grouped sections using the structured per-paper summaries below and inline paper cross-references.
5. `## Top Abstract URLs`: the top 20 relevant abstract URLs, or all relevant URLs if fewer than 20 exist. Each item includes the arXiv ID link, first author, and paper title. This list may be longer than the read-first shortlist.
6. A horizontal rule followed by a compact footer of two or three lines: `Sources:`, `Reading depth:`, and `Working model:`.

Do not include `Selection Logic`, a separate `Source categories checked` preamble, filtering weights, routine scan counts, replacement counts, or scheduling and publication narration in the report. Keep screening and source validation in the agent workflow and operational run record. Preserve per-paper scientific relevance where it helps the reader.

The footer must identify the sources and submission categories actually checked, whether replacements were excluded, and the actual reading depth. For mixed-depth reports, identify skimmed entries so readers can distinguish them from abstract-only entries. Disclose missing dates or incomplete coverage next to `Coverage:`; do not bury a material limitation in the footer.

Use the model and reasoning setting explicitly configured for the task. Do not automatically substitute a newer model or raise the reasoning setting. Disclose the model actually used in the footer; do not copy a model label from an older report or template. If the model cannot be verified, state that it is unverified.

Report scaffold (replace placeholders with verified values):

```markdown
# arXiv astro-ph.GA Review for high-z galaxy/LSS/IGM/AGN astronomers

Coverage: YYYY-MM-DD

## Read-First Shortlist

| Paper | Main finding / reading value |
|---|---|
| [arXivID](https://arxiv.org/abs/arXivID) First Author: Title | One concise finding. |

## Key Findings

- A scientific takeaway with an inline paper reference.

## [Topic]

Structured per-paper summaries.

## Top Abstract URLs

- [arXivID](https://arxiv.org/abs/arXivID) First Author: Title

---

Sources: astro-ph.GA new and cross submissions; replacements excluded.

Reading depth: targeted HTML/PDF manuscript review for all discussed papers; identify any abstract-only URL-only entries.

Working model: [actual model used]
```

### Cross-Reference Rule

When a paper is discussed in the report body, write the arXiv ID as a clickable Markdown link and immediately follow it with the first author's full name.

Example:

```markdown
[2604.13159](https://arxiv.org/abs/2604.13159) M. Galbiati
```

Use the same style in summary tables, section headings, and cross-paper discussion.

### Per-Paper Summary Format

Inside each thematic section, summarize every selected paper as a structured nested bullet. The paper line is the top-level bullet. The five field labels are required when supported by the source material:

- `**Question:**`
- `**Data:**`
- `**Method:**`
- `**Conclusion:**`
- `**Position:**`

Template:

````markdown
- [arXivID](https://arxiv.org/abs/arXivID) First Author et al. `Title`
  - **Question:** what specific question does the paper answer?
  - **Data:**
    - Instrument or dataset: relevant measurements, sample size, redshift range, or wavelength coverage
    - Instrument or dataset: additional supporting data
  - **Method:**
    - Analysis step one
    - Analysis step two
    - Analysis step three
  - **Conclusion:**
    - Direct finding with the supporting quantity in backticks.
    - Direct finding with the evidence chain stated explicitly.
  - **Position:** one-line placement of the paper in the broader field, preferably using prior work cited by the paper itself
````

Format rules:

- Field labels must be exactly `**Question:**`, `**Data:**`, `**Method:**`, `**Conclusion:**`, and `**Position:**`.
- Use all five fields unless the abstract and skim genuinely do not support one.
- Do not fabricate content to fill a field.
- `Question` is a single sentence phrased as a question.
- `Data` is subdivided by instrument, survey, simulation, or dataset whenever possible.
- `Method` is a list of discrete analysis steps.
- `Conclusion` is a list of direct findings. Quantities belong inside backticks, for example `z=3.06`, `N_HI~10^14.6 cm^-2`, or `delta~41`.
- `Position` is a single line placing the paper in the field. Prefer prior-work citations found in the manuscript. Use inferred field knowledge sparingly.
- Sub-bullets use two-space indentation. Sub-sub-bullets use four-space indentation.

## Source and Skim Workflow

Full-text verification is a mandatory completion and publication gate for new or updated reports, for both daily and weekly reviews. Abstracts are for screening; they cannot substitute for manuscript reading in the shortlist, Key Findings, or structured thematic summaries.

1. Read the abstract for topic classification and initial ranking.
2. Fetch `https://arxiv.org/html/<arxivId>` and inspect the relevant data/sample, methods, results, and limitations in the manuscript. Check the numbers, uncertainty, sample definition, and scope behind each substantive conclusion. This is a targeted full-text review, not a requirement to read every paragraph.
3. If manuscript HTML is unavailable or incomplete, fetch the PDF and inspect its text and relevant figures/tables instead.
4. If neither manuscript source is usable, record the failed attempts. An abstract-only paper may appear only as an explicitly marked URL-only entry, not as a completed scientific summary. If a paper needed for the intended coverage remains unverified, keep the report as an incomplete local draft, disclose the gap beside `Coverage:`, and do not mark it complete, commit it for publication, or push it. Do not silently drop an important paper merely to pass this gate.

Keep a local reading ledger at `.codex/reading_checks/<report-stem>.json` (ignored, never published), binding it to the report path and `report_sha256`. For every paper discussed outside `Top Abstract URLs`, record its ID, manuscript URL, local snapshot path and SHA-256, `reading_depth: targeted-full-text`, checked sections (`data`, `methods`, `results`, `limitations`), verified claims with section/table/figure locators, and the limitations affecting interpretation. Reuse evidence for weekly reports only after verifying that it matches the manuscript version and claims being summarized. Recheck changed report content before refreshing its recorded hash.

Run the gate before finalization:

```bash
python3 scripts/check_report_reading.py YYYY/MM/arXiv_FILENAME.md
```

The ledger schema is illustrated by the fixtures in `tests/test_report_pipeline.py`. The script rejects missing full-text evidence, abstract URLs, absent section/claim checks, and changed source snapshots. It validates records and source integrity; the agent must still perform the scientific reading and claim verification. A download alone is not evidence of reading. Historical reports do not need retroactive ledgers unless their scientific content is updated.

Suggested skim prompt for findings:

> Extract 3–5 key numerical findings from this paper, each paired with the specific measurement, statistic, or observation that supports it. Also extract 2–3 specific quantities such as redshift, overdensity, column density, velocity offset, luminosity, mass, or escape fraction, with units. Ignore the introduction, methods minutiae, and references. Return as a bullet list.

Suggested skim prompt for `Position`:

> List the 2–3 prior papers this manuscript cites as its most direct predecessors or closest comparison studies. Give each as `FirstAuthor+YEAR` plus a one-line reason the manuscript cites it.

Do not invent numbers or prior-work citations. Identify any abstract-only URL entries explicitly; they cannot support report conclusions.

## Report Reliability

Reports are AI-assisted reading notes. They are useful for triage, prioritization, and remembering why a paper mattered, but they are not substitutes for the papers themselves.

- Verify scientific claims, numerical values, and citations against the original paper before citing them.
- Treat `Position` lines as reading-context annotations, not formal literature-review conclusions.
- Preserve the reading-depth footer in each report so readers can distinguish skim-backed entries from abstract-only entries.
- Prefer short excerpts and paraphrases; do not copy long passages from abstracts or papers.

## Standard Workflow

### 1. Refresh the Profile

Before filtering papers, read the active profile. **Agent precedence:** read `doc/research_profile.md` if it exists. Otherwise fall back to `doc/template_research_profile.md` (the generic public scaffold) so there is always something to filter against. Do **not** automatically open `doc/research_profile.local.md` — that file is the user's deep archive and is too detailed for a per-session read. Consult it only if the user explicitly asks.

### 2. Resolve the Time Window

Convert the request into explicit dates. Examples:

- `today`
- `latest week`
- `2025-11-01` to `2025-11-30`
- `November 2025`

The report header must state the resolved coverage date or date range.

### 3. Query the Literature Source

Default source in this repository: `arXiv astro-ph.GA`.

Identify the sources used in the report footer. For arXiv reports, record whether the review used new submissions, cross submissions, replacements, or another category. Keep scan counts in the operational run record. Disclose incomplete coverage next to the coverage date.

### 4. Filter Against the Profile

Rank candidate papers by relevance to the active profile (per the precedence rule in step 1). The profile file is the only source for topic weighting — do not substitute or supplement it with hard-coded priority lists outside the profile. This keeps the README and this manual free of strategy content that would otherwise leak through any public fork.

### 5. Write the Report

Save reports in the appropriate `YYYY/MM/` folder. Follow the results-first order in Report Requirements. A reader should immediately see the recommended papers and scientific findings, with coverage and reading depth available in the compact metadata. Do not repeat the filtering procedure in each report.

### 6. Rebuild the PDF

After creating or editing any `YYYY/MM/arXiv_*.md` report, rebuild its PDF before considering the task finished.

Use:

```bash
./scripts/render_report_pdf.sh YYYY/MM/arXiv_FILENAME.md
```

The output should be:

```text
YYYY/MM/pdf/arXiv_FILENAME.pdf
```

Keep the PDF filename matched to the Markdown filename.

### 7. Verify the Output

At minimum:

- pass `scripts/check_report_reading.py` for every new or scientifically updated report; independently confirm the recorded manuscript evidence supports the claims
- check that the Markdown file opens cleanly
- check that the PDF was created
- verify author names are bold charcoal and arXiv IDs are muted teal throughout the PDF (shortlist, findings, summaries, and URL list); inspect the rendered pages and confirm links remain usable
- check PDF metadata with `pdfinfo` when available
- extract a few lines with `pdftotext` when available
- confirm that the report title, date coverage, and working-model line are present
- confirm the order: Read-First Shortlist, Key Findings, thematic summaries, Top Abstract URLs, then the Sources / Reading depth / Working model footer
- confirm shortlist sizes are appropriate, paper IDs and titles match the sources, and summary fields are supported by the material read
- confirm no routine selection-criteria or scheduling preamble remains; do not require the retired Selection Logic, Executive View, or Source categories checked headings
- verify coverage limitations and mixed reading depths are disclosed accurately
- run formatting and privacy checks; keep PDFs and research profiles ignored and untracked

### 8. Sync the Public Mirror

This repository can be used as a private working repo while maintaining a clean public mirror. After the Markdown report and local PDF render are finalized, export the sanitized current tree to the public mirror:

```bash
./scripts/sync_public_mirror.sh "Add arXiv YYYYMMDD report"
```

The sync script archives the current tracked tree, creates a fresh one-commit export, runs a privacy scan, and force-updates the public mirror. It does not copy ignored files, so local profiles, PDFs, agent logs, and recovery files stay private.

Default public-mirror settings:

- remote: `public`
- branch: `main`

Override them with `PUBLIC_REMOTE` or `PUBLIC_BRANCH` if needed.

## PDF Rendering

The standard renderer is:

```bash
scripts/render_report_pdf.sh
```

It uses `pandoc`, Python 3, and `xelatex` to produce A4 PDFs with the repository's default font and margin settings. `scripts/report_pdf_colors.py` and `scripts/report_pdf_colors.tex` render author names in bold charcoal (`#374151`) and arXiv IDs in muted teal (`#287A78`) throughout the PDF. Markdown remains ordinary clickable text on GitHub.

The renderer learns author names from canonical `[ID](abstract-URL) First Author: Title` or `[ID](abstract-URL) First Author et al.` entries and colors their occurrences throughout the report. Keep author spelling consistent across sections. For an additional author mention absent from those entries, link the author name to the corresponding arXiv abstract; compact `Author+YYYY` literature citations are also recognized. Keep names outside code/math. Verify rendered output instead of relying only on successful compilation. Other prose and non-paper links retain their normal colors.

These rendering rules apply whenever a PDF is generated. Do not bulk rewrite historical Markdown or regenerate historical PDFs without a request.

Required command-line tools:

- `pandoc`
- `xelatex`
- `python3`

Useful verification tools:

- `pdfinfo`
- `pdftotext`

PDF renders are local outputs and are ignored by git by default. If a project needs to publish PDFs, change the ignore policy deliberately and document that decision.

The public-mirror sync script is:

```bash
scripts/sync_public_mirror.sh
```

It should be run only after the private working repo has the report you want to publish committed at `HEAD`.

## Privacy and Sharing

This repository is structured so tracked files can be kept shareable, but privacy still requires active review.

Before syncing, publishing, or sharing:

- remove personal names, private collaborator details, exact local file paths, unreleased project details, and confidential proposal text
- keep `doc/research_profile.local.md` and `doc/research_profile.md` untracked
- avoid putting private information in report titles, filenames, or report content
- review generated reports for accidental copied text from local notes
- run a repository-wide text search for sensitive terms when needed

Public-project style documentation does not make the repository public. Repository visibility is a separate hosting decision.

For this live reading-log repo, Markdown reports are the public artifact and PDFs remain local-only unless the project policy changes deliberately.

## Writing Style

Use a direct, factual report style.

- Use short declarative sentences.
- Cut hedging, filler, and padding.
- Keep structure flat.
- Keep lists parallel.
- Use exact technical terms, arXiv IDs, redshifts, instrument names, and file paths.
- Avoid transitional recap phrases such as "in summary" or "as noted above".
- In per-paper summaries, do not write "the abstract reports", "the paper argues", "the work highlights", or similar attribution hedges. State the finding directly when the source supports it.

Reusable writing prompt:

> Write in a direct, factual style. Short declarative sentences. No hedging, no filler. Flat structure. Lists must be short and parallel. Use the structured Question / Data / Method / Conclusion / Position format for per-paper summaries. Put quantities in backticks. Do not attribute findings to "the abstract" or "the paper" unless discussing source limitations.

## Maintenance Checklist

Workflow style update, 2026-09-30: after approval of the local preview, adopted bold charcoal authors (`#374151`) and muted teal arXiv IDs (`#287A78`) as the PDF default, superseding the magenta/green palette below. Updated the renderer, tests, README, profile template, workflow, and daily automation prompt. The manuscript verification gate remains unchanged. Validated with unit tests and a fresh latest-report PDF, including page rendering, author weight/color, and preserved links.

Workflow change record, 2026-09-30: made HTML/PDF manuscript verification a mandatory completion/publication gate, with local evidence records and `scripts/check_report_reading.py`. Added deterministic PDF colors for authors (magenta) and arXiv IDs (green), preserving plain Markdown and clickable links. Synchronized README, workflow, public profile template, and the daily automation prompt. The private research profile remains a local ranking input. Validation covers missing/invalid evidence, PDF color rendering, link preservation, and a fresh render of the latest daily report; older report content is unchanged.

Workflow change record, 2026-09-06: new reports use a results-first shortlist, concise Key Findings, and compact source/model footer. This replaces the recurring selection preamble and Executive View. Task configuration controls model selection. Updated this manual and the README; historical reports retain their original format.

Use this checklist when updating the repository workflow:

- keep the public profile scaffold in `doc/template_research_profile.md`
- keep the operational working profile in ignored `doc/research_profile.md`
- keep deep private notes in ignored `doc/research_profile.local.md`
- keep dated reports in `YYYY/MM/` folders
- keep PDF renders in `YYYY/MM/pdf/`
- keep `**/pdf/` gitignored; publishing PDFs requires an explicit project decision
- update this manual when naming, formatting, or rendering conventions change
- recompile the matching PDF after every report create/update
- sync the public mirror after a report is finalized and committed, if the update should be public
- keep tracked docs and reports free of private information
