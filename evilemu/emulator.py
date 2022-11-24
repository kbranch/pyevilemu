import abc
from evilemu.process import ProcessBase
from typing import Generator


class Emulator(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def find_all() -> Generator["Emulator", None, None]:
        ...

    def __init__(self, process: ProcessBase, rom_address: int, ram_address: int):
        self.__process = process
        self.__rom_address = rom_address
        self.__ram_address = ram_address

    def read_rom(self, offset: int, size: int) -> bytes:
        return self.__process.read_memory(self.__rom_address + offset, size)

    def read_ram(self, offset: int, size: int) -> bytes:
        return self.__process.read_memory(self.__ram_address + offset, size)

    def write_rom(self, offset: int, data: bytes) -> None:
        return self.__process.write_memory(self.__rom_address + offset, data)

    def write_ram(self, offset: int, data: bytes) -> None:
        return self.__process.write_memory(self.__ram_address + offset, data)

    def read_rom8(self, offset: int) -> int:
        return int.from_bytes(self.read_rom(offset, 1), 'little')

    def read_ram8(self, offset: int) -> int:
        return int.from_bytes(self.read_ram(offset, 1), 'little')

    def write_rom8(self, offset: int, data: int) -> None:
        return self.write_rom(offset, data.to_bytes(1, 'little'))

    def write_ram8(self, offset: int, data: int) -> None:
        return self.write_ram(offset, data.to_bytes(1, 'little'))

    def read_rom16(self, offset: int) -> int:
        return int.from_bytes(self.read_rom(offset, 2), 'little')

    def read_ram16(self, offset: int) -> int:
        return int.from_bytes(self.read_ram(offset, 2), 'little')

    def write_rom16(self, offset: int, data: int) -> None:
        return self.write_rom(offset, data.to_bytes(2, 'little'))

    def write_ram16(self, offset: int, data: int) -> None:
        return self.write_ram(offset, data.to_bytes(2, 'little'))
