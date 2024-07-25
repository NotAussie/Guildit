# FastAPI imports
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi_limiter.depends import RateLimiter

# Utility imports
from handlers import handlers
from config import config
from utilities.queue import Queue

# Create router
router = APIRouter()

# Create the queue
queue = Queue()


# Create /webhooks
@router.post(
    "/webhooks/{hookId}/{hookToken}",
    dependencies=[Depends(RateLimiter(times=15, seconds=15))],
)
async def webhooks(hookId: str, hookToken: str, request: Request):
    print(request.headers.get("X-GitHub-Event", "None"))
    # Handle malformed hook information
    if len(hookToken) < 86 or len(hookToken) > 86:
        raise HTTPException(400, "Malformed webhook token")

    elif len(hookId) < 36 or len(hookId) > 36:
        raise HTTPException(400, "Malformed webhook id")

    # Get the event handler
    handler = handlers.get(request.headers.get("X-GitHub-Event", "None"), None)
    if handler == None:  # Handle the event not being implemented
        raise HTTPException(
            501,
            f"Event type \"{request.headers.get('X-GitHub-Event', 'None')}\" isn't supported",
        )

    await queue.add(
        url=f"{config['guilded']['webhookApi']}/{hookId}/{hookToken}",
        embed=await handler(data=await request.json()),
    )

    return {"details": "Added to queue"}, 200
