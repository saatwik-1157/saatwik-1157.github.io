# -*- coding: utf-8 -*-
"""Render Saatwik-Vasamsetti-Resume.pdf and Saatwik-Vasamsetti-CV.pdf.

    python resume/build.py

Content comes from resume/data.py; nothing is typed into a PDF by hand. The
resume is held to one page and the build fails loudly if it spills, because a
two-page "one-page resume" is the kind of thing nobody notices until a recruiter
does.

Output is deterministic — the same content always produces byte-identical
PDFs — so `git status` after a rebuild tells the truth about whether anything
actually changed.

Requires: pip install reportlab
"""

import os
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)  # repo root -- index.html links the PDFs from there

INK = colors.HexColor("#14161A")     # body text
MUTED = colors.HexColor("#4A5159")    # dates, stack lines
ACCENT = colors.HexColor("#1B3A5F")   # name, section headings, links
RULE = colors.HexColor("#1B3A5F")


# --- styles -------------------------------------------------------------------

def styles(size):
    """Build the stylesheet at a given body size so the resume can be squeezed."""
    lead = size + 2.2
    return {
        "name": ParagraphStyle(
            "name", fontName="Helvetica-Bold", fontSize=21, leading=24,
            alignment=TA_CENTER, textColor=ACCENT, spaceAfter=1,
        ),
        "title": ParagraphStyle(
            "title", fontName="Helvetica-Bold", fontSize=size + 0.6, leading=lead + 1,
            alignment=TA_CENTER, textColor=MUTED, spaceAfter=3,
        ),
        "contact": ParagraphStyle(
            "contact", fontName="Helvetica", fontSize=size - 0.3, leading=lead,
            alignment=TA_CENTER, textColor=INK,
        ),
        "section": ParagraphStyle(
            "section", fontName="Helvetica-Bold", fontSize=size + 1.1,
            leading=size + 3, textColor=ACCENT, spaceBefore=4, spaceAfter=1.2,
        ),
        "entry": ParagraphStyle(
            "entry", fontName="Helvetica-Bold", fontSize=size + 0.2, leading=lead,
            textColor=INK,
        ),
        "lead": ParagraphStyle(
            "lead", fontName="Helvetica", fontSize=size, leading=lead + 0.4,
            textColor=INK, alignment=TA_JUSTIFY, spaceAfter=1,
        ),
        "entryright": ParagraphStyle(
            "entryright", fontName="Helvetica-Oblique", fontSize=size - 0.3,
            leading=lead, textColor=MUTED, alignment=2,
        ),
        "sub": ParagraphStyle(
            "sub", fontName="Helvetica-Oblique", fontSize=size - 0.3, leading=lead,
            textColor=MUTED,
        ),
        "body": ParagraphStyle(
            "body", fontName="Helvetica", fontSize=size, leading=lead,
            textColor=INK, alignment=TA_JUSTIFY,
        ),
        "bullet": ParagraphStyle(
            "bullet", fontName="Helvetica", fontSize=size, leading=lead,
            textColor=INK, leftIndent=10, bulletIndent=1, spaceAfter=0.8,
            alignment=TA_JUSTIFY,
        ),
    }


# --- small builders -----------------------------------------------------------

def link(text, href):
    """A hyperlink the reader can actually click in the PDF."""
    return '<link href="%s" color="#1B3A5F">%s</link>' % (href, text)


def header(st, p, with_title):
    out = [Paragraph(p["name"], st["name"])]
    if with_title:
        out.append(Paragraph(p["title"], st["title"]))
    sep = " &nbsp;&#124;&nbsp; "
    line1 = sep.join([
        p["location"],
        link(p["phone"], p["phone_url"]),
        link(p["email"], p["email_url"]),
    ])
    line2 = sep.join([
        link(p["github"], p["github_url"]),
        link(p["linkedin"], p["linkedin_url"]),
        link(p["site"], p["site_url"]),
    ])
    out.append(Paragraph(line1, st["contact"]))
    out.append(Paragraph(line2, st["contact"]))
    out.append(Spacer(1, 1.5))
    return out


def section(st, heading):
    return [
        Paragraph(heading.upper(), st["section"]),
        HRFlowable(width="100%", thickness=0.8, color=RULE,
                   spaceBefore=0, spaceAfter=2.8),
    ]


def row(st, left, right, width):
    """One line with a bold left side and an italic right-aligned date."""
    if not right:
        return Paragraph(left, st["entry"])
    t = Table(
        [[Paragraph(left, st["entry"]), Paragraph(right, st["entryright"])]],
        colWidths=[width * 0.735, width * 0.265],
    )
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def bullets(st, items):
    return [Paragraph(b, st["bullet"], bulletText="•") for b in items]


def education(st, width, courses=True):
    out = []
    for e in data.EDUCATION:
        out.append(row(st, e["school"], e["dates"], width))
        if e["degree"]:
            out.append(row(st, "<i>%s</i>" % e["degree"], e["detail"], width))
        if e["courses"] and courses:
            out.append(Paragraph("<b>Coursework:</b> " + e["courses"], st["sub"]))
        out.append(Spacer(1, 1.5))
    return out


def skills(st, items=None):
    items = data.SKILLS if items is None else items
    return [Paragraph("<b>%s:</b> %s" % (k, v), st["body"]) for k, v in items]


def projects(st, width, key, max_bullets=None):
    out = []
    for p in data.PROJECTS:
        if not p.get(key):
            continue
        head = [row(st, p["name"], p.get("dates"), width)]
        if p.get("stack"):
            head.append(Paragraph("<b>Stack:</b> " + p["stack"], st["sub"]))
        bs = p.get("resume_bullets") if key == "resume" and p.get("resume_bullets") else p["bullets"]
        if max_bullets:
            bs = bs[:max_bullets]
        made = bullets(st, bs)
        # A heading orphaned at the foot of a page is the only break worth forbidding.
        out.append(KeepTogether(head + made[:1]))
        out.extend(made[1:])
        if p.get("repo") and key == "cv":
            repo = p["repo"]
            text = link(repo, "https://" + repo) if repo.startswith("github.com/") else repo
            out.append(Paragraph(text, st["sub"]))
        out.append(Spacer(1, 2.5))
    return out


def experience(st, width, max_bullets=None, resume=False):
    out = []
    for e in data.EXPERIENCE:
        if resume and e.get("resume") is False:
            continue
        out.append(row(st, "%s — %s" % (e["role"], e["org"]), e["dates"], width))
        bs = e["bullets"][:max_bullets] if max_bullets else e["bullets"]
        out.extend(bullets(st, bs))
        out.append(Spacer(1, 2))
    return out


def two_column_list(st, items, width):
    half = (len(items) + 1) // 2
    left, right = items[:half], items[half:]
    right += [""] * (len(left) - len(right))
    rows = [
        [Paragraph("• " + a, st["body"]) if a else "",
         Paragraph("• " + b, st["body"]) if b else ""]
        for a, b in zip(left, right)
    ]
    t = Table(rows, colWidths=[width * 0.5, width * 0.5])
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (0, -1), 0),
        ("LEFTPADDING", (1, 0), (1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0.6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return [t]


# --- documents ----------------------------------------------------------------

def footer(canvas, doc):
    """Name on the left, page number on the right, below the bottom margin."""
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    y = doc.bottomMargin - 13
    canvas.drawString(doc.leftMargin, y, data.PROFILE["name"])
    canvas.drawRightString(doc.leftMargin + doc.width, y, "Page %d" % doc.page)
    canvas.restoreState()


def render(path, story_fn, size, margin, title, with_footer=False):
    doc = SimpleDocTemplate(
        path, pagesize=LETTER,
        leftMargin=margin, rightMargin=margin,
        topMargin=margin * 0.82, bottomMargin=margin * 0.7,
        title=title, author=data.PROFILE["name"], subject=data.PROFILE["title"],
        creator="resume/build.py",
        # Deterministic output: without this reportlab stamps a build timestamp
        # and a fresh document id, so rebuilding with no content change still
        # shows both PDFs as modified and invites a pointless commit.
        invariant=1,
    )
    width = doc.width
    st = styles(size)
    if with_footer:
        doc.build(story_fn(st, width), onFirstPage=footer, onLaterPages=footer)
    else:
        doc.build(story_fn(st, width))
    return doc.page


def resume_story(st, width):
    s = header(st, data.PROFILE, with_title=True)
    s += section(st, "Professional Summary")
    s += [Paragraph(data.RESUME_SUMMARY, st["lead"])]
    s += section(st, "Education") + education(st, width, courses=False)
    s += section(st, "Technical Skills") + skills(st, data.SKILLS_RESUME)
    s += section(st, "Projects") + projects(st, width, "resume")
    s += section(st, "Experience & Leadership")
    s += experience(st, width, data.EXPERIENCE_RESUME_BULLETS, resume=True)
    s += section(st, "Certifications & Recognition")
    s += bullets(st, data.CERTIFICATIONS_RESUME)
    return s


def cv_story(st, width):
    s = header(st, data.PROFILE, with_title=True)
    s += section(st, "Profile") + [Paragraph(data.SUMMARY, st["body"])]
    s += section(st, "Education") + education(st, width)
    s += section(st, "Technical Skills") + skills(st)
    s += section(st, "Selected Projects") + projects(st, width, "cv")
    s += section(st, "Experience & Leadership") + experience(st, width)
    s += section(st, "Certifications") + two_column_list(st, data.CERTIFICATIONS, width)
    s += section(st, "Achievements") + bullets(st, data.ACHIEVEMENTS)
    return s


def build_resume():
    """Shrink until it fits on one page, then stop."""
    path = os.path.join(OUT, "Saatwik-Vasamsetti-Resume.pdf")
    for size, margin in ((9.6, 0.52 * inch), (9.4, 0.50 * inch), (9.2, 0.48 * inch),
                         (9.0, 0.46 * inch), (8.8, 0.44 * inch), (8.6, 0.42 * inch),
                         (8.4, 0.41 * inch), (8.2, 0.40 * inch)):
        pages = render(path, resume_story, size, margin, "Saatwik Sairaam Vasamsetti - Resume")
        if pages == 1:
            return path, pages, size
    raise SystemExit("resume still spills past one page at 8.2pt - cut content in data.py")


def build_cv():
    """Three pages. A fourth holding seven orphaned lines is just a worse CV."""
    path = os.path.join(OUT, "Saatwik-Vasamsetti-CV.pdf")
    for size, margin in ((9.2, 0.52 * inch), (9.0, 0.50 * inch),
                         (8.8, 0.48 * inch), (8.5, 0.46 * inch)):
        pages = render(path, cv_story, size, margin,
                       "Saatwik Sairaam Vasamsetti - CV", with_footer=True)
        if pages <= 3:
            return path, pages, size
    raise SystemExit("CV runs past three pages at 8.5pt - cut content in data.py")


if __name__ == "__main__":
    for fn in (build_resume, build_cv):
        p, pages, size = fn()
        print("%-46s %d page(s) at %.1fpt" % (os.path.basename(p), pages, size))
