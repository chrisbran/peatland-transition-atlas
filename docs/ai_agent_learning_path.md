# AI Agents Learning Path — Peatland Transition Atlas

This project is used as a practical learning environment for AI-agent workflows.

## Learning objective

You will learn how to use agentic workflows to manage a real data-visualisation project.

The goal is not full autonomy. The goal is supervised delegation:

```text
Human judgement + agent execution + QA gates
```

## Stage 0 — Manual agent simulation

This is where the project starts.

One assistant acts as different specialist agents:

- Orchestrator Agent
- Research & Evidence Agent
- Data & GIS Agent
- Visualization Engineer Agent
- Story & Editorial Agent
- QA & Critic Agent
- Release Agent

You learn the structure before using more autonomous tools.

## Stage 1 — File-based agent workflow

Each agent receives:

- role description,
- input files,
- output files,
- acceptance criteria,
- quality gates.

This repository now contains these definitions in `agents/`.

## Stage 2 — GitHub issue workflow

Convert tasks into GitHub issues:

- one issue per task,
- one agent role per issue,
- clear output files,
- acceptance criteria,
- human review.

Example issue title:

```text
A5 — Add methodology panel to static prototype
```

## Stage 3 — Tool-assisted coding

Use coding assistants or agentic developer tools to work on individual issues.

Human still reviews:

- code diff,
- rendered website,
- scientific claims,
- data licensing.

## Stage 4 — Semi-autonomous data workflows

Use scripts/notebooks to fetch, clean and document public data sources.

Agent responsibilities:

- propose code,
- run checks,
- update documentation,
- flag uncertainty.

Human responsibilities:

- approve source use,
- verify interpretation,
- approve publication.

## Stage 5 — Release workflow

Before each public release:

1. QA Agent audits the project.
2. Human lead resolves flagged issues.
3. Release Agent prepares README, release notes and GitHub Pages.
4. Human lead publishes.

## Core lesson

Agents are not replacements for responsibility.

They are useful when work can be decomposed into:

- clear inputs,
- clear outputs,
- explicit constraints,
- testable acceptance criteria.

## First learning exercise

Run Phase A task A1:

```text
Preview the prototype locally and report what works and what does not.
```

Then use the QA & Critic Agent prompt to audit the result.
