import asyncio
from MeowCore import MeowCore


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
