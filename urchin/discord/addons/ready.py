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

from discord.ext import commands


class ReadyStatusTracker:
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
        self.booted = False

        for ext in self.bot.extensions:
            setattr(self, ext, False)

    def extension(self, cog: commands.Cog) -> None:
        setattr(self, (qn := cog.qualified_name.lower()), True)
        print(f" `{qn}` extension ready.")

    @property
    def fully(self) -> bool:
        return self.booted and all(getattr(self, ext) for ext in self.bot.extensions)
