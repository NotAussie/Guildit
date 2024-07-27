# FastAPI imports
from re import I
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi_limiter.depends import RateLimiter

# Utility imports
from handlers import handlers
from config import config
from utilities.poster import post
import json
import logfire

# Create router
router = APIRouter()


# Create /webhooks
@router.post(
    "/webhooks/{id}/{token}",
    dependencies=[Depends(RateLimiter(times=15, seconds=15))],
    summary="A drop in translation layer for GitHub webhooks",
    description='This route is a replacement for "https://media.guilded.gg/webhooks/id/token/github" as it\'s no longer supported, simply replace "https://media.guilded.gg/webhooks/" with "https://guildit.dev/webhooks/".',
)
async def webhooks(id: str, token: str, request: Request):
    # Attempt to decode the body
    try:
        data = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(422, "Failed to decode json data")

    # Handle malformed hook information
    if len(token) < 86 or len(token) > 86:
        raise HTTPException(400, "Malformed webhook token")

    elif len(id) < 36 or len(id) > 36:
        raise HTTPException(400, "Malformed webhook id")

    # Get the event handler
    logfire.info(request.headers.get("X-GitHub-Event", "None"))
    handler = handlers.get(request.headers.get("X-GitHub-Event", "None"), None)
    if handler == None:  # Handle the event not being implemented
        raise HTTPException(
            501,
            f"Event type \"{request.headers.get('X-GitHub-Event', 'None')}\" isn't supported",
        )

    # Detect the repo and branch
    name = data["repository"].get("full_name")
    branch = None
    footer = f"{name}{'+' + branch if branch else ''}"

    print(await handler(data))

    # Post the event in a try block
    try:
        await post(
            url=config["guilded"]["webhookApi"].format(id, token),
            embed=await handler(data),
            footer=footer,
            name="Guildit",
        )

    # Handle missing key errors
    except KeyError:
        raise HTTPException(
            422,
            f"Event payload is missing expected value(s)",
        )

    return {"details": "Added to queue"}, 200
