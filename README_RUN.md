# How to Run the App

## Quick Start (Windows)
Double-click the **`start_app.bat`** file in this directory. 
It will automatically open two terminal windows: one for the backend and one for the frontend.

## Manual Start

### 1. Backend (FastAPI)
Open a terminal and run:
```bash
cd backend
# Make sure your virtual environment is active if you use one
python -m uvicorn app.main:app --reload --port 8001
```

### 2. Frontend (Next.js)
Open a new terminal and run:
```bash
cd frontend
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.
