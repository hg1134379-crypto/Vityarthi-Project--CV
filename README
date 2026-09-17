# Smart Campus Vision & Issue Vigilance System

> An AI-assisted campus facility defect inspection and complaint governance platform built with Python, Flask, and OpenCV.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.11-red.svg)](https://opencv.org/)
[![Tests](https://img.shields.io/badge/Tests-38%20Passed-brightgreen.svg)](https://pytest.org/)
[![Database](https://img.shields.io/badge/Database-SQLite3-lightgrey.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-Academic-yellow.svg)](#)

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Problem Statement](#2-problem-statement)
3. [Key Features](#3-key-features)
4. [System Architecture](#4-system-architecture)
5. [Computer Vision Pipeline](#5-computer-vision-pipeline)
6. [Technology Stack](#6-technology-stack)
7. [Folder Structure](#7-folder-structure)
8. [Installation & Setup](#8-installation--setup)
9. [Running the Application](#9-running-the-application)
10. [Default Credentials](#10-default-credentials)
11. [Application Walkthrough](#11-application-walkthrough)
12. [Testing](#12-testing)
13. [Database Schema](#13-database-schema)
14. [Configuration Reference](#14-configuration-reference)
15. [Sample CV Analysis Results](#15-sample-cv-analysis-results)
16. [Security Design](#16-security-design)
17. [Known Limitations & Future Work](#17-known-limitations--future-work)
18. [References](#18-references)

---

## 1. Project Overview

University campuses serve thousands of people daily. Keeping classrooms, hostels, corridors, and electrical fixtures in working order is critical — but traditional grievance systems rely on verbal descriptions, blurry photos, and manual triage, making the process slow and unreliable.

The **Smart Campus Vision & Issue Vigilance System** solves this by pairing a standard full-stack web complaint portal with an automated **OpenCV defect inspection pipeline**. Every photo uploaded with a complaint is automatically:

- checked for sharpness (blurry images are flagged, not rejected)
- analysed for structural defects using Canny edge detection and contour extraction
- assigned a **Defect Severity Score (0–100%)** and a recommended priority (Low / Medium / High)
- saved as an annotated image with bounding boxes and a metadata HUD banner

Administrators see both the original photo and the computer-vision annotated version side by side, giving them objective visual evidence to triage and prioritise maintenance work.

---

## 2. Problem Statement

| Pain Point | Impact |
|---|---|
| Subjective descriptions ("broken bench", "crack somewhere") | Maintenance teams waste time on exploratory inspections |
| Blurry or unusable uploaded photos | Tickets clog queues without actionable proof |
| Chronological-only triage | High-urgency hazards sit behind cosmetic repair requests |
| No status transparency | Students never know if their complaint was acted on |

This project addresses all four by combining automated image analysis, objective severity scoring, role-based governance, and full ticket lifecycle tracking.

---

## 3. Key Features

### Authentication & User Management
- Student self-registration with name, email (regex-validated), and minimum 6-character password
- Werkzeug PBKDF2/SHA-256 salted password hashing — plain-text passwords are never stored
- Per-session CSRF tokens generated with `secrets.token_urlsafe(32)` and verified with `hmac.compare_digest`
- Role-based access control: **Student** and **Admin** roles with separate dashboards and route guards

### Computer Vision Defect Inspection
- **Blur / Quality Check** — Laplacian variance (`Var(∇²I)`) scores image sharpness; images below threshold 75.0 are flagged as blurry
- **Adaptive Edge Detection** — Gaussian smoothing → Otsu auto-threshold → Canny edge map
- **Morphological Dilation** — 3×3 rectangular kernel bridges hairline crack fragments into coherent contours
- **Defect Severity Score** — weighted combination of contour count, edge density %, and damaged area ratio
- **Annotated Output** — bounding boxes (green/orange/red by severity) + HUD banner written directly onto a copy of the image

### Complaint Lifecycle (CRUD)
- Submit tickets with title, description, category, priority, and optional photo
- Track status: `Pending` → `In Progress` → `Resolved`
- Edit uncompleted tickets; delete with ownership enforcement (resolved tickets are locked)
- Side-by-side original + annotated image viewer

### Administrator Governance
- Centralised queue with full-text keyword search and status filter
- Dual-image review panel (raw vs. CV-annotated)
- One-click status transitions with timestamped admin remark
- No data is permanently deleted by administrators; audit trail is preserved

### Reports & Analytics
- KPI counter cards: Total, Pending, In Progress, Resolved
- CV statistics: total CV-verified photos and average defect severity score
- Category distribution table with percentage breakdown

---

## 4. System Architecture

The application follows a layered **MVC** design with an embedded service layer for the CV pipeline.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Presentation Layer                           │
│          Jinja2 HTML templates  ·  CSS3  ·  Vanilla JS              │
└──────────────┬──────────────────────────┬───────────────────────────┘
               │  HTTP Requests           │  Rendered Responses
┌──────────────▼──────────────────────────▼───────────────────────────┐
│                     Flask Blueprint Controllers                     │
│   auth.py   │   complaints.py   │   admin.py   │   reports.py       │
└──────────────┬────────────────────────────────────────────────────┬─┘
               │  calls                                             │  queries
┌──────────────▼──────────────────┐       ┌────────────────────────▼──┐
│   vision_service.py (OpenCV)    │       │   models.py (SQL layer)   │
│   Defect analysis pipeline      │       │   Parameterised queries    │
└─────────────────────────────────┘       └───────────────────────────┘
                                                         │
                                          ┌──────────────▼──────────────┐
                                          │   SQLite3  (campus.db)      │
                                          │   database/campus.db        │
                                          └─────────────────────────────┘
```

**Blueprint responsibilities:**

| Blueprint | File | Responsibility |
|---|---|---|
| `auth` | `auth.py` | Register, login, logout, session management |
| `complaint_bp` | `complaints.py` | Submit, view, edit, delete complaints + CV trigger |
| `admin_bp` | `admin.py` | Admin queue, status updates, remarks |
| `reports_bp` | `reports.py` | Aggregated statistics and analytics |

---

## 5. Computer Vision Pipeline

Every image uploaded with a complaint passes through the following stages inside `vision_service.py`:

```
Upload → Resize (max 1024px) → Grayscale Conversion
    │
    ├─► Laplacian Variance  ─────────────────► Sharpness Score
    │                                           (flag if < 75.0)
    │
    ├─► Gaussian Blur (5×5)
    │
    ├─► Otsu Auto-Threshold  ────────────────► Lower / Upper Canny thresholds
    │
    ├─► Canny Edge Detection ────────────────► Edge Map
    │
    ├─► Morphological Dilation (3×3, 1 iter) ► Bridged Edge Map
    │
    ├─► findContours (RETR_EXTERNAL) ────────► Raw Contour List
    │
    ├─► Filter: keep area ≥ 0.08% of image ──► Significant Contours
    │
    ├─► Severity Score Calculation
    │      count_score   = min(N × 5.0, 30)
    │      density_score = min(edge_density% × 4.0, 40)
    │      area_score    = min(area_ratio% × 3.0, 30)
    │      severity      = clamp(5.0, 100.0, sum)
    │
    ├─► Priority Inference
    │      ≥ 60  → High    (red bounding boxes)
    │      ≥ 30  → Medium  (orange bounding boxes)
    │      < 30  → Low     (green bounding boxes)
    │
    └─► Draw bounding boxes + HUD banner → Save annotated image
```

**Defect category heuristics** (`classify_defect_heuristics`):

| Signal | Inferred Category |
|---|---|
| Mean brightness < 45 | Infrastructure (lighting fault) |
| Contour aspect ratio > 3.5 AND length > 30px | Infrastructure (structural crack) |
| Edge density > 8% | Cleanliness (debris / litter) |
| Edge density > 4% | Hostel |
| Otherwise | Academic |

---

## 6. Technology Stack

| Layer | Technology | Version | Role |
|---|---|---|---|
| Language | Python | 3.10+ | Application runtime |
| Web framework | Flask | ≥ 3.0 | Routing, blueprints, sessions |
| Computer Vision | OpenCV (`cv2`) | 4.11+ | Image processing pipeline |
| Numerical computing | NumPy | Latest | Array operations inside CV |
| Image I/O | Pillow | Latest | Additional image format support |
| Database | SQLite3 | Built-in | Embedded relational storage |
| Security | Werkzeug Security | Bundled | Password hashing |
| Security | Python `secrets`, `hmac` | Built-in | CSRF tokens |
| Frontend | HTML5, CSS3, JS | — | Responsive Jinja2 templates |
| Testing | Pytest | ≥ 9.1 | 38 automated tests |
| PDF generation | ReportLab | Latest | Project report compilation |

---

## 7. Folder Structure

```
vityarthi project cv/
│
├── campus complaint system/        # Core application package
│   ├── app.py                      # Flask app factory, CSRF middleware, error handlers
│   ├── auth.py                     # Authentication blueprint (register/login/logout)
│   ├── complaints.py               # Complaint CRUD blueprint + image upload + CV trigger
│   ├── admin.py                    # Admin dashboard blueprint
│   ├── reports.py                  # Analytics and statistics blueprint
│   ├── models.py                   # Data access layer — all SQL queries live here
│   ├── database.py                 # SQLite connection manager and schema initialiser
│   ├── config.py                   # Centralised app configuration (paths, limits, keys)
│   ├── vision_service.py           # OpenCV defect analysis pipeline
│   ├── create_admin.py             # CLI utility to create the admin account
│   └── requirements.txt            # Python package dependencies
│
├── data/
│   └── sample_images/              # Curated test images for demonstrating CV analysis
│       ├── structural_wall_crack.jpg
│       ├── cleanliness_debris_litter.jpg
│       ├── corridor_lighting_fault.jpg
│       └── normal_facility_bench.jpg
│
├── database/
│   └── campus.db                   # SQLite database (auto-created on first run)
│
├── docs/                           # Project documentation
│   ├── PROJECT_REPORT.md           # Full 15-section academic report
│   ├── COMPLETE_PROJECT_REPORT.md  # Extended report version
│   ├── dataset_and_cv_evaluation.md# CV benchmark and evaluation methodology
│   ├── Project_Report.pdf          # Compiled PDF for portal submission
│   └── diagrams/                   # Mermaid diagram source files
│       ├── system_architecture.md
│       ├── use_case_diagram.md
│       ├── sequence_diagram.md
│       ├── process_flow_diagram.md
│       ├── class_diagram.md
│       ├── er_diagram.md
│       └── cv_pipeline_diagram.md
│
├── static/
│   ├── css/
│   │   └── style.css               # Responsive stylesheet
│   ├── js/
│   │   └── script.js               # Client-side input validation
│   └── uploads/                    # User-uploaded images (git-ignored except .gitkeep)
│       └── annotated/              # OpenCV-annotated defect proof images
│
├── templates/                      # Jinja2 HTML templates
│   ├── base.html                   # Master layout with responsive navigation bar
│   ├── login.html                  # Login form
│   ├── register.html               # Registration form
│   ├── dashboard.html              # Role-based landing page
│   ├── add_complaints.html         # Complaint submission form with photo upload
│   ├── complaints.html             # Student ticket list with CV severity badges
│   ├── edit_complaint.html         # Edit an existing complaint
│   ├── admin_dashboard.html        # Admin triage queue with search and filter
│   ├── reports.html                # Analytics dashboard
│   ├── 403.html                    # Forbidden error page
│   ├── 404.html                    # Not found error page
│   └── 500.html                    # Internal server error page
│
├── tests/
│   ├── conftest.py                 # Pytest fixtures — isolated in-memory test database
│   ├── test_app.py                 # 33 integration tests (auth, CRUD, admin, reports)
│   ├── test_vision.py              # 5 unit tests for the CV pipeline
│   └── __init__.py
│
├── run.py                          # Application entry point
├── generate_report_pdf.py          # ReportLab script — compiles docs/Project_Report.pdf
├── pyrightconfig.json              # Pyright / VS Code static analysis settings
├── statement.md                    # Formal problem statement
├── .gitignore                      # Git exclusion rules
└── README.md                       # This file
```

---

## 8. Installation & Setup

### Prerequisites

- **Python 3.10 or higher** — [download](https://www.python.org/downloads/)
- **pip** (comes with Python)
- Git (optional)

### Step 1 — Navigate to the project directory

```powershell
cd "C:\vityarthi project cv"
```

### Step 2 — (Recommended) Create a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Step 3 — Install all dependencies

```powershell
pip install Flask pytest opencv-python numpy Pillow reportlab
```

All packages and their roles:

| Package | Purpose |
|---|---|
| `Flask` | Web framework |
| `opencv-python` | Computer vision pipeline (`cv2`) |
| `numpy` | Array operations used inside the CV pipeline |
| `Pillow` | Additional image format support |
| `pytest` | Test runner |
| `reportlab` | PDF report generation (optional) |

### Step 4 — Initialise the database and create the admin account

```powershell
python "campus complaint system/create_admin.py" admin
```

This script:
1. Creates the `database/campus.db` SQLite file with the correct schema
2. Creates the default administrator account (see credentials below)

If you want to create an admin with a different password:

```powershell
python "campus complaint system/create_admin.py" your_password_here
```

---

## 9. Running the Application

```powershell
python run.py
```

Open your browser at: **`http://127.0.0.1:5000/`**

The app starts in **debug mode off** by default. To enable debug/hot-reload during development:

```powershell
$env:FLASK_DEBUG = "1"
python run.py
```

To use a custom database path:

```powershell
$env:DATABASE_PATH = "C:\path\to\your.db"
python run.py
```

---

## 10. Default Credentials

| Role | Email | Password |
|---|---|---|
| **Administrator** | `admin@campus.com` | `admin` |
| **Student** | Register via `/register` | (your choice) |

> Change the admin password in production by re-running `create_admin.py` with a strong password, or by updating the hash directly in the database.

---

## 11. Application Walkthrough

### Student Flow

1. **Register** at `/register` — provide your name, a valid email, and a password (min. 6 characters)
2. **Login** at `/login`
3. **Dashboard** — see your open tickets and quick links
4. **Submit a complaint** at `/add-complaint`:
   - Fill in title, description, issue category, and your perceived priority
   - Attach a photo (PNG / JPG / JPEG / WEBP, max 16 MB)
   - On submission, the CV pipeline runs automatically — you are redirected to your complaints list
5. **My Complaints** at `/my-complaints` — see all your tickets with:
   - Status badge (Pending / In Progress / Resolved)
   - CV severity score pill and priority badge
   - Thumbnail of original and annotated image
6. **Edit** a pending or in-progress ticket at `/edit-complaint/<id>`
7. **Delete** a pending ticket (resolved tickets cannot be deleted)

### Administrator Flow

1. Login with the admin account
2. **Admin Dashboard** at `/admin` — full complaint queue with:
   - Live keyword search (title, description, student name)
   - Status filter dropdown
3. Click any complaint to expand the detail panel:
   - Side-by-side original vs. CV-annotated image
   - Severity score, sharpness, detected anomaly count
4. **Update** the complaint status and add a remark → click Save
5. **Reports** at `/reports` — campus-wide analytics

---

## 12. Testing

The project ships with **38 automated tests** covering authentication, CSRF protection, complaint CRUD, admin governance, analytics, and the CV engine.

### Run the full test suite

```powershell
python -m pytest tests/ -v
```

### Run a specific test file

```powershell
# Integration tests only
python -m pytest tests/test_app.py -v

# Computer vision unit tests only
python -m pytest tests/test_vision.py -v
```

### Test categories

| File | Tests | What is covered |
|---|---|---|
| `test_app.py` | 33 | Registration validation, duplicate email guard, password hashing, CSRF rejection, login/logout, role-based redirects, student complaint CRUD, ownership enforcement, resolution lock, admin permission (403), admin status update, remark persistence, analytics aggregation |
| `test_vision.py` | 5 | `is_allowed_file` extension filtering, Laplacian sharpness calculation, synthetic defect image analysis, non-existent file handling, complaint submission with image upload |

### Test isolation

`tests/conftest.py` creates a **fresh in-memory SQLite database** for every test session using a dedicated `app.test_client()` fixture. No production data is ever touched.

### Expected output

```
============================= test session starts =============================
collected 38 items

tests/test_app.py::test_home_redirects_to_login PASSED
tests/test_app.py::test_register_page_loads PASSED
...
tests/test_vision.py::test_compute_sharpness PASSED
tests/test_vision.py::test_analyze_campus_image_synthetic PASSED

============================= 38 passed in ~3s ================================
```

---

## 13. Database Schema

The database is managed by `database.py` and initialised automatically on startup.

### `users` table

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique user identifier |
| `name` | TEXT | NOT NULL | Full name |
| `email` | TEXT | NOT NULL UNIQUE | Login email (lowercased) |
| `password` | TEXT | NOT NULL | PBKDF2 hashed password |
| `role` | TEXT | NOT NULL DEFAULT 'student' | `student` or `admin` |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Account creation time |

### `complaints` table

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique ticket identifier |
| `user_id` | INTEGER | FK → users.id ON DELETE CASCADE | Owner student |
| `title` | TEXT | NOT NULL | Short issue title |
| `description` | TEXT | NOT NULL | Detailed description |
| `category` | TEXT | NOT NULL | Academic / Hostel / Infrastructure / Cleanliness |
| `priority` | TEXT | NOT NULL | Low / Medium / High |
| `status` | TEXT | NOT NULL DEFAULT 'Pending' | Pending / In Progress / Resolved |
| `admin_remark` | TEXT | — | Administrator feedback |
| `image_path` | TEXT | — | Relative path to original upload |
| `annotated_path` | TEXT | — | Relative path to CV-annotated image |
| `defect_score` | REAL | — | CV severity score (0.0–100.0) |
| `cv_summary` | TEXT | — | Human-readable CV analysis summary |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Submission time |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last modification time |

Foreign key cascade is explicitly enabled via `PRAGMA foreign_keys = ON` on every connection.

---

## 14. Configuration Reference

All configuration lives in `campus complaint system/config.py`. Values can be overridden with environment variables.

| Config key | Environment variable | Default | Description |
|---|---|---|---|
| `SECRET_KEY` | `SECRET_KEY` | Hard-coded dev key | Flask session signing key — **change in production** |
| `DATABASE` | `DATABASE_PATH` | `database/campus.db` | Absolute path to SQLite file |
| `UPLOAD_FOLDER` | — | `static/uploads/` | Directory for user-uploaded images |
| `ANNOTATED_FOLDER` | — | `static/uploads/annotated/` | Directory for CV-annotated images |
| `DEBUG` | `FLASK_DEBUG` | `False` | Enable Flask debug/hot-reload |
| `MAX_CONTENT_LENGTH` | — | `16 * 1024 * 1024` | Maximum upload size (16 MB) |

> For production deployment, always set `SECRET_KEY` to a random 32+ byte value and set `FLASK_DEBUG=0`.

---

## 15. Sample CV Analysis Results

Test images in `data/sample_images/` can be uploaded directly on the complaint form to observe the pipeline in action.

| Test Image | Sharpness | Severity Score | Priority | Anomaly Count | Processing Time |
|---|---|---|---|---|---|
| `structural_wall_crack.jpg` | 185 | 14.7% | Low | 6 | ~45 ms |
| `cleanliness_debris_litter.jpg` | 158 | 59.4% | Medium | 13 | ~42 ms |
| `corridor_lighting_fault.jpg` | 86 | 15.3% | Low | 4 | ~35 ms |
| `normal_facility_bench.jpg` | 212 | 40.0% | Medium | 9 | ~40 ms |

Annotated output images are saved to `static/uploads/annotated/` with the prefix `cv_` and can also be found pre-generated in `docs/screenshots/`.

---

## 16. Security Design

| Threat | Mitigation |
|---|---|
| Password theft | Werkzeug PBKDF2-SHA256 with unique salt per user |
| CSRF attacks | Per-session token in every POST form, verified with `hmac.compare_digest` |
| SQL injection | All queries use parameterised `?` placeholders — no string interpolation |
| Path traversal | `werkzeug.utils.secure_filename` + 10-character UUID prefix on every upload |
| Privilege escalation | Role check on every admin route; `abort(403)` on violation |
| Oversized uploads | `MAX_CONTENT_LENGTH = 16 MB` enforced by Flask before handler runs |
| Session fixation | `session.clear()` followed by fresh token assignment on every login |

---

## 17. Known Limitations & Future Work

### Current limitations

- The CV severity score is heuristic-based — it works well on clearly-lit close-up photos but may over- or under-score artistic/complex backgrounds
- SQLite is fine for single-server deployments; concurrent write-heavy loads need PostgreSQL
- No email notification system — students must manually check status updates

### Planned enhancements

1. **YOLOv8 / ONNX segmentation model** — optional deep learning path for specialised crack and water-leakage detection, falling back to the current classical pipeline when the model is absent
2. **PWA with offline camera capture** — service worker + GPS tagging of campus building coordinates on submission
3. **SMS / WhatsApp webhook dispatch** — instant technician alerts on High-severity ticket creation
4. **PostgreSQL migration** — swap the SQLite connection manager for SQLAlchemy with a config-driven engine URL
5. **Email notifications** — Flask-Mail integration for status change alerts to the submitting student

---

## 18. References

1. Bradski, G., & Kaehler, A. (2008). *Learning OpenCV: Computer Vision with the OpenCV Library*. O'Reilly Media.
2. Canny, J. (1986). A computational approach to edge detection. *IEEE Transactions on Pattern Analysis and Machine Intelligence*, PAMI-8(6), 679–698.
3. Otsu, N. (1979). A threshold selection method from gray-level histograms. *IEEE Transactions on Systems, Man, and Cybernetics*, 9(1), 62–66.
4. Pech-Pacheco, J. L., et al. (2000). Diatom autofocusing in brightfield microscopy: a comparative study. *Proceedings of the 15th International Conference on Pattern Recognition*.
5. Grinberg, M. (2018). *Flask Web Development: Developing Web Applications with Python* (2nd ed.). O'Reilly Media.
6. OpenCV Documentation — https://docs.opencv.org/4.x/
7. Flask Documentation — https://flask.palletsprojects.com/en/3.0.x/

---

*VITyarthi — Build Your Own Project | Vellore Institute of Technology | Academic Year 2025–2026*
