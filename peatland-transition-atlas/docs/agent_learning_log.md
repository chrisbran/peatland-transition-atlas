# Agent Learning Log

## 2026-06-16 — Lesson 1: First local preview and QA gate

### What happened

The Phase A prototype was downloaded, served locally and visually checked by the human lead.

### Result

The prototype rendered successfully:

- 21 papers
- 8 transition pathways
- 11 evidence regions
- six story sections
- evidence map
- transition pathway spectrum
- South Germany fit chart

### Agent lesson

This is the first example of a supervised agentic workflow:

```text
Agent prepares artefact → Human previews → QA Agent audits → next task is selected
```

The important point is that the human did not simply say "looks good" and release.  
The positive preview triggered a QA gate and a next improvement task.

### Next agent task

```text
A5 — Add methodology panel to static prototype
```

### Why this matters

The prototype is visually strong, but public-facing scientific visualisations need explicit caveats:

- qualitative scores are not measured values,
- evidence-map points are approximate anchors,
- South Germany transfer is a hypothesis,
- literature evidence is heterogeneous.


## 2026-06-16 — Lesson 2: Visualization Engineer Agent with acceptance criteria

### What happened

Task A5 was executed as a bounded Visualization Engineer Agent task.

### Input

- local QA report
- acceptance criteria
- static web prototype

### Output

- visible methodology panel
- score legend
- South Germany Fit legend
- typography refinements
- task report

### Agent lesson

A good agent task is small enough to verify.  
The agent did not redesign the entire project. It made a bounded improvement with clear acceptance criteria.

### Human review required

Preview the page locally and check:

- Method link works.
- Methodology panel appears before Data.
- Caveats are readable.
- The design still feels coherent.


## 2026-06-16 — Lesson 3: Story & Editorial Agent

### What happened

Task A2 was executed as a bounded Story & Editorial Agent task.

### Input

- `atlas_story_sections.json`
- screenshot-based human feedback
- Phase A QA report

### Output

- sharper section messages,
- shorter story-card text,
- revised storyboard,
- A2 story review report.

### Agent lesson

Editorial agents are most useful when they improve the structure of claims, not merely rewrite sentences.

The key improvement was the narrative arc:

```text
Hotspot → Water-table mechanism → International evidence → Transition spectrum → South Germany transfer → Modelling frontier
```

### Human review required

Preview the page and check whether the revised story cards are clearer and less text-heavy.


## 2026-06-16 — Lesson 4: Research & Evidence Agent

### What happened

Task A3 was executed as a Research & Evidence Agent task.

### Input

- `region_case_studies.geojson`
- `region_case_studies.csv`
- `papers.csv`
- QA concerns about false precision and over-transfer

### Output

- sharper evidence-region cards,
- added evidence-type metadata,
- added transfer-confidence metadata,
- added coordinate-precision metadata,
- A3 evidence review report,
- A6 follow-up task.

### Agent lesson

Research agents are not only for adding more sources. They are especially valuable for reducing overclaiming.

The key improvement was not more text, but better epistemic labelling:

```text
What kind of evidence is this?
How transferable is it?
How precise is the coordinate?
```

### Human review required

Preview the map cards after A6 so that the new metadata are visible in the interface.


## 2026-06-16 — Lesson 5: Simplification as an agentic skill

### What happened

Task A6 was corrected before implementation. The initial plan would have made too much internal QA metadata visible.

### Decision

Show only the metadata that helps the public reader:

```text
Evidence type
Transfer hypothesis
Main caveat
Supporting papers
```

Keep internal fields available for QA but out of the primary interface.

### Agent lesson

Agentic work can drift into detail. A good human lead stops the process and asks:

```text
Does this improve the user's understanding?
Or are we exposing our internal machinery?
```

This is an important governance function in AI-agent projects.


## 2026-06-16 — Lesson 6: Avoid unnecessary refinement

### What happened

Task A4 reviewed the transition scores.

### Decision

No score changes are required for Phase A.

### Agent lesson

A QA agent should not always create more work. Sometimes the correct conclusion is:

```text
Good enough for this release. Move on.
```

The goal is a public portfolio MVP, not a perfect scientific decision-support model.

### Next step

Prepare the GitHub publication package.


## 2026-06-16 — Lesson 7: Release Agent

### What happened

Task A7 prepared the GitHub publication package.

### Output

- public-facing README,
- CHANGELOG,
- GitHub release plan,
- project descriptions,
- Phase A release checklist,
- `.nojekyll` for GitHub Pages.

### Agent lesson

The Release Agent is not a coder. Its job is to reduce friction between a working prototype and public publication.

Release work asks:

```text
Can someone understand this in one minute?
Can the project be published safely?
Are limitations visible?
Are next steps clear?
```

### Human action required

The next step is no longer agent work. The human lead should run a final local preview and publish the repository.
