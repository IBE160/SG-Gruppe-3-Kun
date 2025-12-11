from fastapi import FastAPI
from app.api.v1.endpoints import health

app = FastAPI()

app.include_router(health.router, prefix="/api/v1/health", tags=["health"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}
