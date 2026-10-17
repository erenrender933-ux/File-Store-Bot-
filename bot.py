from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, DB_CHANNEL


class Bot(Client):
    def __init__(self):
        super().__init__(
            "FileStoreBot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="plugins"),
            workers=50,
        )

    async def start(self, *args, **kwargs):
        await super().start(*args, **kwargs)
        try:
            test = await self.send_message(DB_CHANNEL, "✅ Bot started")
            await test.delete()
        except Exception as e:
            print(f"[ERROR] Cannot access DB_CHANNEL ({DB_CHANNEL}): {e}")
        print(f"Bot started as @{self.me.username}")

    async def stop(self, *args, **kwargs):
        await super().stop(*args, **kwargs)
        print("Bot stopped")


if __name__ == "__main__":
    Bot().run()
