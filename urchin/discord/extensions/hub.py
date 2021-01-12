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

import discord
from discord.ext import commands

from urchin import Config
from urchin.constants import VERSION


class Hub(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        if self.bot.ready.hub:
            return

        self.guild = self.bot.get_guild(Config.HUB_GUILD_ID)
        if self.guild:
            self.commands = self.guild.get_channel(Config.HUB_COMMANDS_CHANNEL_ID)
            self.stdout = self.guild.get_channel(Config.HUB_STDOUT_CHANNEL_ID)
            if self.stdout:
                await self.stdout.send(f"{self.bot.user.display_name} is now online! (Version {VERSION})")

        self.bot.ready.extension(self)

    async def on_close(self) -> None:
        await self.stdout.send(f"{self.bot.user.display_name} is shutting down. (Version {VERSION})")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        if self.bot.user in message.mentions or "all" in message.content:
            if message.channel == self.commands:
                if message.content.lower().startswith("shutdown"):
                    await self.bot.close()


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Hub(bot))
