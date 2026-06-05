from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.routers.auth import router as auth_router
from app.api.routers.profile import router as profile_router
from app.api.routers.membership import router as membership_router
from app.api.routers.gallery import router as gallery_router
from app.api.routers.image import router as image_router
from app.core.redis import redis_service
from app.core.config import settings

import app.models.user        # noqa: F401
import app.models.gallery     # noqa: F401
import app.models.membership  # noqa: F401
import app.models.image       # noqa: F401

@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_service.connect()
    yield
    await redis_service.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(membership_router)
app.include_router(gallery_router)
app.include_router(image_router)

app.mount("/uploads", StaticFiles(directory=Path(__file__).parent / "uploads"), name="uploads")