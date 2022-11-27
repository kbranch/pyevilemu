from evilemu.emulator import Emulator
from evilemu.process import Process
from typing import Generator


class BGB32(Emulator):
    @staticmethod
    def find_all() -> Generator[Emulator, None, None]:
        for process in Process.find_processes("bgb.exe"):
            try:
                for base_address in process.search(b'\x6D\x61\x69\x6E\x6C\x6F\x6F\x70\x83\xC4\xF4\xA1'):
                    main_address = process.read_pointer_chain32(base_address + 12, 0, 0, 0x34)
                    rom_address = process.read_pointer32(main_address + 0x10)
                    ram_address = process.read_pointer32(main_address + 0x108)
                    if rom_address != 0 and ram_address != 0:
                        yield BGB32(process, rom_address, ram_address)
            except IOError:
                pass


class BGB64(Emulator):
    @staticmethod
    def find_all() -> Generator[Emulator, None, None]:
        for process in Process.find_processes("bgb64.exe"):
            try:
                for base_address in process.search_chunks(
                    (0, b'\x48\x83\xec\x28\x48\x8b\x05'),
                    (11, b'\x48\x83\x38\x00\x74\x1a\x48\x8b\x05'),
                    (24, b'\x48\x8b\x00\x80\xb8'),
                    (33, b'\x00\x74\x07'),
                ):
                    offset = process.read_pointer32(base_address + 20) + 24
                    main_address = process.read_pointer_chain64(base_address + offset, 0, 0x44)
                    rom_address = process.read_pointer64(main_address + 0x18)
                    ram_address = process.read_pointer64(main_address + 0x190)
                    if rom_address != 0 and ram_address != 0:
                        yield BGB64(process, rom_address, ram_address)
            except IOError:
                pass
