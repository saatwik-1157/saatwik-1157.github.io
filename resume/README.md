# Résumé & CV source

The two PDFs at the repo root are build output. This directory is the source.

```
resume/data.py     all the content — one Python module, no templating language
resume/build.py    the renderer (reportlab)
```

## Regenerate

```bash
pip install reportlab
python resume/build.py
```

It writes `Saatwik-Vasamsetti-Resume.pdf` and `Saatwik-Vasamsetti-CV.pdf` into
the repo root, where `index.html` already links them. Nothing else needs
touching.

## Why a script and not a Word file

The previous PDFs had no source at all — updating a line meant rebuilding the
whole document by hand, and the résumé and the CV drifted apart because the same
fact lived in two places. Here both documents read `data.py`, so a project
description is written once and appears correctly in both.

The build also enforces length, because that is the rule everyone means to
follow and nobody checks:

- the résumé must be **one page** — `build.py` shrinks the body size through a
  ladder of steps and raises `SystemExit` if it still spills at 8.2 pt;
- the CV must be **three pages or fewer**, on the same principle.

If a build fails, the fix is to cut content in `data.py`, not to raise the cap.

## How the two documents differ

Both read the same data; each takes a different slice of it.

| | Résumé | CV |
| --- | --- | --- |
| Projects | four, `"resume": True` | all, `"cv": True` |
| Project bullets | `resume_bullets` — one line each, capped at 3 | full `bullets` |
| Skills | `SKILLS_RESUME`, five lines | `SKILLS`, seven lines |
| Coursework | omitted | listed |
| Opening paragraph | `RESUME_SUMMARY`, three lines | `SUMMARY`, longer |
| Page footer | none | name and page number |
| Achievements | folded into the last `CERTIFICATIONS_RESUME` line | full `ACHIEVEMENTS` list |

To move a project onto the résumé, set `"resume": True` and give it a
`resume_bullets` list. Expect to take something else off — the page is full.

## Design

Black and white, no colour anywhere. Hierarchy comes from weight, size and
rules rather than hue, and the only greys are for dates and stack lines — they
photocopy and fax as grey rather than turning muddy. Verified per document: no
text span renders with `r != g != b`.

The phone, email, GitHub, LinkedIn and portfolio entries in the header are
still real hyperlinks, as are the repository lines under each CV project —
they simply render black now, so a reader on a laptop can open the code from
the document while a printed copy loses nothing.

Both files stay plain text under the hood, so an applicant tracking system
parses them: no images, no text in tables that carry meaning, no columns
running through the body.

## Keeping the numbers true

Every figure in `data.py` — 636 assertions, 64 routes, mAP50 0.471, 117 commits
— was measured in the repository it describes, and the command that produces it
is documented there. When a project moves, update this file too. A résumé that
disagrees with its own source repo is the failure mode RoadAssist's claims gate
exists to prevent, and it is worse here, because the reader is an interviewer
with the repository open.

Certification entries are transcribed from the PDFs in the certificates
archive, not from memory.
