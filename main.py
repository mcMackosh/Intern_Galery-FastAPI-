from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routers.auth import router as auth_router
from app.api.routers.profile import router as profile_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(profile_router)
