# Deployment Instructions

## Frontend (Next.js) -> Vercel

1. Push this repository to GitHub/GitLab/Bitbucket.
2. Log in to [Vercel](https://vercel.com).
3. Import the project.
4. Select `frontend` as the Root Directory.
5. Framework Preset: Next.js (should auto-detect).
6. Build Command: `npm run build` (default).
7. Output Directory: `.next` (default).
8. **Environment Variables**:
   - `NEXT_PUBLIC_API_URL`: URL of your deployed backend (e.g. `https://my-backend.onrender.com`).
   - Note: You need to update the frontend code to use this variable instead of hardcoded `http://127.0.0.1:8000` before deploying!

## Backend (FastAPI) -> AWS / Render / Railway

### AWS EC2
1. Launch an EC2 instance (Ubuntu/Linux).
2. SSH into the instance.
3. Clone the repo.
4. Install Python 3 and pip.
5. `cd backend`
6. `pip install -r requirements.txt`
7. `uvicorn app.main:app --host 0.0.0.0 --port 8000`
8. Configure Security Group to allow inbound traffic on port 8000.

### Docker
1. Build image: `docker build -t qml-qkd-backend .`
2. Run container: `docker run -d -p 8000:8000 qml-qkd-backend`
