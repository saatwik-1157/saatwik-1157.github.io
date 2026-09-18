# -*- coding: utf-8 -*-
"""Single source of truth for the resume and the CV.

Both PDFs are rendered from this file by build.py. Edit here, never the PDF.

Every project figure below is measured, and the command that produced it lives
in the repository named beside it. If a number changes in a repo, change it
here too -- a resume that disagrees with its own source is the same defect the
RoadAssist claims gate exists to catch.
"""

PROFILE = {
    "name": "Saatwik Sairaam Vasamsetti",
    "title": "Full-Stack Software Engineer · Data & Analytics",
    "location": "Andhra Pradesh, India",
    "phone": "+91-9989057655",
    "email": "saathwik.13@gmail.com",
    "github": "github.com/saatwik-1157",
    "linkedin": "linkedin.com/in/saatwiksairaamvasamsetti",
    "site": "saatwik-1157.github.io",
    # Link targets. The header shows the text above and hyperlinks to these.
    "email_url": "mailto:saathwik.13@gmail.com",
    "phone_url": "tel:+919989057655",
    "github_url": "https://github.com/saatwik-1157",
    "linkedin_url": "https://linkedin.com/in/saatwiksairaamvasamsetti",
    "site_url": "https://saatwik-1157.github.io",
}

# Opens the one-page resume. Three lines, because the reader gives it six
# seconds and decides there. Every claim in it is expanded and evidenced below.
RESUME_SUMMARY = (
    "Full-stack engineer who ships complete systems and proves they work. Sole author of an "
    "emergency-response platform — a 64-route TypeScript API on PostgreSQL/PostGIS, a Kotlin "
    "Compose Android client and a YOLO11 vision pipeline — whose API alone passes 636 assertions "
    "across six suites, 74 of them security attacks, plus 66 Android and 39 pipeline tests. Strong in "
    "data too: scikit-learn back-testing, statistical validation and BI, with 12 certifications across "
    "AWS, Google, SAP and Oracle. Available immediately for software-engineering and data internships."
)

# Opens the CV. Longer than RESUME_SUMMARY, which has six seconds to work.
SUMMARY = (
    "Full-stack engineer who ships production-shaped systems and measures them. Recent work spans a "
    "TypeScript/PostgreSQL platform with 636 passing assertions and a Kotlin Compose client, a YOLO11 "
    "computer-vision pipeline trained to a measured mAP50 of 0.471, and research tooling where every "
    "number in a generated report is machine-checked back to its source data. Comfortable across the "
    "stack — API and schema design, transactional concurrency, front-end delivery, Python data "
    "pipelines and BI — and in the habit of reporting the result even when the result is negative."
)

EDUCATION = [
    {
        "school": "VIT-AP University, Amaravati",
        "dates": "2024 – 2029",
        "degree": "Integrated M.Tech — Computer Science & Engineering (in collaboration with Virtusa)",
        "detail": "CGPA: 7.55 / 10",
        "courses": "Advanced Programming, Data Structures & Algorithms, Database Management Systems, "
                   "Software Engineering, Frontend Design & Testing",
    },
    {
        "school": "SR Junior College — Intermediate (Class XII, MPC)",
        "dates": "2022 – 2024 · 94.8%",
        "degree": None,
        "detail": None,
        "courses": None,
    },
    {
        "school": "DAV Public School — Secondary School (Class X)",
        "dates": "81.17%",
        "degree": None,
        "detail": None,
        "courses": None,
    },
]

SKILLS = [
    ("Languages", "TypeScript, JavaScript, Python, Kotlin, SQL, Java, HTML, CSS"),
    ("Backend & APIs", "Node.js, Fastify, Express, FastAPI, REST design, JWT auth with rotating "
                       "refresh tokens, RBAC, Zod validation, webhooks"),
    ("Frontend", "React 19, Next.js 15, Angular, Tailwind CSS, Jetpack Compose, progressive web apps, "
                 "dependency-free canvas UI, accessibility (A11y)"),
    ("Databases", "PostgreSQL 16 + PostGIS, MySQL, Drizzle, Prisma, schema & index design, "
                  "transactional concurrency control"),
    ("Data & ML", "pandas, NumPy, scikit-learn, Ultralytics YOLO11, ONNX, exploratory data analysis, "
                  "walk-forward back-testing, conformal prediction, Monte Carlo simulation"),
    ("Visualisation & BI", "Power BI, Tableau, Matplotlib, Chart.js, Advanced Excel dashboards, data storytelling"),
    ("Cloud, Tooling & QA", "AWS Cloud Foundations, Oracle Cloud (OCI), Docker & Compose, Git, GitHub Actions CI, "
                            "Gradle, Vitest, ESLint, PyInstaller"),
]

# --- Projects -----------------------------------------------------------------
# "resume": include in the one-page resume. "cv": include in the CV.
# Bullets are ordered most-defensible first.

PROJECTS = [
    {
        "name": "RoadAssist Bharat — Offline-First Emergency Mobility Platform",
        "dates": "Aug – Sep 2026",
        "stack": "TypeScript, Fastify, PostgreSQL 16 + PostGIS, Drizzle, Kotlin, Jetpack Compose, "
                 "Python, YOLO11, Docker, GitHub Actions",
        "repo": "github.com/saatwik-1157/roadassist-bharat",
        "resume": True,
        "cv": True,
        "resume_bullets": [
            'Sole author of a 64-route Fastify/TypeScript API over a 56-table PostGIS schema, plus a Kotlin Compose Android client and four browser surfaces — 117 commits.',
            'Verified the API with 636 assertions across six suites, zero failures, including 75 concurrency tests and 74 security attacks that must each be refused.',
            'Trained four YOLO11 variants on RDD2022 across four countries — best measured mAP50 0.471 on held-out validation, plus a separate nano ONNX tier at ~48 ms/image on CPU for Pi-class hardware.',
        ],
        "bullets": [
            "Designed and built the entire platform solo across 117 commits: a 64-route Fastify modular "
            "monolith, a 56-table PostGIS schema with 138 indexes and 5 migrations, four browser surfaces, "
            "a native Android client and a computer-vision pipeline.",
            "Verified the API with 636 assertions across six suites, zero failures — including 74 security "
            "attacks that must each be refused (cross-tenant access, role escalation, SQL injection, "
            "forged and alg:none tokens, unsigned webhooks) and 75 concurrency tests.",
            "Settled every race in the database rather than by timing: SELECT ... FOR UPDATE on booking "
            "rows with offer expiry re-checked under the lock, a partial unique index making \"paid once\" "
            "true under simultaneous confirmations, and a hash-chained audit log that Postgres RULES make "
            "immutable.",
            "Trained four YOLO11 variants on RDD2022 across four countries: the best reaches a measured "
            "mAP50 of 0.471 (mAP50-95 0.226) on held-out validation at ~135 ms/image, and a separate "
            "nano tier trades accuracy for ~48 ms/image on CPU for Pi-class hardware. Potholes remain "
            "the hard class at ~0.24, and the per-class breakdown says so.",
            "Shipped Off-Grid Mode as architecture, not fallback: a Kotlin SOS ladder (data → SMS → 112 "
            "→ offline queue) where exactly one channel owns an emergency, proven by 21 unit tests on "
            "that file alone, so a retry never dispatches a second ambulance.",
            "Wrote CI gates that fail the build when a document disagrees with the measured figures, when "
            "a file:line citation rots, or when module boundaries break — after the same wrong number "
            "reached twenty documents three times and a human caught it each time.",
            "Made a feature phone a first-class client: a complete booking over SMS with no app, in eight "
            "languages switched by text command — seven of them machine-translated and not yet "
            "native-reviewed, which the project states rather than implies.",
        ],
    },
    {
        "name": "Trade Research — Verifiable Research & Execution Platform",
        "dates": "Aug – Sep 2026",
        "stack": "Python, scikit-learn, pandas, FastAPI, PostgreSQL, React, MetaTrader 5, PyInstaller",
        "repo": "github.com/saatwik-1157/trade-research",
        "resume": True,
        "cv": True,
        "resume_bullets": [
            'Built a leakage-free walk-forward back-test of six scikit-learn models against naive and drift baselines, with conformal intervals, Monte Carlo paths and a cost-aware trading simulation.',
            'Made the numbers checkable: indicators computed in Python, financials from SEC EDGAR XBRL, and a verifier that traces every figure in a generated note back to the data — then reported the honest negative result.',
        ],
        "bullets": [
            "Built a leakage-free walk-forward back-test benchmarking six scikit-learn models against "
            "naive and drift baselines, with conformal prediction intervals reporting honest held-out "
            "coverage, Monte Carlo price paths, and a cost-aware trading simulation reporting Sharpe "
            "and drawdown.",
            "Inverted the usual \"AI analyst\" design so Python computes and the model only interprets: "
            "indicators are calculated in code, financials come from SEC EDGAR XBRL with accession "
            "numbers, missing data stays null, and a verifier machine-checks every figure in the "
            "finished note back to the snapshot.",
            "Implemented the execution platform end to end — FastAPI, PostgreSQL and React wiring "
            "alerts through risk checks and an OMS to the broker — plus an autonomous MetaTrader 5 "
            "demo harness with scheduled wind-down.",
            "Reported the negative result rather than burying it: none of the strategies measured here "
            "has a demonstrable edge, and the README says so first.",
            "Measured the packaging decision instead of preferring one: PyInstaller onedir starts in "
            "1,000 ms against onefile's 5,400 ms, so the 24-command toolkit ships as a directory.",
        ],
    },
    {
        "name": "SkillForge — Entrepreneurship Enablement Platform",
        "dates": "2026",
        "stack": "TypeScript, Next.js 15, React 19, Express, Prisma, PostgreSQL 16, Tailwind CSS, Docker",
        "repo": "github.com/saatwik-1157/skillforge",
        "resume": True,
        "cv": True,
        "resume_bullets": [
            'Architected a Next.js 15 / React 19 front end over an Express + Prisma API on PostgreSQL 16, containerised with Docker Compose.',
            "Built a recommendation engine scoring 150+ business ideas against a user's skills, budget and time, behind JWT auth with rotating refresh tokens, OTP verification and RBAC.",
        ],
        "bullets": [
            "Architected a full-stack monorepo turning skills into businesses: a Next.js 15 / React 19 "
            "front end over an Express + Prisma API on PostgreSQL 16, containerised with Docker Compose.",
            "Built a recommendation engine scoring 150+ business ideas against a user's skills, budget, "
            "available time and preferred business type, backed by a business-readiness assessment.",
            "Implemented production-grade auth — JWT with rotating refresh tokens, OTP email "
            "verification, password reset, Google login and role-based access control across "
            "entrepreneur, mentor and admin roles.",
            "Shipped the surrounding product: mentor booking with reviews, courses with auto-issued "
            "certificates, a threaded community forum, notifications, and an admin console for content "
            "approval and analytics.",
        ],
    },
    {
        "name": "MachineSense AI — Explainable Industrial Intelligence",
        "dates": "Smart India Hackathon 2026",
        "stack": "Python, FastAPI, JavaScript, Canvas",
        "repo": "github.com/saatwik-1157/machinesense-ai",
        "resume": True,
        "cv": True,
        "resume_bullets": [
            'Built a FastAPI predictive-maintenance platform: weighted 0-100 health scoring, MAD z-score anomaly detection, remaining-useful-life forecasting and fleet energy optimisation.',
            'Made every score explainable by sensor with plain-language root causes, and added a digital twin that simulates a maintenance action before anyone touches the machine.',
        ],
        "bullets": [
            "Built an Industry 4.0 prototype for Indian industrial units: a FastAPI backend simulating a "
            "fleet of IoT-instrumented machines (vibration, temperature, current, sound, power) behind "
            "an analytics engine and a six-view real-time dashboard.",
            "Implemented the AI layer — a weighted 0-100 machine health score, MAD z-score anomaly "
            "detection, remaining-useful-life and failure-probability forecasting, and energy/cost/CO2 "
            "optimisation across the fleet.",
            "Made every score explainable: each health number is decomposed by sensor with "
            "plain-language root-cause reasoning, and a digital twin simulates a maintenance action "
            "before anyone touches the real machine.",
            "Mirrored the same scoring logic in dependency-free browser JavaScript so the demo behaves "
            "identically with the backend down, and labelled on screen which mode is running.",
        ],
    },
    {
        "name": "Founder Labs Autopilot — Ads → Voice → Revenue Closed Loop",
        "dates": "Sep 2026",
        "stack": "TypeScript, Node 24, Meta Ads API, Anthropic SDK, webhooks",
        "repo": "github.com/saatwik-1157/ads-voice-revenue-loop",
        "resume": False,
        "cv": True,
        "bullets": [
            "Implemented an AI orchestrator that picks a niche, writes the offer and creative, publishes "
            "a guarded Meta test campaign, hands each lead to a voice agent, reads structured call "
            "outcomes back, and decides KEEP / KILL / ITERATE / SCALE from revenue rather than clicks.",
            "Carried campaign, adset, ad and creative identifiers from the lead form through the voice "
            "agent's call metadata and back on the post-call webhook — the round trip that lets a sale "
            "be attributed to the exact hook that paid for it.",
            "Put spend behind guardrails and two human approval gates, and made the whole loop runnable "
            "against mock providers so it demonstrates end to end with no ad spend and no phone calls.",
        ],
    },
    {
        "name": "Smart University Management System (SUMS)",
        "dates": "2026",
        "stack": "MySQL, JavaScript, Chart.js, CSS3",
        "repo": "github.com/saatwik-1157/smart_university_management-system_dbms",
        "resume": False,
        "cv": True,
        "bullets": [
            "Designed a normalised MySQL schema for an enterprise university system managing students, "
            "courses, faculty and academic records, with the query layer behind it.",
            "Built a glassmorphism front end with Chart.js dashboards surfacing enrolment and "
            "performance insights over the live data.",
        ],
    },
    {
        "name": "OfferPilot — Job-Application Platform for F-1 / OPT Students",
        "dates": "2026",
        "stack": "JavaScript, HTML, CSS, localStorage",
        "repo": "github.com/saatwik-1157/offerpilot",
        "resume": False,
        "cv": True,
        "bullets": [
            "Built a dependency-free static platform — marketing site, onboarding, client dashboard, "
            "profile, legal pages and a passcode-gated ops console — with no build step and full "
            "localStorage persistence.",
            "Shipped the RezForge resume-tailoring engine, an interview kanban, a referral programme and "
            "analytics charts on a hand-written SVG engine, plus an OPT Runway Calculator computing "
            "work-authorisation runway, unemployment-day budget and H-1B lottery timing.",
            "Labelled the prototype honestly on the page: the match and resume engines are deterministic "
            "mocks and no real applications are submitted.",
        ],
    },
    {
        "name": "ShopCart — Angular E-Commerce Application",
        "dates": "2026",
        "stack": "Angular, TypeScript, Signals, Vitest",
        "repo": "Frontend Design & Testing Lab (SWE3004)",
        "resume": False,
        "cv": True,
        "bullets": [
            "Built a signal-based Angular storefront: searchable and category-filtered catalogue, "
            "product detail pages, a quantity-aware cart with computed totals, and accounts with a "
            "route guard protecting checkout.",
            "Covered cart, accounts and header behaviour with 14 Vitest unit tests across three files.",
        ],
    },
    {
        "name": "ExamPlanner — Android Study Planner",
        "dates": "2026",
        "stack": "Kotlin, Android, Java",
        "repo": "github.com/saatwik-1157/ExamPlanner",
        "resume": False,
        "cv": True,
        "bullets": [
            "Built a native Android study planner with authentication, exam and schedule management, and "
            "a Pomodoro timer with customisable focus and break intervals.",
        ],
    },
    {
        "name": "GenAI-Powered Data Analytics — Job Simulation",
        "dates": "Forage · Jun 2026",
        "stack": "Python, pandas, GenAI, data storytelling",
        "repo": None,
        "resume": False,
        "cv": True,
        "bullets": [
            "Performed exploratory data analysis and risk profiling on a real-world lending dataset, "
            "built a model to predict customer delinquency, and delivered the data storytelling behind "
            "an AI-driven collections strategy.",
        ],
    },
    {
        "name": "Additional public repositories",
        "dates": None,
        "stack": None,
        "repo": None,
        "resume": False,
        "cv": True,
        "bullets": [
            "PathAhead — production-ready responsive site for a career-guidance platform running "
            "workshops for intermediate students across India (41 commits).",
            "Gemini Chat Client — a complete browser-only chat client: multi-thread sidebar, four "
            "personas, vision and voice input, Markdown rendering sanitised with DOMPurify, "
            "localStorage persistence, no server and no build step.",
            "YouTube Clone — responsive vanilla-JS UI clone with dynamic rendering and accessible "
            "components; Python ATM — CLI banking simulator with JSON persistence and PIN attempt "
            "limits; Assistant Bot — rule-based study helper that runs with the network off.",
        ],
    },
]

EXPERIENCE = [
    {
        "role": "Campus Ambassador",
        "org": "SmartED",
        "dates": "Jun 2026",
        "bullets": [
            "Led campus outreach for SmartED's initiatives; formally recognised for leadership, "
            "dedication and the connections built across the student community.",
        ],
    },
    {
        "role": "Data Analytics Job Simulations",
        "org": "Deloitte, Quantium &amp; GenAI programmes via Forage",
        "dates": "Jun – Aug 2026",
        # Listed under Certifications on the one-pager; the CV carries the detail.
        "resume": False,
        "bullets": [
            "Deloitte (Jul 2026): completed practical tasks in data analysis and forensic technology.",
            "Quantium (Aug 2026): data preparation and customer analytics, experimentation and uplift "
            "testing, and the commercial application of the results.",
            "GenAI-Powered Data Analytics (Jun 2026): exploratory data analysis and risk profiling on a "
            "lending dataset, delinquency prediction, and the data storytelling behind an AI-driven "
            "collections strategy.",
        ],
    },
]

CERTIFICATIONS = [
    "Google Analytics Certification — Google, May 2026 – May 2027 (ID 183723043)",
    "Google AI Essentials — Google",
    "GenAI-Powered Data Analytics (Job Simulation) — Forage, Jun 2026",
    "Data Analytics Job Simulation — Deloitte via Forage, Jul 2026",
    "Data Analytics Job Simulation — Quantium via Forage, Aug 2026",
    "Introduction to AWS — AWS Training & Certification, May 2026",
    "AWS Certified Cloud Practitioner (CLF-C02) Domain 1 Review — AWS, May 2026",
    "AWS Certified Data Engineer – Associate (DEA-C01) Exam Prep — AWS, May 2026",
    "Exploring SAP Analytics Cloud — SAP Learning, Jun 2026",
    "Becoming an SAP Data Architect — SAP Learning, Jun 2026",
    "OCI Foundations Associate — Oracle",
    "Responsive Web Design — freeCodeCamp",
]

# Condensed grouping used on the one-page resume.
CERTIFICATIONS_RESUME = [
    "<b>AWS Training &amp; Certification:</b> Introduction to AWS &nbsp;·&nbsp; Cloud Practitioner "
    "(CLF-C02) Domain 1 &nbsp;·&nbsp; Data Engineer – Associate (DEA-C01) Exam Prep "
    "&nbsp;·&nbsp; <b>Oracle:</b> OCI Foundations Associate",
    "<b>Google:</b> Analytics Certification (ID 183723043) &nbsp;·&nbsp; AI Essentials "
    "&nbsp;·&nbsp; <b>SAP Learning:</b> SAP Analytics Cloud &nbsp;·&nbsp; SAP Data Architect "
    "&nbsp;·&nbsp; <b>freeCodeCamp:</b> Responsive Web Design",
    "<b>Forage Job Simulations:</b> Deloitte Data Analytics &nbsp;·&nbsp; Quantium Data Analytics "
    "&nbsp;·&nbsp; GenAI-Powered Data Analytics &nbsp;·&nbsp; <b>Recognition:</b> Campus "
    "Ambassador, SmartED (2026) &nbsp;·&nbsp; Participant, HackDevengers 1.0 (2026)",
]

ACHIEVEMENTS = [
    "Sole author of RoadAssist Bharat — 117 commits covering API, Android client, CV pipeline, "
    "schema, six test suites and CI, with 636 assertions passing over the API and zero failures.",
    "Trained and measured four YOLO11 detector variants on RDD2022, reaching mAP50 0.471 on held-out "
    "validation and publishing the per-class breakdown including the classes that perform badly.",
    "Earned 12 professional certifications across data analytics, cloud (AWS &amp; Oracle), SAP and web "
    "development, including three Forage job simulations (Deloitte, Quantium, GenAI analytics).",
    "Participant, HackDevengers 1.0 hackathon — organised by Devengers, 2026.",
    "Scored 94.8% in Class XII and 81.17% in Class X; recognised as Campus Ambassador, SmartED (2026).",
    "Designed, built and deployed a dependency-free personal portfolio at saatwik-1157.github.io.",
]


# --- One-page resume variants -------------------------------------------------
# The CV gets the full grouping above; the resume gets the same facts in five
# lines instead of seven.

SKILLS_RESUME = [
    ("Languages", "TypeScript, JavaScript, Python, Kotlin, SQL, Java, HTML, CSS"),
    ("Backend &amp; Data Stores", "Node.js, Fastify, Express, FastAPI, REST design, JWT/RBAC auth, "
                                  "PostgreSQL 16 + PostGIS, MySQL, Drizzle, Prisma, schema &amp; index "
                                  "design, transactional concurrency"),
    ("Frontend", "React 19, Next.js 15, Angular, Tailwind CSS, Jetpack Compose, progressive web apps, "
                 "dependency-free canvas UI, accessibility"),
    ("Data, ML &amp; BI", "pandas, NumPy, scikit-learn, Ultralytics YOLO11, ONNX, EDA, walk-forward "
                          "back-testing, conformal prediction, Monte Carlo, Power BI, Tableau, "
                          "Matplotlib, Excel dashboards"),
    ("Cloud, Tooling &amp; QA", "AWS, Oracle Cloud (OCI), Docker &amp; Compose, Git, GitHub Actions CI, "
                                "Gradle, Vitest, ESLint"),
]

# How many bullets each Experience entry gets on the resume.
EXPERIENCE_RESUME_BULLETS = 1
