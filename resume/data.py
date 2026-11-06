# -*- coding: utf-8 -*-
"""Single source of truth for the resume and the CV.

Both PDFs are rendered from this file by build.py. Edit here, never the PDF.

Every project figure below is measured, and the command that produced it lives
in the repository named beside it. If a number changes in a repo, change it
here too -- a resume that disagrees with its own source is the same defect the
RoadAssist claims gate exists to catch.
"""

FILES = {
    "resume": "Saatwik-Vasamsetti-Resume.pdf",
    "cv": "Saatwik-Vasamsetti-CV.pdf",
}

PROFILE = {
    "name": "Saatwik Sairaam Vasamsetti",
    "title": "Data Analyst · Data Engineer",
    "location": "Vijayawada, Andhra Pradesh, India",
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
    "Data-focused engineer who builds tested systems and checks every number back to its source: "
    "walk-forward ML back-testing in Python and scikit-learn, and a 60-table PostgreSQL + PostGIS "
    "backend verified by 1,603 assertions. Full Stack Web Developer Intern at Qaulium AI; co-founder "
    "of PathAhead. Seeking Data Analyst and Data Engineering internships."
)

# Opens the CV. Longer than RESUME_SUMMARY, which has six seconds to work.
SUMMARY = (
    "Data-focused engineer who ships production-shaped systems and measures them. Recent work spans "
    "Trade Research, where Python computes every figure and a verifier traces each one in a generated "
    "report back to its source data; the backend and cloud database of an offline-first emergency "
    "platform whose TypeScript/PostGIS API passes 1,603 assertions across six suites; and a privacy "
    "engine at Qaulium AI covered by 360 unit and integration tests. "
    "Comfortable with relational schema and index design, SQL, transactional concurrency, Python data "
    "pipelines, model evaluation and BI — and in the habit of reporting the result even when the "
    "result is negative."
)

# Rendered after every other section, newest first. Each entry is two lines:
# school and dates, then qualification and score.
EDUCATION_LAST = True

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
        "school": "SR Junior College",
        "dates": "2022 – 2024",
        "degree": "Intermediate (Class XII, MPC)",
        "detail": "94.8%",
        "courses": None,
    },
    {
        # No completion year on record anywhere; left blank rather than guessed.
        "school": "DAV Public School",
        "dates": None,
        "degree": "Secondary School (Class X)",
        "detail": "81.17%",
        "courses": None,
    },
]

SKILLS = [
    ("Languages", "TypeScript, JavaScript, Python, Kotlin, SQL, Java, HTML, CSS"),
    ("Backend & APIs", "Node.js, Fastify, Express, FastAPI, REST design, JWT auth with rotating "
                       "refresh tokens, RBAC, Zod validation, webhooks"),
    ("Frontend", "React 19, Next.js 16, Angular, Tailwind CSS, Jetpack Compose, progressive web apps, "
                 "dependency-free canvas UI, accessibility (A11y)"),
    ("Databases", "PostgreSQL 16 + PostGIS, MySQL, Drizzle, Prisma, schema & index design, "
                  "transactional concurrency control"),
    ("Data & ML", "pandas, NumPy, scikit-learn, Ultralytics YOLO11, ONNX, exploratory data analysis, "
                  "walk-forward back-testing, conformal prediction, Monte Carlo simulation"),
    ("Visualisation & BI", "Power BI, Tableau, Matplotlib, Chart.js, Advanced Excel dashboards, data storytelling"),
    ("Cloud, Tooling & QA", "AWS, Docker & Compose, Git, GitHub Actions CI, "
                            "Gradle, Vitest, ESLint, PyInstaller"),
]

# --- Projects -----------------------------------------------------------------
# "resume": include in the one-page resume. "cv": include in the CV.
# Bullets are ordered most-defensible first.

PROJECTS = [
    {
        "name": "Trade Research — Verifiable Research & Execution Platform",
        "dates": "Aug – Sep 2026",
        "stack": "Python, scikit-learn, pandas, FastAPI, PostgreSQL, React, MetaTrader 5, PyInstaller",
        # The repo is private, so printing the URL would hand a reader a 404.
        "repo": "Private repository — available on request",
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
        "name": "RoadAssist Bharat — Offline-First Emergency Mobility Platform",
        "dates": "Aug – Oct 2026",
        "stack": "TypeScript, Fastify, PostgreSQL 16 + PostGIS, Drizzle, zod, Docker, GitHub Actions",
        "repo": "github.com/saatwik-1157/roadassist-bharat",
        "resume": True,
        "cv": True,
        # Four-person course project (SWE4004). Saatwik's workstream is backend & cloud
        # database; claim that, not the whole platform. Figures: app/docs/measured.json.
        "resume_bullets": [
            'Led backend &amp; cloud database for a four-person team: an 86-route Fastify/TypeScript API over a 60-table PostgreSQL 16 + PostGIS schema with 151 indexes and 13 migrations.',
            'Verified by 1,603 assertions across six suites with zero failures, including 112 concurrency tests and 144 refused security attacks.',
            'Made races impossible in the database rather than by timing: row locks with expiry re-checked under the lock, a partial unique index guaranteeing "paid once", and a hash-chained, immutable audit log.',
        ],
        "bullets": [
            "Led the backend &amp; cloud-database workstream of a four-person team: an 86-route Fastify "
            "modular monolith over a 60-table PostGIS schema with 151 indexes and 13 migrations, "
            "serving four browser surfaces, a native Android client and a feature-phone SMS channel.",
            "Platform verified by 1,603 assertions across six suites, zero failures — including 144 "
            "security attacks that must each be refused (cross-tenant access, role escalation, SQL "
            "injection, forged and alg:none tokens, unsigned webhooks) and 112 concurrency tests.",
            "Settled every race in the database rather than by timing: SELECT ... FOR UPDATE on booking "
            "rows with offer expiry re-checked under the lock, a partial unique index making \"paid once\" "
            "true under simultaneous confirmations, and a hash-chained audit log that Postgres RULES make "
            "immutable.",
            "Implemented auth end to end: hashed SMS one-time codes, 10-minute access tokens and "
            "rotating refresh tokens whose reuse revokes the whole family, with zod validation on "
            "every route.",
            "The platform's health endpoint distinguishes \"no network\" from \"platform unwell\": CI "
            "kills PostgreSQL under a running API and checks /health returns 503 while /v1/ping "
            "stays up, then rehearses a backup and restore and re-verifies the audit chain.",
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
            "Built a FastAPI predictive-maintenance prototype on simulated IoT sensor data: MAD "
            "z-score anomaly detection, 0-100 health scores explained per sensor, and "
            "remaining-useful-life forecasting.",
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
        "name": "Smart University Management System (SUMS)",
        "dates": "2026",
        "stack": "MySQL, JavaScript, Chart.js, CSS3",
        "repo": "github.com/saatwik-1157/database_management_SUMS",
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
        "name": "Angular Applications — ShopCart, Notes, Search & Auth",
        "dates": "2026",
        "stack": "Angular 22, TypeScript 6, standalone components, signals, Vitest",
        "repo": None,
        "resume": False,
        "cv": True,
        "resume_bullets": [
            "Built four Angular 22 applications on standalone components and signals in a zoneless "
            "app: ShopCart, a full e-commerce site; a notes app; a live-filtering search template; "
            "and an authentication app with a guarded route.",
            "ShopCart is the largest: searchable, category-filtered catalogue, product detail pages, a "
            "quantity-aware cart with computed totals and accounts behind a route guard, covered by 14 "
            "Vitest unit tests across three files.",
        ],
        "bullets": [
            "<b>ShopCart (e-commerce):</b> searchable, category-filtered catalogue, product detail "
            "pages, a quantity-aware cart with computed totals, and signup/sign-in with a route guard "
            "protecting checkout — 14 Vitest unit tests across cart, accounts and header.",
            "<b>Search template:</b> a user list loaded from JSON through a service and filtered on "
            "screen as the query is typed, matching on either name or email address.",
            "<b>Notes app:</b> add, update and delete notes held in a service-owned signal, rendered "
            "through separate form, list and single-note components.",
            "<b>Authentication app:</b> a login page validated in a service, with the home page "
            "reachable only through a route guard after a successful sign-in.",
            "Every experiment's lab record is generated from the live source on disk rather than "
            "written by hand, so the submitted document cannot disagree with the code that ran.",
        ],
    },
    {
        "name": "ExamPlanner — Android Study Planner",
        "dates": "2026",
        "stack": "Kotlin, Android, Java",
        # Private repository; no link rather than a 404.
        "repo": None,
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
        "name": "PathAhead — Career-Guidance Platform",
        "dates": "Jun 2026 – Present",
        "stack": "HTML, CSS, JavaScript, Netlify Functions",
        "repo": "github.com/saatwik-1157/project_PathAhead",
        "resume": False,
        "cv": True,
        "bullets": [
            "Built the live platform (pathahead22.netlify.app): 12 career roadmaps with downloadable "
            "PDFs, a Career Builder that turns branch, year and interest into a plan, and an AI "
            "counsellor grounded only in PathAhead's own content — 45 commits.",
            "Static site with two Netlify serverless functions (counsellor, leads), so it stays fast on "
            "the patchy mobile data most students open it on.",
            "Shipped the surrounding promotional kit alongside it: presentation, brochure and "
            "tri-fold materials, so the launch did not depend on a separate design pass.",
        ],
    },
    {
        "name": "Additional projects",
        "dates": None,
        "stack": None,
        "repo": None,
        "resume": False,
        "cv": True,
        "bullets": [
            "Gemini Chat Client — a complete browser-only chat client: multi-thread sidebar, four "
            "personas, vision and voice input, Markdown rendering sanitised with DOMPurify, "
            "localStorage persistence, no server and no build step.",
        ],
    },
]

EXPERIENCE = [
    {
        # Role and dates as on LinkedIn. Work described from the qualium-browser-ui
        # repo, whose 360 Vitest tests were run and passed on 2026-10-23.
        "role": "Full Stack Web Developer Intern",
        "org": "Qaulium AI Private Limited",
        "dates": "Jul 2026 – Present",
        "resume": True,
        "bullets": [
            "Built the privacy engine of the Qualium Quantum Browser in TypeScript — ad and tracker "
            "blocking, cookie and storage isolation, fingerprint, WebRTC and DNS protection — as pure "
            "decision functions with no I/O, so every rule is testable without a browser.",
            "Covered it with 360 Vitest unit and integration tests across 22 files and 24 Playwright "
            "end-to-end tests, gated on typecheck and lint.",
        ],
    },
    {
        "role": "Co-Founder",
        "org": "PathAhead, career-guidance platform",
        "dates": "Jun 2026 – Present",
        "resume": True,
        "bullets": [
            "Built the live platform: 12 career roadmaps, a Career Builder and an AI counsellor "
            "grounded in PathAhead's own content, on two Netlify functions.",
        ],
    },
    {
        "role": "Campus Ambassador",
        "org": "SmartED Innovations",
        "dates": "Jun – Jul 2026",
        "resume": False,
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
    "Data Fundamentals — IBM SkillsBuild, Jan 2026",
    "GenAI-Powered Data Analytics (Job Simulation) — Forage, Jun 2026",
    "Data Analytics Job Simulation — Deloitte via Forage, Jul 2026",
    "Data Analytics Job Simulation — Quantium via Forage, Aug 2026",
    "Introduction to AWS — AWS Training & Certification, May 2026",
    "AWS Certified Cloud Practitioner (CLF-C02) Domain 1 Review — AWS, May 2026",
    "AWS Certified Data Engineer – Associate (DEA-C01) Exam Prep — AWS, May 2026",
    "Exploring SAP Analytics Cloud — SAP Learning, Jun 2026",
    "Becoming an SAP Data Architect — SAP Learning, Jun 2026",
    "Architecting Agentic AI Business Solutions — Microsoft Learn badge, 2026",
]

# Condensed grouping used on the one-page resume.
CERTIFICATIONS_RESUME = [
    "<b>Google Analytics Certification</b> — Google, to May 2027",
    "<b>Data Fundamentals</b> — IBM SkillsBuild",
    "<b>Introduction to AWS</b> — AWS Training &amp; Certification",
    "<b>Cloud Practitioner (CLF-C02) Domain 1 Review</b> — AWS",
    "<b>Data Engineer – Associate (DEA-C01) Exam Prep</b> — AWS",
    "<b>Exploring SAP Analytics Cloud</b> — SAP Learning",
    "<b>Becoming an SAP Data Architect</b> — SAP Learning",
    "<b>Architecting Agentic AI Business Solutions</b> — Microsoft Learn",
    "<b>Data Analytics Job Simulations</b> — Quantium and Deloitte, via Forage",
    "<b>GenAI-Powered Data Analytics Simulation</b> — Tata, via Forage",
]

RECOGNITION_RESUME = [
    "<b>Campus Ambassador</b> — SmartED Innovations, 2026",
    "<b>Smart India Hackathon 2026</b> — MachineSense AI",
    "<b>HackDevengers 1.0</b> — participant",
    "<b>SentinelAI</b> — Samsung Solve for Tomorrow &amp; Ideas for India 2026",
    "<b>IIT Hyderabad Student Body Workshop</b> — Career &amp; AI, Jun 2026",
]

ACHIEVEMENTS = [
    "Led backend &amp; cloud database for RoadAssist Bharat, a four-person platform verified by "
    "1,603 assertions across six suites with zero failures.",
    "Earned ten professional certifications across data analytics and cloud — AWS, Google and "
    "SAP and Microsoft — including three Forage job simulations (Deloitte, Quantium, GenAI analytics).",
    "Attended the IIT Hyderabad Student Body Workshop on Career, AI &amp; Campus Experience, Jun 2026.",
    "Participant, HackDevengers 1.0 hackathon — organised by Devengers, 2026.",
    "Scored 94.8% in Class XII and 81.17% in Class X; recognised as Campus Ambassador, SmartED (2026).",
    "Designed, built and deployed a dependency-free personal portfolio at saatwik-1157.github.io.",
]


# --- One-page resume variants -------------------------------------------------
# The CV gets the full grouping above; the resume gets the same facts in five
# lines instead of seven.

SKILLS_RESUME = [
    ("Languages", "Python, SQL, TypeScript, JavaScript, Java, Kotlin, HTML, CSS"),
    ("Data &amp; Analytics", "pandas, NumPy, scikit-learn, EDA, walk-forward back-testing, "
                             "conformal prediction, Matplotlib, Power BI, Tableau, Excel"),
    ("Databases &amp; Data Eng.", "PostgreSQL 16 + PostGIS, MySQL, Drizzle, schema &amp; index "
                                  "design, migrations, concurrency control, SEC EDGAR ingestion"),
    ("APIs, ML &amp; Tools", "FastAPI, REST, YOLO11, ONNX, AWS, Docker, Git, GitHub Actions CI, "
                             "Vitest, Playwright"),
]

# How many bullets each Experience entry gets on the resume.
EXPERIENCE_RESUME_BULLETS = 2
