# Saatwik Sairaam Vasamsetti — Portfolio

A single-file personal portfolio: one `index.html` carrying the markup, the
styles and the canvas animation, with no build step, no framework and no
runtime dependencies. Open the file and it runs.

**Built by Saatwik Sairaam Vasamsetti** · [github.com/saatwik-1157](https://github.com/saatwik-1157)

## Why one file

A portfolio is read once, quickly, usually on a phone, often on a bad
connection. Every dependency is a request that can fail before the page paints.
Keeping the whole site in one document means:

- **One request** for everything above the fold — no CSS or JS round-trip.
- **Nothing to build.** No toolchain to re-learn a year from now when a
  recruiter asks for an update and the Node version has moved on twice.
- **Nothing to break.** No package can be yanked, deprecated or CVE'd out from
  under a static page that imports nothing.

The cost is a 674-line HTML file. That is the trade, made deliberately.

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

Also bundled: `Saatwik-Vasamsetti-Resume.pdf`, `Saatwik-Vasamsetti-CV.pdf` and
`Saatwik-Internship-Toolkit.pdf`, linked from the page so a visitor can leave
with the document rather than a screenshot.

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
Saatwik-Vasamsetti-Resume.pdf   linked from #contact
Saatwik-Vasamsetti-CV.pdf
Saatwik-Internship-Toolkit.pdf
```

## Optional intro video

The hero supports a video layer behind the canvas. It ships disabled because
the repo carries no video. To enable it, drop a file at `assets/intro.mp4` and
uncomment the `<video>` element in the hero section of `index.html`.

## License

Personal portfolio content — code is free to learn from, the written content,
imagery and documents are not for reuse.
