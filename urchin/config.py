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

import os
import typing as t
from pathlib import Path

import dotenv

dotenv.load_dotenv()


class ConfigMeta(type):
    def resolve_value(cls, value: str):
        _map: t.Dict[str, t.Callable] = {
            "bool": bool,
            "int": int,
            "float": float,
            "file": lambda x: Path(x).read_text(),
            "str": str,
            "set": lambda x: set([cls.resolve_value(e.strip()) for e in x.split(",")]),
        }

        return _map[(v := value.split(":", maxsplit=1))[0]](v[1])

    def resolve_key(cls, key: str):
        try:
            return cls.resolve_key(os.environ[key])
        except:
            return cls.resolve_value(key)

    def __getattr__(cls, name):
        try:
            return cls.resolve_key(name)
        except KeyError:
            raise AttributeError(f"{name} is not a key in config.") from None

    def __getitem__(cls, name):
        return cls.__getattr__(name)


class Config(metaclass=ConfigMeta):
    pass
