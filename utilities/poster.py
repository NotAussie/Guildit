"""Handler for our webhooks"""

# Import types
from guilded_webhook import Embed, AsyncWebhook
from fastapi import HTTPException
from assets import guilditLogo, guilditIcon
from datetime import datetime, timezone


async def post(
    url: str,
    embed: Embed | None,
    action: str,
    footer: str,
) -> None:
    """Handles any pre-processing then posts to Guilded"""
    hook = AsyncWebhook(
        url=url,
        avatar=guilditIcon,
        username="guildit.dev",
    )

    if embed is None:
        raise HTTPException(501, f'Event action "{action}" isn\'t supported')
    assert embed != None  # This is a fail safe that should NEVER trigger

    if not embed._timestamp:
        embed._timestamp = datetime.now(timezone.utc)

    embed._footer["text"] = footer
    embed._footer["iconUrl"] = guilditLogo
    embed._color = 0x373943

    await hook.send(embeds=[embed])
