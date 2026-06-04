from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routers.auth import router as auth_router
from app.api.routers.profile import router as profile_router
from app.api.routers.membership import router as membership_router
from app.api.routers.gallery import router as gallery_router
from app.api.routers.image import router as image_router
from app.core.redis import redis_service

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
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(membership_router)
app.include_router(gallery_router)
app.include_router(image_router)