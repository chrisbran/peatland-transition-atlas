# B54 - Restore Original Thuenen Legend Colors

Date: 2026-06-19

## Issue

B53 added an extra floating Germany legend. This was not intended. The intended fix is to keep the existing central legend and only make sure that its color swatches are visible.

## Fix

- Remove the B53 script tag from `index.html`.
- Delete `src/germany_thuenen_legend_fix.js` if present.
- Remove the B53 custom legend CSS block from `src/styles.css`.
- Add B54 CSS rules that assign colors to the original `legend-thuenen-*` classes.

## Expected result

- No extra floating B53 Germany legend.
- The original central legend remains.
- The soil-type labels in the original legend now show their corresponding colors.
