# Data Analytics E-Portfolio

This repository contains my Data Analytics e-Portfolio. The site records my learning, project work, discussion activities and reflection across the module.

It uses plain HTML, CSS and a small amount of JavaScript so the same files can run on GitHub Pages or from an offline copy.

## Open locally

Open `index.html` in a web browser. All links use relative paths so the copied or unzipped site should continue to work.

## Site structure

- `index.html` — portfolio overview
- `learning-journey.html` — evidence from Units 1–12
- `discussions.html` — collaborative discussion work
- `project.html` — database analytics project
- `reflection.html` — critical reflection
- `references.html` — Harvard-style reference list
- `assets/` — supporting images, documents and unit artefacts

The portfolio is being updated as the module progresses. Source and row-level datasets, generated database files, and the supplied course workbook are retained locally rather than included in this repository. The site presents selected results, scripts, audit summaries, and integrity-test evidence instead.

## Publishing safely

Do not ZIP or drag-and-drop this entire working directory. It contains a `.git` directory and local source files, including row-level CSVs, a course workbook and a SQLite database. `.gitignore` prevents Git from tracking those files, but does not exclude them from a manual upload or ZIP.

Create a separate publish copy containing only the six HTML pages, `css/`, `js/`, and the selected linked evidence under `assets/`. Include the two Unit 6 ERD images, which are used by the site but are not currently tracked by Git. Check the publish copy's links and images before uploading it or creating the compressed working copy for submission.
