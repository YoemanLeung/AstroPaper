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
│   └── sync_public_mirror.sh
└── YYYY/
    ├── arXiv_*.md
    └── pdf/                             # local-only PDF renders; gitignored
```

### `doc/`

Use `doc/` for reusable review context. The research profile is organized as a three-tier stack so that public scope, operational strategy, and personal archive stay separate. The agent reads only one profile file per session; the others are scaffolding and archive.

**Tier 1 — `doc/template_research_profile.md` (tracked, public).** Generic scaffold. Names broad fields and methodology categories but intentionally omits priority ordering, method-recurrence patterns, and instrument preference rankings. Anything tracked here is published, so it must not leak research strategy. This is what someone gets when they clone the repo fresh.

**Tier 2 — `doc/research_profile.md` (gitignored, local).** Your customized working profile — derived from Tier 1 and populated with your real priorities, recurring methods, and survey weightings. This is the file the agent actually reads every session. Kept local so your strategy does not leak.

**Tier 3 — `doc/research_profile.local.md` (gitignored, local).** Your deep archive — private notes, reading statistics, project-derived topic inventories, and anything else too heavy for the agent's session context. The agent does **not** read this file automatically; consult it manually when you need to refresh or expand Tier 2.

**Agent precedence.** Read `doc/research_profile.md` if it exists. Otherwise fall back to `doc/template_research_profile.md` (the generic scaffold) so the agent still has something to filter against on a fresh clone. Do not automatically open `doc/research_profile.local.md`; only read it if the user explicitly asks.

### `YYYY/`

Use year folders for dated report snapshots.

- `YYYY/arXiv_*.md` files are the primary tracked reports.
- `YYYY/pdf/` stores local PDF renders of the Markdown reports. The `*/pdf/` pattern is gitignored by default.

Current examples:

- `2026/arXiv_20260417w.md`

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

- daily snapshot: `YYYY/arXiv_YYYYMMDDd.md`
- weekly snapshot: `YYYY/arXiv_YYYYMMDDw.md`
- monthly retrospective: `YYYY/arXiv_YYYYMMm.md`
- yearly retrospective: `YYYY/arXiv_YYYYy.md`
- seasonal retrospective: `YYYY/arXiv_YYYYQ1s.md` or another season label ending in `s`
- self-defined period: `YYYY/arXiv_YYYYMMDD_YYYYMMDDp.md`

The filename date should normally be the report date, anchor date, or end date. The report header must always state the exact coverage dates, especially when the request is ambiguous.

Examples:

- `2026/arXiv_20260420d.md` for a daily report covering 2026-04-20
- `2026/arXiv_20260417w.md` for a weekly report ending or anchored on 2026-04-17
- `2025/arXiv_20251101_20251130p.md` for a custom period from 2025-11-01 to 2025-11-30

## Report Requirements

Each report should normally include:

- the standard title line
- the exact coverage dates
- the working-model acknowledgment used for that report draft, for example `Working model: GPT-5.4`
- the source category or categories checked
- the profile-based filtering logic
- an executive view
- a read-first shortlist table
- topic-grouped sections with structured per-paper summaries
- inline cross-references for papers discussed in the body
- a final list of the top 20 abstract URLs, or all relevant URLs if fewer than 20 exist
- enough source disclosure for readers to know whether the summaries are skim-backed or abstract-only

Use this source-disclosure line when body skims were performed:

```text
summaries below use arXiv abstracts plus quick manuscript skims from the arXiv HTML pages when available
```

Use this line for an abstract-only report:

```text
summaries below are abstract-based only
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

Use the lightest source level that still supports the report quality needed.

Recommended source priority:

1. arXiv abstract for topic classification and the initial question.
2. arXiv HTML body skim at `https://arxiv.org/html/<arxivId>` for data details, methods, numerical findings, and cited prior work.
3. PDF fallback when HTML is unavailable.
4. Abstract-only fallback when neither HTML nor usable PDF text is available.

For weekly reports, skim only the papers that get structured thematic summaries. This usually keeps the report efficient while still making the main entries useful. For daily reports, skim all profile-relevant papers when practical.

Suggested skim prompt for findings:

> Extract 3–5 key numerical findings from this paper, each paired with the specific measurement, statistic, or observation that supports it. Also extract 2–3 specific quantities such as redshift, overdensity, column density, velocity offset, luminosity, mass, or escape fraction, with units. Ignore the introduction, methods minutiae, and references. Return as a bullet list.

Suggested skim prompt for `Position`:

> List the 2–3 prior papers this manuscript cites as its most direct predecessors or closest comparison studies. Give each as `FirstAuthor+YEAR` plus a one-line reason the manuscript cites it.

If a report is abstract-only, write direct but less detailed conclusions. Do not invent numbers or prior-work citations.

## Report Reliability

Reports are AI-assisted reading notes. They are useful for triage, prioritization, and remembering why a paper mattered, but they are not substitutes for the papers themselves.

- Verify scientific claims, numerical values, and citations against the original paper before citing them.
- Treat `Position` lines as reading-context annotations, not formal literature-review conclusions.
- Preserve the source-disclosure line in each report so readers can distinguish skim-backed entries from abstract-only entries.
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

If another source is used, state it in the report header. For arXiv reports, record whether the review used new submissions, cross submissions, replacements, or another category.

### 4. Filter Against the Profile

Rank candidate papers by relevance to the active profile (per the precedence rule in step 1). The profile file is the only source for topic weighting — do not substitute or supplement it with hard-coded priority lists outside the profile. This keeps the README and this manual free of strategy content that would otherwise leak through any public fork.

### 5. Write the Report

Save reports in the appropriate year folder. Keep the report readable as a standalone snapshot: a reader should be able to understand the coverage, ranking logic, and source depth without opening previous reports.

### 6. Rebuild the PDF

After creating or editing any `YYYY/arXiv_*.md` report, rebuild its PDF before considering the task finished.

Use:

```bash
./scripts/render_report_pdf.sh YYYY/arXiv_FILENAME.md
```

The output should be:

```text
YYYY/pdf/arXiv_FILENAME.pdf
```

Keep the PDF filename matched to the Markdown filename.

### 7. Verify the Output

At minimum:

- check that the Markdown file opens cleanly
- check that the PDF was created
- check PDF metadata with `pdfinfo` when available
- extract a few lines with `pdftotext` when available
- confirm that the report title, date coverage, and working-model line are present

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

It uses `pandoc` and `xelatex` to produce A4 PDFs with the repository's default font and margin settings.

Required command-line tools:

- `pandoc`
- `xelatex`

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

Use this checklist when updating the repository workflow:

- keep the public profile scaffold in `doc/template_research_profile.md`
- keep the operational working profile in ignored `doc/research_profile.md`
- keep deep private notes in ignored `doc/research_profile.local.md`
- keep dated reports in year folders
- keep PDF renders in `YYYY/pdf/`
- keep `*/pdf/` gitignored; publishing PDFs requires an explicit project decision
- update this manual when naming, formatting, or rendering conventions change
- recompile the matching PDF after every report create/update
- sync the public mirror after a report is finalized and committed, if the update should be public
- keep tracked docs and reports free of private information
