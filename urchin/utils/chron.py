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
from time import strftime

from urchin.utils import string


def sys_time():
    return strftime("%H:%M:%S")


def utc_time():
    return dt.datetime.utcnow().strftime("%H:%M:%S")


def short_date(dt):
    return dt.strftime("%d/%m/%y")


def short_date_and_time(dt):
    return dt.strftime("%d/%m/%y %H:%M:%S")


def long_date(dt):
    return dt.strftime("%d %b %Y")


def long_date_and_time(dt):
    return dt.strftime("%d %b %Y at %H:%M:%S")


def short_delta(td, milliseconds=False):
    parts = []

    if td.days != 0:
        parts.append(f"{td.days:,}d")

    if (h := td.seconds // 3600) != 0:
        parts.append(f"{h}h")

    if (m := td.seconds // 60 - (60 * h)) != 0:
        parts.append(f"{m}m")

    if (s := td.seconds - (60 * m) - (3600 * h)) != 0 or not parts:
        if milliseconds:
            ms = round(td.microseconds / 1000)
            parts.append(f"{s}.{ms}s")
        else:
            parts.append(f"{s}s")

    return ", ".join(parts)


def long_delta(td, milliseconds=False):
    parts = []

    if (d := td.days) != 0:
        parts.append(f"{d:,} day{'s' if d > 1 else ''}")

    if (h := td.seconds // 3600) != 0:
        parts.append(f"{h} hour{'s' if h > 1 else ''}")

    if (m := td.seconds // 60 - (60 * h)) != 0:
        parts.append(f"{m} minute{'s' if m > 1 else ''}")

    if (s := td.seconds - (60 * m) - (3600 * h)) != 0 or not parts:
        if milliseconds:
            ms = round(td.microseconds / 1000)
            parts.append(f"{s}.{ms} seconds")
        else:
            parts.append(f"{s} second{'s' if s > 1 else ''}")

    return string.list_of(parts)


def from_iso(stamp):
    try:
        return dt.datetime.fromisoformat(stamp)
    except TypeError:
        # In case there's no records:
        return dt.datetime.min


def to_iso(obj):
    return obj.isoformat(" ")
