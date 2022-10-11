import asyncio
import logging as log

from telethon import TelegramClient
from telethon.tl.types import PeerChannel

from config import Config
from kvdb import KvdbClient
from telegram_bridge import TelegramBridge

log.basicConfig(
    level=log.INFO,
    filename="application.log",
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

_loop = asyncio.new_event_loop()
asyncio.set_event_loop(_loop)


class Application:
    def __init__(self):
        self.config = Config()

        bucket_id = self.config.get('kvdb', 'bucket_id')
        self.kvdb = KvdbClient(bucket_id)

        session_path = self.config.get('telegram', 'session_path')
        api_id = self.config.get_int('telegram', 'api_id')
        api_hash = self.config.get('telegram', 'api_hash')
        self.telegram = TelegramClient(session_path, api_id, api_hash, loop=_loop)

        self.last_message_id = None
        self.source_group_ids = self.config.get('bridge', 'source_group_ids')
        self.target_group_ids = self.config.get('bridge', 'target_group_ids')

    async def run(self):
        log.info("Starting telegram client")
        phone_number = self.config.get('telegram', 'phone_number')
        await self.telegram.start(phone=phone_number)

        source_ids = self.source_group_ids.split(',')
        target_ids = self.target_group_ids.split(',')
        for i, source_id in enumerate(source_ids):
            target_id = target_ids[i]

            source_entity = await self.telegram.get_entity(PeerChannel(int(source_id)))
            log.debug(f"Source entity: {source_entity}")
            target_entity = await self.telegram.get_entity(PeerChannel(int(target_id)))
            log.debug(f"Target entity: {target_entity}")

            last_message_id = self.kvdb.get_int(source_entity.id)
            if last_message_id is None:
                last_message_id = 0

            bridge = TelegramBridge(self.telegram, source_entity, target_entity, last_message_id)
            asyncio.ensure_future(
                bridge.start(
                    interval_secs=10,
                    update_event=lambda b: self.kvdb.set(b.source_entity.id, b.last_message_id)
                ), loop=_loop
            )


if __name__ == "__main__":
    log.info("Initializing application...")
    try:
        app = Application()
        _loop.create_task(app.run(), name='main')
        _loop.run_forever()
    except Exception as e:
        log.error(e)
