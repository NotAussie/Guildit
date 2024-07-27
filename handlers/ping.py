from guilded_webhook import Embed
from assets import guilditLogo
from datetime import datetime, timezone


async def Ping(data: dict) -> Embed | None:
    return Embed(
        title="GitHub ping!",
        description="Congrats, your webhook is all set-up! :partying_face:"
        f"\nThis channel will now recive events from [`{data['repository']['full_name']}`]({data['repository']['html_url']}).",
    )
