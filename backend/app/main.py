from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
app=FastAPI(title="Verba API",version="0.1.0",description="REST API for English speaking practice.")
app.add_middleware(CORSMiddleware,allow_origins=[x.strip() for x in settings.cors_origins.split(',')],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
@app.get("/health",tags=["system"])
def health(): return {"status":"ok"}
@app.post("/auth/register",tags=["auth"])
def register(): return {"detail":"Authentication endpoint scaffolded; connect repository and password service."}
@app.post("/auth/login",tags=["auth"])
def login(): return {"detail":"Authentication endpoint scaffolded; connect repository and JWT service."}
@app.get("/lessons",tags=["lessons"])
def lessons(): return []
