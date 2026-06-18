# B17b — Force Insert Pathway Evidence Matrix

Date: 2026-06-18

## Problem

A previous B17 script checked for `id="pathwayMatrix"` before inserting the new section. The page already had an existing placeholder/div with this ID:

`<div id="pathwayMatrix" class="matrix"></div>`

Therefore the script skipped insertion.

## Fix

This patch inserts the new evidence section with a non-conflicting ID:

`#pathwayEvidenceMatrix`

## Purpose

Connect literature-derived transition pathways to the spatial storyline:

- wet grazing,
- paludiculture biomass,
- water management,
- governance and adoption.

Each pathway is described through spatial signal, evidence role, constraint and data gap.
