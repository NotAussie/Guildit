# `📁` Guildit *[Server]*
Guildit's webhook middleman. 🔌

## `📡` How does it work?

Guildit’s webhook system works like this: When a new webhook event is published, we automatically convert GitHub’s unsupported webhook into a Guilded webhook. Once the webhook is ready to be sent out, we add it to our webhook queue. This queue helps us avoid rate limits by keeping webhook posts at a steady pace.

## `📃` Credits

- [FastAPI](https://pypi.org/project/fastapi/) - Webserver.
- [Smee.io](https://smee.io/) - Webhook testing.