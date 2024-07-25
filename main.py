# FastAPI imports
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.logger import logger

# Ratelimiter imports
from fastapi_limiter import FastAPILimiter
from contextlib import asynccontextmanager
import redis.asyncio as redis

# Logfire imports
from logging import basicConfig, StreamHandler
from logfire import configure, instrument_fastapi, LogfireLoggingHandler, PydanticPlugin

# Utility imports
import subprocess
from config import config

# Get the SHA
sha = subprocess.check_output(
    ["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.STDOUT, text=True
).strip()

# Get the current branch
branch = subprocess.check_output(
    ["git", "rev-parse", "--abbrev-ref", "HEAD"],
    stderr=subprocess.STDOUT,
    text=True,
).strip()


# Setup rate limiting
@asynccontextmanager
async def lifespan(_: FastAPI):
    connection = redis.from_url(config["redis"]["uri"], encoding="utf8")
    await FastAPILimiter.init(connection)
    yield
    await FastAPILimiter.close()


# Create app
app = FastAPI(
    title="Guildit",
    version=f"{branch.title()} ({sha})",
    description="All public GuilIt routes",
    lifespan=lifespan,
)

# Setup logfire
if config["logfire"]["enabled"]:
    configure(
        token=config["logfire"]["token"],
        pydantic_plugin=PydanticPlugin(record="all"),
    )
    basicConfig(handlers=[LogfireLoggingHandler()])
    logger.addHandler(LogfireLoggingHandler())
    logger.addHandler(StreamHandler())
    instrument_fastapi(app, capture_headers=True)


# Import routers
from routers.webhook import router as webhook

# Include routers
app.include_router(webhook)


# Convert / into a redirect
@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse("/docs")
