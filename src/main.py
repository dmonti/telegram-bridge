import asyncio

from telethon import TelegramClient

from config import Config
from kvdb import KvdbClient
from telegram_bridge import TelegramBridge

config = Config()

kvdb_bucket_id = config.get('kvdb', 'bucket_id')

session_path = config.get('telegram', 'session_path')
api_id = config.get_int('telegram', 'api_id')
api_hash = config.get('telegram', 'api_hash')

source_group_id = config.get_int('betty', 'source_group_id')
target_group_id = config.get_int('betty', 'target_group_id')

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def main():
    print("Starting telegram client")
    telegram = TelegramClient(session_path, api_id, api_hash, loop=loop)
    telegram.start()

    kvdb = KvdbClient(kvdb_bucket_id)
    last_message_id = kvdb.get_int("last-message-id")

    bridge = TelegramBridge(telegram, target_group_id, source_group_id, last_message_id=last_message_id)
    asyncio.ensure_future(bridge.start(), loop=loop)


if __name__ == "__main__":
    try:
        loop.create_task(main(), name='main')
        loop.run_forever()
    except Exception as e:
        print(e)
