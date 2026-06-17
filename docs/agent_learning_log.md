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


## 2026-06-17 — Lesson 8: Data & GIS Agent, schema before data

Phase B started with a Data & GIS Agent task. The first hotspot layer will be country-level, not raster-level. A country-level dataset is reproducible, small enough for GitHub Pages and sufficient to add a real hotspot layer to the portfolio prototype.

Agent lesson: define target dataset, variables, units, sources, licence constraints and publication boundary before fetching data.
