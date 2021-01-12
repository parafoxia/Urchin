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

import datetime as dt
import traceback
import typing as t

import discord
from discord.ext import commands

from urchin.utils import chron, string


class ErrorHandler:
    __slots__ = ("bot",)

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def handle_error(
        self,
        err: str,
        ctx: t.Optional[commands.Context] = None,
        exc: t.Optional[Exception] = None,
    ) -> None:
        async with self.bot.session.post("https://mystb.in/documents", data=traceback.format_exc()) as response:
            if response.status == 200:
                data = await response.json()
                await self.bot.stdout.send(f"Something went wrong: <https://mystb.in/{data['key']}>")

        if ctx and err == "on_command_error":
            await ctx.send(
                f"Something went wrong. An automatic error report was submitted, but you should report it to {self.bot.app.owner.display_name}."
            )

        if exc:
            raise getattr(exc, "original", exc)

    async def handle_command_error(self, ctx: commands.Context, exc: Exception) -> None:
        if isinstance(exc, commands.CommandNotFound):
            return

        if isinstance(exc, commands.MissingRequiredArgument):
            return await ctx.send(f"You didn't pass enough arguments (missing `{exc.param.name}`).")

        if isinstance(exc, commands.BadArgument):
            return await ctx.send("You passed an invalid argument (probably incorrect type).")

        if isinstance(exc, commands.TooManyArguments):
            return await ctx.send("You passed too many arguments.")

        if isinstance(exc, commands.MissingPermissions):
            mp = string.list_of([str(perm.replace("_", " ")).title() for perm in exc.missing_perms])
            return await ctx.send(f"You don't have permission to do that (missing {mp}).")

        if isinstance(exc, commands.BotMissingPermissions):
            try:
                mp = string.list_of([str(perm.replace("_", " ")).title() for perm in exc.missing_perms])
                return await ctx.send(f"I don't have permission to do that (missing {mp}).")
            except discord.Forbidden:
                # If Send Messages permission is missing:
                return

        if isinstance(exc, commands.NotOwner):
            return await ctx.send(f"Only {self.bot.app.owner.display_name} can do that.")

        if isinstance(exc, commands.CommandOnCooldown):
            await ctx.message.delete()
            return await ctx.send(
                f"That command is on cooldown ({chron.long_delta(dt.timedelta(seconds=exc.retry_after))} remaining).",
                delete_after=10,
            )

        if isinstance(exc, commands.UserInputError):
            return await ctx.send("There was a user input error (probably near quotes).")

        if isinstance(exc, commands.CheckFailure):
            return await ctx.send("A command check failed (probably invalid configuration).")

        if original := getattr(exc, "original", None):
            if isinstance(original, discord.HTTPException):
                return await ctx.send(f"There was a HTTP exception ({original.status} - {original.text}).")
            else:
                raise original

        raise exc
