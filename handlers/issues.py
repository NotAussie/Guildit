from guilded_webhook import Embed


async def Issue(data: dict) -> Embed | None:

    action = data.get("action", "none")

    # Handle an issue being opened
    if action == "opened":
        # Create the embed
        embed = Embed(
            url=data["issue"]["html_url"],
            title=f"New issue #{data['issue']['number']}: {data['issue']['title']}",
            description=(data["issue"].get("body") or "*No description provided.*"),
        )

        # Set the author
        embed.set_author(
            name=data["issue"]["user"]["login"],
            icon_url=data["issue"]["user"]["avatar_url"],
            url=data["issue"]["user"]["html_url"],
        )

        return embed

    # Handle an issue being pinned
    elif action == "pinned":
        # Create the embed
        embed = Embed(
            url=data["issue"]["html_url"],
            title=f"Issue #{data['issue']['number']} has been pinned",
        )

        # Set the author
        embed.set_author(
            name=data["sender"]["login"],
            icon_url=data["sender"]["avatar_url"],
            url=data["sender"]["html_url"],
        )

        return embed

    # Handle an issue being closed
    elif action == "closed":
        # Create the embed
        embed = Embed(
            url=data["issue"]["html_url"],
            title=f"Issue #{data['issue']['number']} has been pinned",
        )

        # Set the author
        embed.set_author(
            name=data["sender"]["login"],
            icon_url=data["sender"]["avatar_url"],
            url=data["sender"]["html_url"],
        )

        return embed
