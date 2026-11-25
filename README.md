# RepairLab


## Project status

Implemented: local interface, three repair prompts, deterministic record matching, selectable candidates, candidate rejection, confirmation, correction, stopping, one-step undo, event export and automated checks.

Simulated: appointments, ambiguous interpretation and deliberately incomplete candidate coverage. Interpretation uses lexical rules; there is no trained language model, probability estimate, semantic ranking or provider API. The prototype demonstrates the interaction around an intelligent component rather than claiming general language understanding.

Not implemented: speech, booking, authentication, persistent storage, live integrations or user research. Refresh and changes to strategy or coverage reset the session.

## Run or inspect

Open `index.html` in a modern browser; no installation, API key, paid service or server is required. Alternatively use a local static server:

```console
python -m http.server 8766 --bind 127.0.0.1
```

Then open `http://127.0.0.1:8766`.

Tests need Node.js with its built-in test runner, without npm installation:

```console
node --test tests/core.test.cjs
node scripts/replay.cjs
```

## Walkthroughs

1. Choose Candidate options, then An ambiguous request. Select Dental check, review the interpretation, confirm and undo; the status returns to Active.
2. Click Intention missing from options. Imagine intending Friday physiotherapy. Choose None of these, type Friday and send. Review A103 before confirming; the other records remain active.
3. Reset. Send Cancel dental, choose Go back and correct, then send eye. Confirm only the eye appointment.
4. Select General repetition or Targeted question and send the same ambiguous request to inspect the different repair prompts. These settings are demonstrations, not experimental results.

## Architecture and technology

HTML and CSS provide the browser interface. `app.js` renders DOM state and binds controls. `core.js` owns interpretation, repair policy, session state, record validation and actions; Node imports the same module for tests. All data is fictional and held in memory. No outgoing requests are made by the application.

## Development record

- `bf5d947`: implemented the bounded controller and 25 behavioural checks before building the interface.
- `cf29515`: added the schedule, conversation, strategy selection, omission demo, confirmation and recovery controls.
- `33ae597`: recorded reproducible replays, citation boundaries and an actual browser screenshot.
- Week 4 revision: checked L10-L12 and added session-lifetime, exact-lookup and execution-boundary rationale; prototype behaviour unchanged.
- Subsequent commits add documentation, report assets and verification records; use `git log --oneline` to inspect the actual history. Commits identify Codex-assisted development rather than attributing unperformed work to the student.

The shared core keeps prompt comparisons from silently changing action logic. The report narrows the earlier broad superiority question to inspectable correction and cancellation boundaries. Teacher rubric screenshots prompted explicit context, source-to-claim checks and a clear contribution; they did not identify specific suspect references.

## Evidence and limits

`evidence/test-results.txt` records 25 passing automated checks. `evidence/scenario-replays.json` contains five deterministic traces, not participant responses. `evidence/browser-checks.txt` records UI walkthroughs. `docs/source-audit.txt` links each report claim to an original source and its boundary. Report word counts are generated from source, including status-table text.

No evidence here establishes lower cognitive load, greater satisfaction or superior repair performance. The schedule is visible in every condition. Omission is configured, ranking is fixed, lexical interpretation is limited, and only the latest cancellation can be undone.

## AI assistance

OpenAI Codex conducted functional checks and browser tests based on the research topics selected by the students and the brief descriptions provided. The project therefore combines the student’s topic selection and supplied context with AI-assisted development and writing. It conducted an automatic check and browser demonstration, verified the original paragraphs cited, and modified the relevant statements to distinguish between implementation and simulation.The automated checks demonstrate specified system behaviour, not findings from a participant study.

## Submission and publication

The report is in `docs/Assignment_2_Project_Report_GitHub.docx` and its PDF counterpart; these GitHub files are the current report, superseding the original version. Architecture, storyboards and an interface screenshot are in `docs/`. Source files and evidence belong in the public repository; no separate ZIP submission is needed when they are there.

Repository: https://github.com/jn8t9zw27v-arch/repairlab

README: https://github.com/jn8t9zw27v-arch/repairlab/blob/main/README.md

Submission version: `v1.2.0`. Inspect that immutable snapshot at https://github.com/jn8t9zw27v-arch/repairlab/tree/v1.2.0 after upload. Use `Publish_To_GitHub.cmd` or `git push -u origin main --tags` from this checkout, completing normal GitHub sign-in if requested. Verify public access before submission. No API keys are used or required.
