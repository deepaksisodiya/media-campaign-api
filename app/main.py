from fastapi import FastAPI
from app.routers import campaigns
from app.routers import analyse

app = FastAPI(title="Media Campaign API", version="1.0.0")

app.include_router(campaigns.router)
app.include_router(analyse.router)


@app.get("/health")
def health_check():
    return { "status": "ok" }