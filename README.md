# Saatwik Sairaam Vasamsetti — Portfolio

A single-file personal portfolio: one `index.html` carrying the markup, the
styles and the canvas animation, with no build step and no framework. The
only external request is Google Fonts, and the page falls back to system fonts
without it. Open the file and it runs.

Live at **<https://saatwik-1157.github.io/>** (GitHub Pages user site).

**Built by Saatwik Sairaam Vasamsetti** · [github.com/saatwik-1157](https://github.com/saatwik-1157)

## Why one file

A portfolio is read once, quickly, usually on a phone, often on a bad
connection. Every dependency is a request that can fail before the page paints.
Keeping the whole site in one document means:

- **One request** for the page itself — no separate CSS or JS round-trip.
- **Nothing to build.** No toolchain to re-learn a year from now when a
  recruiter asks for an update and the Node version has moved on twice.
- **Nothing to break.** No package can be yanked, deprecated or CVE'd out from
  under a static page that imports nothing.

The cost is a single HTML file of roughly 740 lines. That is the trade, made
deliberately.

## What's on the page

| Section       | What it covers                                                   |
| ------------- | ---------------------------------------------------------------- |
| Hero          | Animated canvas background, role, primary calls to action         |
| `#about`      | Short professional summary                                        |
| `#skills`     | Languages, frameworks and tooling                                 |
| `#projects`   | Selected work with links to the live sites and source             |
| `#experience` | Roles and what was actually shipped in each                       |
| `#certs`      | Certifications                                                    |
| `#contact`    | Direct contact routes                                             |

Also published: `Saatwik-Vasamsetti-Resume.pdf` and `Saatwik-Vasamsetti-CV.pdf`,
linked from the page so a visitor can leave with the document rather than a
screenshot.

The first two are build output, not hand-made files. Their content lives in
`resume/data.py` and is rendered by `python resume/build.py` — see
[resume/README.md](resume/README.md).

## Preview locally

From the repository root:

```bash
python -m http.server 8500
```

Then open <http://localhost:8500>. Opening `index.html` directly from the
filesystem also works — nothing on the page needs an origin.

## Deploy

This repository is the GitHub Pages user site for `saatwik-1157`, so
**deploying is pushing to `main`**. Pages serves the repository root as-is at
<https://saatwik-1157.github.io/>; there is no build command, no workflow and
no output directory.

Because the site is served straight from the root, **file paths are public
URLs**. `index.html`, the two PDFs, `og-image.png` and `assets/` are linked
from the page, from the social-preview meta tags and possibly from résumés
already sent out, so do not rename or move them.

If the résumé content changes, rebuild the PDFs before pushing (see
[resume/README.md](resume/README.md)).

## Project structure

```
saatwik-1157.github.io/
├── index.html                      the entire site (markup, styles, script)
├── og-image.png                    social preview card (og:image / twitter:image)
├── assets/
│   └── saatwik.jpg                 portrait
├── Saatwik-Vasamsetti-Resume.pdf   linked from the page — built from resume/
├── Saatwik-Vasamsetti-CV.pdf       linked from the page — built from resume/
├── resume/
│   ├── data.py                     résumé and CV content
│   ├── build.py                    renders both PDFs (reportlab)
│   └── README.md
├── .gitattributes                  marks PDFs and images binary
├── .gitignore
└── README.md
```

Two files may exist in a local checkout but are git-ignored and never
published: `index-classic-backup.html` (the previous design, kept locally for
reference) and `Saatwik-Internship-Toolkit.pdf` (personal planning notes).

**Tech:** HTML5, CSS3, vanilla JavaScript (canvas animation); Python +
reportlab for the PDF build.

## Optional intro video

The hero supports a video layer behind the canvas. It ships disabled because
the repo carries no video. To enable it, drop a file at `assets/intro.mp4` and
uncomment the `<video>` element in the hero section of `index.html`.

## License

Personal portfolio content — code is free to learn from, the written content,
imagery and documents are not for reuse.
