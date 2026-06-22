\# B63 – Story and Project Audit



Date: 2026-06-22

Scope: Peatland Transition Atlas current page structure, asset use, story flow and cleanup priorities after successful BW/BK50 integration.



\## 1. Current state



The atlas now contains a functioning central PNG-based sticky-scroll story from global peatland extent and emission pressure to Europe, Germany / Thuenen Kulisse and Baden-Wuerttemberg / BK50 peat and wetland soil context.



The current page also still contains older prototype sections and GeoJSON-driven story components. These are not necessarily wrong, but they currently compete with the new central story instead of clearly supporting it.



The main structural issue is that the page tells the scale-transition story more than once:



1\. A conceptual framing block.

2\. An older guided scroll story.

3\. The new central PNG-based sticky-scroll map story.

4\. Later evidence, hotspot, pathway and method sections.



The new central map story should become the narrative spine of the page.



\## 2. Recommended narrative spine



The atlas should follow this sequence:



1\. Framing: peatland transition as a spatial and systemic problem.

2\. Conceptual logic: Extent -> Pressure -> Implementation -> Pathways.

3\. Main atlas story: global -> Europe -> Germany -> Baden-Wuerttemberg.

4\. Pathway interpretation: what spatial pressure implies for feasible transition pathways.

5\. Evidence explorer: supporting country-level hotspots, case evidence and pathway examples.

6\. Method and data: limitations, interpretation boundary and prototype datasets.



\## 3. KEEP



Keep these elements as core structure:



\* `hero`

\* `transitionLogic`

\* `centralGlobalMapStory`

\* `pathwayEvidenceMatrix`

\* `methodology`

\* `data`



Rationale:



\* `hero` provides the main thesis.

\* `transitionLogic` gives the conceptual chain: Extent -> Pressure -> Implementation -> Pathways.

\* `centralGlobalMapStory` is now the strongest visual and narrative component.

\* `pathwayEvidenceMatrix` is the logical transition from spatial context to plausible transition options.

\* `methodology` and `data` are needed to keep the prototype scientifically transparent.



\## 4. ADAPT



Adapt these elements, but do not remove them immediately:



\### `story`



The current "Six-part story" block should either be removed or merged into `transitionLogic`. It creates an additional introductory layer before the actual story begins.



Recommendation: remove or strongly compress.



\### `layerProvenance`



This section is useful, but currently interrupts the story. It should become a compact "How to read the map layers" note directly before or after the central map story.



Recommendation: keep, shorten and reposition.



\### `hotspots`



The country-level hotspot map and rankings are useful, but should no longer behave like a second main story.



Recommendation: reframe as "Evidence Explorer: country-level pressure".



\### `map`, `pathways`, `fit`



These sections are useful supporting modules, but need clearer grouping.



Recommendation: combine under a broader section such as "From spatial pressure to transition hypotheses".



\## 5. DEACTIVATE FIRST



\### `guidedStory`



This is the strongest candidate for first deactivation.



Reason:



\* It uses a separate state system: `world-emissions`, `global-peat`, `europe`, `germany`, `bw`, `boundary`.

\* It duplicates the same scale movement now handled more clearly by `centralGlobalMapStory`.

\* It creates narrative redundancy before the strongest part of the page.



Recommendation for B64:



\* Do not delete.

\* Add a reversible retirement class, e.g. `is-retired`.

\* Hide via CSS.

\* Keep code and assets for now.



\## 6. REVIEW LATER



Review these after B64, but do not touch yet:



\* `bwPeatLayer`

\* `bw\_peat\_layer.js`

\* `gpm2\_context\_images.js`

\* `scrolly\_story.js`

\* `scrolly\_story\_layers.js`

\* `emissions\_metric\_scrolly.js`

\* GeoJSON-driven Germany/BW story layers

\* `public/images/gpm2\_global\_context.png`

\* `public/images/gpm2\_europe\_context.png`

\* `public/data/bw\_bk50\_moor\_simplified.geojson`

\* `public/data/germany\_organic\_soils\_simplified.geojson`



Reason:



Some of these may still support active sections. Removal should only happen after section-level deactivation and reference checks.



\## 7. DO NOT TOUCH



Do not modify these in the next cleanup phase:



\* `src/central\_global\_map\_story.js`

\* `src/central\_layer\_state\_hardener.js`

\* `src/central\_step\_state\_bridge.js`

\* `src/central\_stage\_label\_fix.js`

\* B62/BW state bindings

\* central PNG layer stack

\* `public/maps/global/`

\* `public/maps/europe/`

\* `public/maps/germany/`

\* `public/maps/bw/`



Reason:



These were just stabilized. The priority is story architecture, not further map-controller refactoring.



\## 8. Proposed B64 scope



B64 should be a reversible story-flow cleanup, not a deletion patch.



Recommended B64 title:



`B64\_cleanup\_story\_flow\_phase1`



Recommended scope:



1\. Hide `guidedStory` with a reversible class.

2\. Remove or compress the "Six-part story" block if it duplicates `transitionLogic`.

3\. Keep `transitionLogic` as the conceptual introduction.

4\. Make `centralGlobalMapStory` the main atlas story.

5\. Reframe lower sections as supporting evidence.

6\. Do not delete assets.

7\. Do not remove scripts.

8\. Do not alter the central map state controller.



\## 9. Proposed B65 scope



B65 should only happen after B64 is visually checked.



Recommended B65 title:



`B65\_legacy\_asset\_and\_script\_reference\_audit`



Recommended scope:



1\. Check which scripts are still required after `guidedStory` is hidden.

2\. Identify unused GeoJSON, PNG and JS files.

3\. Decide whether old interactive components are retained as explorer modules or retired.

4\. Update the QA script to include BW map PNGs and BW central states.



\## 10. Immediate next decision



Before B64, decide whether `story` / "Six-part story" should be:



A. removed entirely,

B. merged into `transitionLogic`, or

C. kept but shortened.



Recommendation: A or B. The current page already has enough framing. The central map story should start sooner.



