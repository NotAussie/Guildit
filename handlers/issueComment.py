from guilded_webhook import Embed
from difflib import ndiff
import re


async def issueComment(data: dict) -> Embed | None:

    action = data.get("action", "none")

    # Handle a comment being created
    if action == "created":
        # Create the embed
        embed = Embed(
            url=data["comment"]["html_url"],
            title=f"New comment in issue #{data['issue']['number']}: {data['issue']['title']}",
            description=(
                data["comment"]["body"]
                if len(data["comment"]["body"]) < 2048
                else "*Difference was longer then __2048__ characters.*"
            ),
        )

        # Set the author
        embed.set_author(
            name=data["comment"]["user"]["login"],
            icon_url=data["comment"]["user"]["avatar_url"],
            url=data["comment"]["user"]["html_url"],
        )

        return embed

    # Handle a comment being deleted
    elif action == "deleted":
        # Create the embed
        embed = Embed(
            url=data["comment"]["html_url"],
            title=f"Comment deleted in issue #{data['issue']['number']}: {data['issue']['title']}",
            description=(
                data["comment"]["body"]
                if len(data["comment"]["body"]) < 2048
                else "*Difference was longer then __2048__ characters.* "
            ),
        )

        # Set the author
        embed.set_author(
            name=data["comment"]["user"]["login"],
            icon_url=data["comment"]["user"]["avatar_url"],
            url=data["comment"]["user"]["html_url"],
        )

        return embed

    # Handle a comment being edited
    elif action == "edited":
        # Create the message
        diff = "\n".join(
            [
                line
                for line in ndiff(
                    str(data["changes"]["body"]["from"]).splitlines(),
                    str(data["comment"]["body"]).splitlines(),
                )
                if not re.match(r"^\?", line)
            ]
        )

        # Create the embed
        embed = Embed(
            url=data["comment"]["html_url"],
            title=f"Comment edited in issue #{data['issue']['number']}: {data['issue']['title']}",
            description=(
                f"```diff\n{diff}\n```"
                if len(f"```diff\n{diff}\n```") < 2048
                else "*Difference was longer then __2048__ characters.* "
            ),
        )

        # Set the author
        embed.set_author(
            name=data["comment"]["user"]["login"],
            icon_url=data["comment"]["user"]["avatar_url"],
            url=data["comment"]["user"]["html_url"],
        )

        return embed
