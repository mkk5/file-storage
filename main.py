from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import files, html


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(files.router)
app.include_router(html.router)
