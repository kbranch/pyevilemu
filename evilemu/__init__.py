from typing import Generator
from evilemu.emulator import Emulator
from evilemu.bgb import BGB32, BGB64

_ALL_GAMEBOY = [BGB32, BGB64]


def find_gameboy_emulators() -> Generator[Emulator, None, None]:
    for cls in _ALL_GAMEBOY:
        for e in cls.find_all():
            yield e
