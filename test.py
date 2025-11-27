import asyncio
from MeowCore import MeowCore
import logging
import sys


FORMAT = "[TEST] %(message)s"
logging.basicConfig(
    handlers=[logging.FileHandler("logs.txt"), logging.StreamHandler()],
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
)

LOGGER = logging.getLogger("TEST")


async def aa():
    MeowClient = MeowCore(
        api_key="test-rj",
        bot_name="iSHiKKiBot",
    )
    await asyncio.sleep(10)
    print("hoi")


asyncio.run(aa())

