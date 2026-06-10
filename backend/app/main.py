import nltk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import detect, humanize
from app.core.config import settings

# Pre-download NLTK data at startup
for _pkg in ("punkt", "punkt_tab", "stopwords"):
    try:
        nltk.data.find(f"tokenizers/{_pkg}" if "punkt" in _pkg else f"corpora/{_pkg}")
    except LookupError:
        nltk.download(_pkg, quiet=True)

app = FastAPI(
    title="DetectAI API",
    description="Multi-layer AI text detection and humanization engine",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url,
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(detect.router, prefix="/api/v1", tags=["Detection"])
app.include_router(humanize.router, prefix="/api/v1", tags=["Humanization"])


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "version": "1.0.0"}
