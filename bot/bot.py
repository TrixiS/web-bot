import logging

from pathlib import Path
from typing import List

import discord

from discord.ext import commands

from .context import BotContext
from bot import root_path
from app.web_config import WebConfig, Phrases, Config


def get_all_extensions(cogs_path: Path):
    ext_paths = (
        p for p in cogs_path.glob("*.py") if p.is_file() and not p.name.startswith("_")
    )
    return [f"bot.cogs.{p.stem}" for p in ext_paths]


class Bot(commands.AutoShardedBot):
    def __init__(self, web_config: WebConfig, *args, **kwargs):
        super().__init__(
            *args,
            command_prefix=get_command_prefix,
            intents=discord.Intents.all(),
            **kwargs,
        )
        self.web_config = web_config
        self.logger = logging.getLogger("bot")

        for ext in get_all_extensions(root_path / "bot/cogs"):
            self.load_extension(ext)

    @property
    def config(self) -> Config:
        return self.web_config.config

    @property
    def phrases(self) -> Phrases:
        return self.web_config.phrases

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
