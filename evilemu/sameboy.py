from evilemu.emulator import Emulator
from evilemu.process import Process
from typing import Generator


class SameBoy(Emulator):
    @staticmethod
    def find_all() -> Generator[Emulator, None, None]:
        for process in Process.find_processes("sameboy.exe"):
            try:
                for base_address in process.search(b'EMAS'):
                    # Sameboy's data structure starts with this magic number, and then the version number
                    version = process.read_pointer32(base_address + 4)
                    if version == 14:
                        # Offsets depend on the version of SameBoy
                        rom_address = process.read_pointer32(base_address + 33920)
                        ram_address = process.read_pointer32(base_address + 33944)
                        yield SameBoy(process, rom_address, ram_address)
                        break
            except IOError:
                pass
