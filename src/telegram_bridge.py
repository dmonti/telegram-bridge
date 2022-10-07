import logging as log
from time import sleep

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

    def __init__(self, client: TelegramClient,
                 source_channel_id: int,
                 target_channel_id: int,
                 last_message_id=None,
                 interval_secs=60):
        self.client = client
        self.source_channel_id = source_channel_id
        self.target_channel_id = target_channel_id
        self.last_message_id = last_message_id
        self.interval_secs = interval_secs
        self.running = False

    async def start(self):
        self.running = True
        log.info("Starting TelegramBridge monitor")
        if self.client.disconnected:
            await self.client.connect()

        source_channel = PeerChannel(self.source_channel_id)
        source_entity = await self.client.get_entity(source_channel)
        target_channel = PeerChannel(self.target_channel_id)
        target_entity = await self.client.get_entity(target_channel)

        log.info(f"TelegramBridge looking group {source_entity.title} for messages")
        while self.running:
            min_id = self.last_message_id
            async for message in self.client.iter_messages(source_entity, min_id=min_id, reverse=True):
                log.info(f"New message received #{message.id}")
                await self.send_message_channel(message, target_entity)
                self.last_message_id = message.id

            sleep(self.interval_secs)

        log.info("Telegram monitor stopped")

    async def send_message_channel(self, message, channel: Channel):
        client = self.client
        await client.send_message(channel.id, message.message)
        for link in map_to_links(message.buttons):
            await client.send_message(channel.id, link, link_preview=False)

        log.info(f"New message #{message.id} sent to {channel.title}")

    def stop(self):
        self.running = False
        log.info("Stopping telegram monitor...")
