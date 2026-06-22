# B15c — Bind Global Peatland Map 2.0 Context Images to Sticky Story

Date: 2026-06-18

## Purpose

Replace the planned global and Europe peatland-context placeholders in the sticky-scroll story with exported image layers from Global Peatland Map 2.0.

## Inputs

- `public/images/gpm2_global_context.png`
- `public/images/gpm2_europe_context.png`

## Data source

Global Peatland Map 2.0, Greifswald Mire Centre / Global Peatland Database.

The downloaded README states:

- GeoTIFF projection: WGS 84
- values: `1 = peat dominated`, `2 = peat in soil mosaic`
- resolution: roughly 1 x 1 km
- dataset used for the Global Peatland Assessment 2022

## Website integration

Created:

- `src/gpm2_context_images.js`

Modified:

- `index.html`
- `src/styles.css`

## Interpretation boundary

The GPM 2.0 images are context layers. They show where peat-dominated areas and peat-in-soil-mosaic areas occur globally and in Europe. They are not local rewetting suitability maps and should not be interpreted as site-level planning layers.

## Story role

The images support the transition from global peatland extent to drained-organic-soil emissions hotspots, and then to Germany/Baden-Württemberg implementation constraints.
