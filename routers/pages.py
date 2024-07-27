# FastAPI imports
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

# Utility imports
from config import config

# Create router
router = APIRouter()

# Create the templates object
templates = Jinja2Templates(directory="pages")


@router.get("/", include_in_schema=False)
async def home(request: Request):

    return templates.TemplateResponse(request=request, name="landing.html")
