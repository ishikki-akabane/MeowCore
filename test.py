import asyncio
from MeowCore import MeowCore
import logging
import sys


FORMAT = "[TEST] %(message)s"
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
logging.basicConfig(
    handlers=[
        logging.FileHandler("logs.txt", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
    force=True,
)


LOGGER = logging.getLogger('[TEST]')


async def aa():
    MeowClient = MeowCore(
        api_key="test-rj",
        bot_name="iSHiKKiBot",
    )
    await asyncio.sleep(10)
    print("hoi")


asyncio.run(aa())

