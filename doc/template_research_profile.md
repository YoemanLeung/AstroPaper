# Research Profile (Public Template)

This is the tracked, sync-safe template for the research profile. It names the broad topical scope of the repository so that forkers and casual readers can see the shape of a populated profile, but it intentionally does **not** encode specific priority ordering, method-recurrence patterns, or instrument preference rankings. Anything tracked here is published.

The agent treats this file as a **fallback**. When `doc/research_profile.md` is present (the user's customized working profile, gitignored), that file is authoritative and supersedes everything here for the duration of the session. See the README's "Standard Workflow" section for the full three-tier precedence rule.

Forkers: adapt the scope below to your own field if you are reusing this workflow, copy this file to `doc/research_profile.md` (gitignored), and populate that copy with your actual priorities, weightings, and survey preferences. Keep this tracked template free of research strategy.

## Scope

This repository tracks `arXiv astro-ph.GA` papers on the intersection of:

- high-redshift galaxy evolution
- the intergalactic medium (IGM) and circumgalactic medium (CGM)
- quasars, AGN, and their gas and galaxy environments
- large-scale structure: protoclusters, overdensities, filaments, and the cosmic web
- reionization and the high-redshift frontier, including extreme JWST-era populations
- galaxy morphology and structural evolution, where tied to environment or high-z context

## Tracers and Regimes

Observational tracers commonly used within the scope above include Lyman-alpha emitters, Lyman-break galaxies, quasars, HI absorption (Lyman-alpha forest and damped systems), tomographic reconstructions, emission-line galaxies, and dusty or compact red sources. The redshift range of interest spans cosmic noon through cosmic dawn.

## Methods

Broad methodological categories relevant to the reports include overdensity / environment mapping, galaxy-gas cross-correlations, absorption-based environment measures, stacking and matched-sightline analyses, SED fitting and stellar-population inference, emission-line and metallicity diagnostics, morphology and structural measurements, and survey feasibility work. This list is not ordered by recurrence or preference.

## Surveys and Facilities

Reports track science from major high-redshift and wide-field facilities, including but not limited to JWST, Roman, ALMA, and a range of optical / near-infrared spectroscopic and imaging surveys (DESI, PFS, and CLAMATO-like tomography among them). No priority ordering is implied by this list.

## Writing Style for Reports

Report format and style rules are defined in the repository README. Key points:

- Every paper in a thematic section is summarized using the five-field structured format: **Question**, **Data**, **Method**, **Conclusion**, **Position** (field labels in bold, nested bullets).
- `Data` and `Method` are subdivided by instrument and by analysis step, using the specific configurations and numbers from the body skim (not just the abstract).
- `Conclusion` states findings directly with the supporting evidence chain — `A is B, because [measurement from the paper]`. Quantities go inside backticks. No "the abstract argues / reports / favors / presents / interprets" or "the paper argues / reports / finds / pushes" hedges.
- `Position` places the paper in the broader field and prefers prior-work references the paper itself cites (recovered via the body skim). Agent-inferred citations are capped at two or three and only wear the `Position (inferred):` tag when every reference on the line is agent-inferred rather than skim-derived.
- Content source: arXiv abstract plus a targeted HTML fetch of `https://arxiv.org/html/<arxivId>` for the papers that get structured thematic-section summaries. PDF fallback (via `pdftotext` or an agent-native PDF reader) when HTML is not available. Abstract-only is a last resort; if used, mark it in the report header.
- See the README sections "Per-paper summary format" and "Content sources and skim workflow" for the canonical example, the standard extraction prompts, and the full rule list.
