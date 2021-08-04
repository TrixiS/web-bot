import logging

from typing import List

import discord

from discord.ext import commands

from .context import BotContext
from app.web_config import WebConfig


class Bot(commands.AutoShardedBot):
    def __init__(self, web_config: WebConfig, *args, **kwargs):
        super().__init__(
            *args,
            command_prefix=get_command_prefix,
            intents=discord.Intents.all(),
            **kwargs
        )
        self.config = web_config.config
        self.phrases = web_config.phrases
        self.logger = logging.getLogger("bot")

    def run(self):
        super().run(self.config.bot_token, bot=True)

    async def close(self):
        for cog in self.cogs.values():
            await cog.on_bot_close()

        await super().close()

    async def process_commands(self, message: discord.Message):
        ctx: BotContext = await self.get_context(message, cls=BotContext)

        if ctx.command is None:
            return

        await self.invoke(ctx)

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        await self.process_commands(message)


async def get_command_prefix(bot: Bot, message: discord.Message) -> List[str]:
    return bot.config.command_prefixes
