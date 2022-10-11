import asyncio
import logging as log

from telethon import TelegramClient
from telethon.tl.types import PeerChannel, Channel


def map_to_links(buttons):
    links = []
    if buttons is None:
        return links
    for button in buttons:
        for link in button:
            links.append(link.url)
    return links


class TelegramBridge:

    def __init__(self, client: TelegramClient, source_entity, target_entity, last_message_id: int):
        self.running = False
        self.client = client
        self.source_entity = source_entity
        self.target_entity = target_entity
        self.last_message_id = last_message_id

    async def start(self, update_event=None, interval_secs=60):
        self.running = True
        min_id = self.last_message_id

        log.info(f"""
        Starting bridge with ID #{min_id} (min_id)
        Source group: {self.source_entity.title} #{self.source_entity.id}
        Target group: {self.target_entity.title} #{self.target_entity.id}""")
        await asyncio.sleep(3)

        while self.running:
            async for message in self.client.iter_messages(self.source_entity, min_id=min_id, reverse=True):
                log.info(f"New message received #{message.id}")
                await self.send_message_channel(message, self.target_entity)
                self.last_message_id = message.id

            if min_id < self.last_message_id:
                min_id = self.last_message_id
                update_event(self)

            log.debug(f"Waiting {interval_secs}s")
            await asyncio.sleep(interval_secs)

        log.info("Telegram monitor stopped")

    async def send_message_channel(self, message, channel: Channel):
        await self.client.send_message(channel.id, message.message)
        for link in map_to_links(message.buttons):
            await self.client.send_message(channel.id, link, link_preview=False)
        log.info(f"New message #{message.id} sent to {channel.title}")

    async def get_group_entity(self, group_id):
        channel = PeerChannel(group_id)
        return await self.client.get_entity(channel)

    def stop(self):
        self.running = False
        log.info("Stopping telegram monitor...")
