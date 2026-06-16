# GitHub Repository Setup

## Option 1 — Browser upload

1. Go to GitHub.
2. Create a new repository:
   - Repository name: `peatland-transition-atlas`
   - Visibility: public, if intended as portfolio
   - Do not initialise with README if you upload this prepared folder.
3. Upload all files from this folder.
4. Commit to `main`.

## Option 2 — Command line

```bash
cd peatland-transition-atlas
git init
git add .
git commit -m "Initial literature-driven Peatland Transition Atlas prototype"
git branch -M main
git remote add origin https://github.com/<your-username>/peatland-transition-atlas.git
git push -u origin main
```

## Enable GitHub Pages

1. Open repository on GitHub.
2. Go to **Settings → Pages**.
3. Under **Build and deployment**:
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/root`
4. Save.
5. Wait until GitHub publishes the site.

The URL will usually be:

```text
https://<your-username>.github.io/peatland-transition-atlas/
```

## Recommended repository settings

### About section

Description:

```text
Interactive data-visualisation prototype on peatland rewetting, GHG mitigation and transition-compatible land-use pathways.
```

Topics:

```text
data-visualization
peatlands
rewetting
paludiculture
climate-mitigation
agriculture
scrollytelling
d3
geojson
```

## Commit strategy

Use small, meaningful commits:

```bash
git add data/processed/papers.csv public/data/papers.csv
git commit -m "Add curated literature evidence dataset"

git add data/processed/transition_pathways.csv public/data/transition_pathways.csv
git commit -m "Add transition pathway coding"

git add index.html src/
git commit -m "Add static atlas prototype"
```

## Do not commit

- copyrighted PDFs
- large raw raster files
- personal/project-sensitive PALUD/RoGeR data
- credentials or API keys
- unpublished partner data
