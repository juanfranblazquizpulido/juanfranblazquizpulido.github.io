# Juan Francisco Blázquiz Pulido — academic website

Read [EDITING_GUIDE.md](EDITING_GUIDE.md) for detailed page-by-page editing instructions, file mappings and examples.

## Build and preview

Run these commands inside this site folder (Python 3.10+; no external packages):

```sh
python build.py
python verify.py
python -m http.server 8765 --bind 127.0.0.1 --directory dist
```

Open http://127.0.0.1:8765/. If the server is already running, rebuild and refresh.

## Contents

All five pages retain the academic content migrated from Google Sites, including both abstracts, four projects in progress, all 23 conferences, seminars, five courses, the local CV and both institutional addresses and emails. Social profiles now include X, Bluesky, LinkedIn, Google Scholar, GitHub, ORCID and ResearchGate.

## Local photos

- Home: Explanada (explanada-castillo.jpg).
- Research: thesis defence (research-defense.jpg).
- Teaching: blackboard (pizarra.png), fitted without cropping.
- CV: UA (ua-mano.jpg).
- Contact: Alicante castle and rainbow (alicante-castillo.jpg).
- Portrait and header: BlazquizJ.jpg.

All photos and icons are local. Unused photos are retained in public/assets/ and copied into dist/assets/ on every build. Original files are unmodified; CSS controls cropping.

## Editing

- build.py: layout, headings, paper metadata, teaching entries, contact information and footer.
- content/inicio.json and content/research.json: migrated paragraphs used in the pages.
- content/images.json: photo assignments.
- content/socials.json: profile order, names, links and icons.
- custom.css: readable personal style overrides, including image focal positions.
- styles.css: base styles.
- public/assets/: photos, icons and PDF.
- dist/: generated output; do not edit directly.

Search build.py for HOME_HERO_TAGLINE to restore or replace the commented optional text above the name.

## Publication status

The website is not published yet. The organisation juanfranblazquizpulido has been created, administered through juanfranbp4. Repository creation and GitHub Pages publication remain pending.

For juanfranblazquizpulido.github.io, the organisation must own a public repository named juanfranblazquizpulido.github.io. Upload this site folder's contents to its root, including .github/workflows/pages.yml. Set Settings > Pages > Source to GitHub Actions. The workflow builds and deploys dist/ when main changes.

The source and stored assets will be public under this free setup. No credentials or tracking code are included. Migration audit files and one-off editing scripts remain outside this publishable folder.
