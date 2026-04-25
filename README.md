# AstroPaper

A rolling reading log of `arXiv astro-ph.GA` papers — weekly reviews and occasional daily snapshots on high-redshift galaxies, the IGM/CGM, quasar environments, cosmic-web structure, reionization, and related topics. Reports live under [`2026/`](2026/); the most recent weekly review is [`2026/arXiv_20260417w.md`](2026/arXiv_20260417w.md). New reports arrive on a rolling cadence, primarily weekly with occasional daily snapshots; older years will accumulate under sibling `YYYY/` folders as the log grows.

Reports are drafted by an LLM coding agent (Claude Code, Codex CLI, GPT with browsing, or similar) following the structured workflow documented in [`doc/agent_workflow.md`](doc/agent_workflow.md). That workflow is the repo's secondary artifact: a prompt-driven template other researchers can fork to build their own reading logs for any arXiv category or paper feed.

**Disclaimer:** these are reading notes, not peer-reviewed summaries. Verify against the original papers before citing or reusing any scientific claim.

> **Agents running this workflow:** before producing a report, read [`doc/agent_workflow.md`](doc/agent_workflow.md) — it is the full operational manual (repository layout, cadence encoding, report structure, per-paper summary format, source/skim priority, writing style).

## Quick Start

You do three things. The agent handles the rest.

1. **Set it up once.** Copy `doc/template_research_profile.md` to `doc/research_profile.md`, then rewrite it to describe what *you* want to read. That local file is what the agent reads each session. It is gitignored, so your real priorities stay local. PDF production requires `pandoc` and `xelatex`; ask your agent to help install or configure them if needed.

2. **Ask.** In an LLM coding agent with web access (Claude Code, Codex CLI, or similar) that has this repo as its working directory, drop a short request like:

   ```text
   check the papers from last week
   ```

   The agent reads the README, follows the pointer to `doc/agent_workflow.md`, picks a sensible date window, scans `arXiv astro-ph.GA`, ranks the hits against your profile, and writes a fresh `YYYY/arXiv_*.md` in the documented format. This can be made automatic by putting it into a routine.

3. **Render.** If the agent can run shell it will produce the PDF itself. Otherwise do it by hand:

   ```bash
   ./scripts/render_report_pdf.sh YYYY/arXiv_FILENAME.md
   # → YYYY/pdf/arXiv_FILENAME.pdf
   ```

## For reusers

To fork this repo and build your own reading log in any field:

- Read [`doc/agent_workflow.md`](doc/agent_workflow.md) for the full operational manual.
- Start from [`doc/template_research_profile.md`](doc/template_research_profile.md) — copy it to `doc/research_profile.md` (gitignored) and rewrite the scope for your field.
- The three-tier profile stack (template / working / archive), filename conventions, per-paper summary format, source/skim priority, and writing style are all documented in the manual.

## License

Dual-licensed. Workflow, scripts, and templates are MIT-licensed; the dated reports under `YYYY/` are released under Creative Commons Attribution 4.0 International (CC BY 4.0). See [LICENSE](LICENSE) for details.

## Acknowledgments

- Report drafting uses the model disclosed in each report's `Working model:` header line.
- Repository scaffolding, README polish, and public-release preparation were AI-assisted.
