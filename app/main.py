from fastapi import FastAPI
from app.routers import campaigns

app = FastAPI(title="Media Campaign API", version="1.0.0")

app.include_router(campaigns.router)


@app.get("/health")
def health_check():
    return { "status": "ok" }