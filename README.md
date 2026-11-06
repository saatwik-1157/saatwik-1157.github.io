# Saatwik Sairaam Vasamsetti — Portfolio

A personal portfolio with no build step and no framework: `index.html` carries
the content and base styles, and `assets/agentic.js` and `assets/agentic.css`
add the motion. The only external request is Google Fonts, and the page falls
back to system fonts without it.

The page is assembled in front of the visitor by a team of animated cursors.
Scrolling, tapping or pressing a key skips the intro, "Agents off" stops the
motion, and `prefers-reduced-motion` turns it off entirely.

**Built by Saatwik Sairaam Vasamsetti** · [github.com/saatwik-1157](https://github.com/saatwik-1157)

## Why no build step

A portfolio is read once, quickly, usually on a phone, often on a bad
connection. With no toolchain and no packages, there is nothing to re-learn when
a recruiter asks for an update, and nothing that can be deprecated out from
under a static page. All the text lives in `index.html`, so the page is complete
even if the motion files fail to load.

## What's on the page

| Section      | What it covers                                                    |
| ------------ | ----------------------------------------------------------------- |
| Hero         | Role, summary and primary calls to action                         |
| `#about`     | Background, approach and skills                                   |
| `#flagships` | Trade Research and the other main projects, with measured results |
| `#matrix`    | Smaller projects, filterable by type                              |
| `#record`    | Experience and credentials                                        |
| `#contact`   | Direct contact routes                                             |

Also bundled: `Saatwik-Vasamsetti-Resume.pdf` and `Saatwik-Vasamsetti-CV.pdf`,
linked from the page so a visitor can leave with the document rather than a
screenshot.

These two PDFs are build output. Their content lives in `resume/data.py` and is
rendered by `python resume/build.py resume .` (see
[resume/README.md](resume/README.md)). The build embeds Calibri, so it needs a
Windows machine or that font installed.

## Run it

```bash
python -m http.server 8000
```

Then open <http://localhost:8000>. Opening `index.html` directly from the
filesystem also works — nothing on the page needs an origin.

## Deploy

Any static host serves this as-is: GitHub Pages, Netlify, Vercel, Cloudflare
Pages. There is no build command and no output directory — publish the repo
root.

## Layout

```
index.html                      the entire site
index-classic-backup.html       previous design, kept for reference
og-image.png                    social preview card
assets/saatwik.jpg              portrait
Saatwik-Vasamsetti-Resume.pdf   linked from #contact — built from resume/
Saatwik-Vasamsetti-CV.pdf                              — built from resume/
Saatwik-Internship-Toolkit.pdf
resume/data.py                  résumé and CV content
resume/build.py                 renders both PDFs
```

## Optional intro video

The hero supports a video layer behind the canvas. It ships disabled because
the repo carries no video. To enable it, drop a file at `assets/intro.mp4` and
uncomment the `<video>` element in the hero section of `index.html`.

## License

Personal portfolio content — code is free to learn from, the written content,
imagery and documents are not for reuse.
