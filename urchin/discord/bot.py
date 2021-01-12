# Urchin - The resident urchin of The Tsunami Zone.
# Copyright (C) 2021  Ethan Henderson

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Ethan Henderson
# ethan.henderson.1998@gmail.com

from pathlib import Path

import discord
from aiohttp import ClientSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext import commands

from urchin import Config


class Bot(commands.Bot):
    __slots__ = ("extensions", "scheduler", "session")

    def __init__(self) -> None:
        self.extensions = [p.stem for p in Path(".").glob("./urchin/discord/extensions/*.py")]
        self.scheduler = AsyncIOScheduler()
        self.session = ClientSession()

        super().__init__(
            command_prefix=commands.when_mentioned_or(Config.DEFAULT_PREFIX),
            case_insensitive=True,
            status=discord.Status.dnd,
            intents=discord.Intents.all(),
        )

    def __call__(self) -> None:
        self.run()

    def setup(self) -> None:
        print("Running setup...")
        for ext in self.extensions:
            self.load_extension(f"urchin.discord.extensions.{ext}")
            print(f" `{ext}` extension loaded.")
        print("Setup complete.")

    def run(self) -> None:
        self.setup()
        print("Running bot...")
        super().run(Config.TOKEN, reconnect=True)

    async def close(self) -> None:
        print("Shutting down...")

        for cn, cog in self.cogs.items():
            if hasattr(cog, "on_close"):
                await cog.on_close()
                print(f" `{cn}` cog closed.")

        self.scheduler.shutdown()
        print(" Scheduler shut down.")
        await self.session.close()
        print(" HTTP session closed.")
        await super().close()
        print(" Bot shut down.")

    async def on_connect(self) -> None:
        print(f" Bot connected. DWSP latency: {self.latency * 1000:,.0f} ms.")

    async def on_disconnect(self) -> None:
        print(f" Bot disconnected.")

    async def on_ready(self) -> None:
        self.scheduler.start()
        print(f" Scheduler started ({len(self.scheduler.get_jobs())} jobs scheduled).")
        print(" Bot ready.")

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or isinstance(message.channel, discord.DMChannel):
            return

        await self.process_commands(message)

    async def on_error(self, err: str, ctx: commands.Context, exc: Exception, **kwargs) -> None:
        raise getattr(exc, "original", exc)

    async def on_command_error(self, ctx: commands.Context, exc: commands.CommandError) -> None:
        raise getattr(exc, "original", exc)

    async def process_commands(self, message: discord.Message) -> None:
        ctx = await self.get_context(message, cls=commands.Context)

        if ctx.command is None:
            return

        await self.invoke(ctx)
