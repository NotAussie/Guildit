from guilded_webhook import Embed


async def Meta(data: dict) -> Embed | None:

    action = data.get("action", "none")

    if action == "deleted":  # Deleted is currently the only supported action for this
        return Embed(
            url=data["repository"]["html_url"],
            title=f"Goodbye!",
            description="Thanks for using `guildit.dev`, your webhook has been disconnected.",
        )
