import re
from evilemu.emulator import Emulator
from evilemu.process import Process
from typing import Generator


class BGB32(Emulator):
    @staticmethod
    def find_all() -> Generator[Emulator, None, None]:
        for process in Process.find_processes("bgb.exe"):
            try:
                version = 'unknown'

                # One byte between the chunks varies with version
                # Last chunk ends with 'bgb1.' to pinpoint the right spot, which is fragile but at least detects 1.5.x correctly
                version_address = next(process.search_chunks(
                    (0, b'\xFF\xFF\xFF\xFF'),
                    (5, b'\x00\x00\x00\x62\x67\x62\x31\x2E'),
                ), False)

                if version_address:
                    # Should give us something like 'bgb1.5.11___'
                    # We read some junk at the end for extra digits in the future
                    version_address += 8
                    version = process.read_memory(version_address, 12).decode('utf-8', errors='ignore')

                hram_offset = 0x130

                version_chunks = [int(x) for x in re.findall('(\d+)', version)]
                if version_chunks[1] >= 6 and version_chunks[2] >= 1:
                    # Tested with 1.6.1-4
                    hram_offset = 0x248

                for base_address in process.search(b'\x6D\x61\x69\x6E\x6C\x6F\x6F\x70\x83\xC4\xF4\xA1'):
                    main_address = process.read_pointer_chain32(base_address + 12, 0, 0, 0x34)
                    rom_address = process.read_pointer32(main_address + 0x10)
                    ram_address = process.read_pointer32(main_address + 0x108)
                    hram_address = process.read_pointer32(main_address + hram_offset)
                    if rom_address != 0 and ram_address != 0:
                        yield BGB32(process, rom_address, ram_address, hram_address)
            except IOError:
                pass


class BGB64(Emulator):
    @staticmethod
    def find_all() -> Generator[Emulator, None, None]:
        for process in Process.find_processes("bgb64.exe"):
            try:
                version = 'unknown'

                # One byte between the chunks varies with version
                # Last chunk ends with 'bgb1.' to pinpoint the right spot, which is fragile but at least detects 1.5.x correctly
                version_address = next(process.search_chunks(
                    (0, b'\xE4\x04\x01\x00\xFF\xFF\xFF\xFF'),
                    (9, b'\x00\x00\x00\x62\x67\x62\x31\x2E'),
                ), False)

                if version_address:
                    # Should give us something like 'bgb1.5.11.w64'
                    version_address += 12
                    version = process.read_memory(version_address, 14).decode('utf-8', errors='ignore')

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

                    if "bgb1.5." in version:
                        # Tested with 1.5.10 and 1.5.11
                        hram_address = process.read_pointer64(main_address + 0x1D9)  # Not sure, this is unaligned, which is odd...
                    else:
                        # Tested with 1.6 and 1.6.1
                        hram_address = process.read_pointer64(main_address + 0x2E9)

                    if rom_address != 0 and ram_address != 0 and hram_address != 0:
                        yield BGB64(process, rom_address, ram_address, hram_address)
            except IOError:
                pass
