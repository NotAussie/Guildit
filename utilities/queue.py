"""Handler for our webhook queue"""

# Import types
from guilded_webhook import Embed, AsyncWebhook
from fastapi import HTTPException
from assets import guilditLogo, octocatAnimation
from datetime import datetime, timezone


class Queue:
    def __init__(self, maxSize: int = 100) -> None: ...

    async def add(self, url: str, embed: Embed) -> None:
        hook = AsyncWebhook(url=url, username="Guildit", avatar=octocatAnimation)

        embed._timestamp = datetime.now(timezone.utc)
        embed.set_footer(text="Powered by Guildit.dev", icon_url=guilditLogo)

        await hook.send(embeds=[embed])
