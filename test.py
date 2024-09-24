import asyncio
from MeowCore import MeowCore
import logging


FORMAT = "[TEST] %(message)s"
logging.basicConfig(
    handlers=[logging.FileHandler("logs.txt"), logging.StreamHandler()],
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
)

LOGGER = logging.getLogger('[TEST]')

async def aa():
    MeowClient = MeowCore(
        "69696969-MeowMeow",
        category="telegram",
        bot_id="123456789",
        bot_username="iSHiKKiBot"
    )
    await MeowClient.load_welcome(["x00xhaha"])

    print("hoi")

asyncio.run(aa())
