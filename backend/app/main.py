from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from datetime import datetime

# =========================================================
# CONFIGURATION
# =========================================================

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "quantum_learning")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI environment variable not set")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="Quantum Learning Platform API",
    description="Backend API for QML & QKD Learning Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OK for now (restrict later)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# MODELS
# =========================================================

class ProgressUpdate(BaseModel):
    domain: str
    slug: str
    readCompleted: bool
    quizCompleted: bool
    quizScore: float = 0.0

# =========================================================
# ROOT
# =========================================================

@app.get("/")
async def root():
    return {
        "status": "running",
        "database": DB_NAME,
        "modules": ["QML", "QKD"]
    }

# =========================================================
# QML
# =========================================================

@app.get("/api/qml/introduction")
async def qml_introduction():
    doc = await db.qml_introduction.find_one({}, {"_id": 0})
    if not doc:
        raise HTTPException(404, "QML introduction not found")
    return doc

@app.get("/api/qml/workflow")
async def qml_workflow():
    doc = await db.qml_workflow.find_one({}, {"_id": 0})
    if not doc:
        raise HTTPException(404, "QML workflow not found")
    return doc

@app.get("/api/qml/domains")
async def qml_domains():
    domains = await db.qml_algorithms.distinct("domain_slug")
    return [{"slug": d, "title": d.replace("-", " ").title()} for d in domains]

@app.get("/api/qml/domains/{domain_slug}")
async def qml_domain(domain_slug: str):
    algorithms = await db.qml_algorithms.find(
        {"domain_slug": domain_slug}, {"_id": 0}
    ).to_list(None)

    if not algorithms:
        raise HTTPException(404, "No algorithms found")

    return {
        "domain": {"slug": domain_slug, "title": domain_slug.replace("-", " ").title()},
        "algorithms": algorithms
    }

@app.get("/api/qml/algorithms/{slug}")
async def qml_algorithm(slug: str):
    algo = await db.qml_algorithms.find_one({"slug": slug}, {"_id": 0})
    if not algo:
        raise HTTPException(404, "Algorithm not found")
    return algo

# =========================================================
# QKD
# =========================================================

@app.get("/api/qkd/introduction")
async def qkd_introduction():
    doc = await db.qkd_introduction.find_one({}, {"_id": 0})
    if not doc:
        raise HTTPException(404, "QKD introduction not found")
    return doc

@app.get("/api/qkd/workflow")
async def qkd_workflow():
    doc = await db.qkd_workflow.find_one({}, {"_id": 0})
    if not doc:
        raise HTTPException(404, "QKD workflow not found")
    return doc

@app.get("/api/qkd/domains")
async def qkd_domains():
    domains = await db.qkd_protocols.distinct("domain_slug")
    return [{"slug": d, "title": d.replace("-", " ").title()} for d in domains]

@app.get("/api/qkd/domains/{domain_slug}")
async def qkd_domain(domain_slug: str):
    protocols = await db.qkd_protocols.find(
        {"domain_slug": domain_slug}, {"_id": 0}
    ).to_list(None)

    if not protocols:
        raise HTTPException(404, "No protocols found")

    return {
        "domain": {"slug": domain_slug, "title": domain_slug.replace("-", " ").title()},
        "protocols": protocols
    }

@app.get("/api/qkd/protocols/{slug}")
async def qkd_protocol(slug: str):
    protocol = await db.qkd_protocols.find_one({"slug": slug}, {"_id": 0})
    if not protocol:
        raise HTTPException(404, "Protocol not found")
    return protocol

# =========================================================
# USER PROGRESS
# =========================================================

@app.post("/api/me/progress")
async def update_progress(update: ProgressUpdate):
    user_id = "default_user"

    await db.user_progress.update_one(
        {"user_id": user_id, "slug": update.slug},
        {"$set": {
            "domain": update.domain,
            "read_completed": update.readCompleted,
            "quiz_completed": update.quizCompleted,
            "quiz_score": update.quizScore,
            "updated_at": datetime.utcnow()
        }},
        upsert=True
    )

    return {"status": "success"}
