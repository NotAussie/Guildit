This directory contains handlers for *all* of GitHub's actions.

Each handler must return a `guilded_webhook.Embed` or `None`.

If you're registering a new handler add it to the `handlers` dictionary in `__init__.py`, make sure to put the `X-GitHub-Event` for it's name.