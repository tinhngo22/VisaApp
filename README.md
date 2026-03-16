# VisaApp

Full-stack boilerplate using **FastAPI** (Python) for the backend and **Next.js** (TypeScript) for the frontend.

```
visaapp/
├── backend/          # FastAPI app
│   ├── app/
│   │   ├── api/
│   │   │   ├── router.py          # Registers all route groups
│   │   │   └── routes/
│   │   │       └── health.py      # GET /api/health
│   │   ├── core/
│   │   │   └── config.py          # Pydantic-settings config (reads .env)
│   │   ├── models/                # SQLAlchemy / Pydantic models (add here)
│   │   └── main.py                # App entry point, CORS middleware
│   ├── .env.example
│   ├── .gitignore
│   └── requirements.txt
├── frontend/         # Next.js 15 app (App Router, TypeScript, Tailwind)
│   ├── src/
│   │   ├── app/
│   │   │   └── page.tsx           # Home page — calls /api/health
│   │   └── lib/
│   │       └── api.ts             # Typed fetch wrapper
│   └── .env.local                 # NEXT_PUBLIC_API_URL
├── .gitignore
└── README.md
```

---

## Setup

### Prerequisites

- Python 3.11+
- Node.js 20+
- npm 10+

---

### Backend

```bash
cd backend

# 1. Create and activate a virtual environment
python -m venv .venv

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy the example env file and edit as needed
copy .env.example .env   # Windows
cp .env.example .env     # macOS / Linux

# 4. Start the dev server
uvicorn app.main:app --reload --port 8000
```

The API will be available at <http://localhost:8000>.  
Interactive docs (Swagger UI) are at <http://localhost:8000/docs>.

---

### Frontend

```bash
cd frontend

# 1. Install dependencies (already done during scaffold, run again after cloning)
npm install

# 2. Start the dev server
npm run dev
```

The app will be available at <http://localhost:3000>.

---

## How They Connect

| | Value |
|---|---|
| Frontend origin | `http://localhost:3000` |
| Backend API URL | `http://localhost:8000` |
| CORS origin (backend `.env`) | `http://localhost:3000` |
| Env var (frontend `.env.local`) | `NEXT_PUBLIC_API_URL=http://localhost:8000` |

The Next.js home page performs a server-side fetch to `GET /api/health` and displays whether the backend is reachable.

---

## Adding New Features

### New API route (backend)

1. Create `backend/app/api/routes/my_feature.py` with an `APIRouter`.
2. Register it in `backend/app/api/router.py`:
   ```python
   from app.api.routes import my_feature
   api_router.include_router(my_feature.router, prefix="/api/my-feature")
   ```

### New page (frontend)

Create `frontend/src/app/my-page/page.tsx` — Next.js App Router picks it up automatically at `/my-page`.

---

## Setup Steps Taken

The following steps were used to create this boilerplate:

1. **Created `backend/` directory structure** manually:
   `app/api/routes/`, `app/core/`, `app/models/`

2. **Written backend files:**
   - `requirements.txt` — pinned versions of fastapi, uvicorn, pydantic, pydantic-settings, python-dotenv, httpx
   - `app/core/config.py` — `pydantic-settings` `BaseSettings` class; reads `APP_NAME`, `APP_ENV`, `DEBUG`, `CORS_ORIGINS` from `.env`
   - `app/main.py` — FastAPI app with `CORSMiddleware` configured from settings
   - `app/api/router.py` — central `APIRouter` that registers sub-routers
   - `app/api/routes/health.py` — `GET /api/health` endpoint
   - `.env.example` — documents required env vars

3. **Scaffolded `frontend/` with `create-next-app`:**
   ```
   npx create-next-app@latest frontend \
     --typescript --tailwind --eslint --app --src-dir --no-import-alias --use-npm
   ```
   Options chosen: TypeScript ✓, Tailwind CSS ✓, ESLint ✓, App Router ✓, `src/` directory ✓, React Compiler ✗

4. **Added frontend glue code:**
   - `frontend/.env.local` — sets `NEXT_PUBLIC_API_URL`
   - `frontend/src/lib/api.ts` — typed `apiFetch` wrapper
   - Updated `frontend/src/app/page.tsx` — server component that calls the health endpoint and renders the result

5. **Added `.gitignore`** at root (covers both workspaces) and inside `backend/`.
