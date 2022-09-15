import nats
import asyncio
from logging import info
from diff.config import NatsConfig


async def nats_connect(url: str):
    info("Connecting to NATS")
    return await nats.connect(url)


queues = ["diffusion", "upscale", "video", "audio"]


async def _setup_stream(url: str):
    nc = await nats_connect(url)
    js = nc.jetstream()

    for q in queues:
        queue = f"tasks-{q}"
        info(f"Setting up NATS stream for {queue}")
        await js.add_stream(name=f"tasks-stream-{queue}", subjects=[queue])


def add_stream(cfg: NatsConfig):
    asyncio.run(_setup_stream(cfg.url()))
