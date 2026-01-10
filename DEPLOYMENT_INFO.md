
# Deployment Guide: Quantum Learning Platform

This guide covers deploying the Next.js Frontend and FastAPI Backend.

## 1. Architecture Overview

- **Frontend**: Next.js (Static/Serverless) -> Deployed to Vercel or AWS Amplify.
- **Backend**: FastAPI (Python) -> Deployed to AWS App Runner, ECS, or Vercel (Python Runtimes).
- **Database**: MongoDB -> MongoDB Atlas (Cloud).

---

## 2. Frontend Deployment (Vercel) - Recommended

Vercel is the creators of Next.js and offers the seamless deployment.

1.  **Push code to GitHub/GitLab**.
2.  **Log in to Vercel** and "Add New Project".
3.  **Import your repository** (`qml-qkd-app/frontend`).
4.  **Configure Build Settings**:
    - Framework Preset: Next.js (Automatic)
    - Root Directory: `frontend`
5.  **Environment Variables**:
    - Add `NEXT_PUBLIC_API_URL` pointing to your deployed backend URL (e.g., `https://api.quantum-platform.com`).
    - *Note*: You need to update `src/lib/api.ts` to use this environment variable instead of hardcoded `localhost`.
6.  **Deploy**.

## 3. Backend Deployment (AWS App Runner)

AWS App Runner is the easiest way to deploy containerized web applications.

### Prerequisites
- Docker installed.
- AWS CLI configured.

### Steps
1.  **Containerize the Backend**:
    Create a `Dockerfile` in the `backend` directory:
    ```dockerfile
    FROM python:3.9
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    COPY . .
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    ```

2.  **Push to ECR (Elastic Container Registry)**:
    ```bash
    aws ecr create-repository --repository-name quantum-backend
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
    docker build -t quantum-backend ./backend
    docker tag quantum-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/quantum-backend:latest
    docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/quantum-backend:latest
    ```

3.  **Create App Runner Service**:
    - Go to AWS Console -> App Runner.
    - Source: Container Registry (ECR).
    - Configure Service:
        - Environment Variables: `MONGO_URI`, `DB_NAME`.
        - Port: `8000`.
    - Deploy.

4.  **Update Frontend**:
    - Take the App Runner URL (e.g., `https://xyz.awsapprunner.com`).
    - Update frontend `NEXT_PUBLIC_API_URL` env var.

---

## 4. Frontend Deployment (AWS Amplify)

If you prefer full AWS ecosystem:

1.  Go to **AWS Amplify Console**.
2.  **New App** -> Host web app.
3.  Connect Repostiory.
4.  **Build Settings**:
    - Base Directory: `frontend`.
    - Build Command: `npm run build`.
5.  **Environment Variables**:
    - `NEXT_PUBLIC_API_URL`: Your backend URL.
6.  **Deploy**.

---

## 5. Configuration Update Required

Before deployment, update `src/lib/api.ts` to use environment variables:

```typescript
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001";
```

Ensure your backend has CORS configured to allow the frontend domain.
