# FastAPI imports
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.logger import logger
from fastapi.staticfiles import StaticFiles

# Ratelimiter imports
from fastapi_limiter import FastAPILimiter
from contextlib import asynccontextmanager
import redis.asyncio as redis

# Logfire imports
import logfire
from logging import basicConfig, StreamHandler

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
    summary="We enforce rate limits, please do not spam our API or you will be blocked.",
    description="All public Guildit routes...",
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
)
app.mount(
    "/assets", StaticFiles(directory="assets"), name="assets"
)  # Mount the assets directory

# Setup logfire
if config["logfire"]["enabled"]:
    logfire.configure(
        token=config["logfire"]["token"],
        pydantic_plugin=logfire.PydanticPlugin(record="all"),
    )
    basicConfig(handlers=[logfire.LogfireLoggingHandler()])
    logger.addHandler(logfire.LogfireLoggingHandler())
    logger.addHandler(StreamHandler())
    logfire.instrument_fastapi(app, capture_headers=True)
    logfire.instrument_redis()
    logfire.instrument_aiohttp_client()
    logfire.install_auto_tracing(
        modules=[
            "handlers",
            "utilities",
        ]
    )

# Import routers
from routers.webhook import router as webhook
from routers.pages import router as pages

# Include routers
app.include_router(webhook)
app.include_router(pages)


@app.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Guildit",
        swagger_favicon_url="/assets/guildit.webp",
    )
