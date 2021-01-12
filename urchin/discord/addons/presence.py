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

from itertools import cycle

import discord
from apscheduler.triggers.cron import CronTrigger
from discord.ext import commands

from urchin import Config
from urchin.constants import VERSION


class PresenceUpdater:
    __slots__ = ("bot", "_name", "_messages")

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self._name = "{}help • {} • Version {}"
        self._messages = cycle(("The new spikey boi on the block",))

        bot.scheduler.add_job(self.cycle, CronTrigger(second=0))

    @property
    def name(self) -> str:
        return self._name.format(Config.DEFAULT_PREFIX, next(self._messages), VERSION)

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    async def cycle(self) -> None:
        await self.bot.change_presence(activity=discord.Activity(name=self.name, type=discord.ActivityType.watching))
