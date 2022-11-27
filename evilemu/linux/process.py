import evilemu.processbase
import os
from typing import Generator, Tuple


class Process(evilemu.processbase.ProcessBase):
    @staticmethod
    def find_processes(executable_name: str) -> Generator["Process", None, None]:
        for pid in os.listdir("/proc/"):
            try:
                pid = int(pid)
            except ValueError:
                continue
            try:
                exe = os.readlink(f"/proc/{pid}/exe")
            except IOError:
                continue
            exe = os.path.basename(exe)
            if exe == executable_name:
                yield Process(pid)

    def __init__(self, pid: int):
        self.__mem = open(f"/proc/{pid}/mem", "rb")
        self.__pid = pid

    def __del__(self) -> None:
        self.__mem.close()

    def read_memory(self, addr: int, size: int) -> bytes:
        self.__mem.seek(addr)
        return self.__mem.read(size)

    def write_memory(self, addr: int, data: bytes) -> None:
        self.__mem.seek(addr)
        self.__mem.write(data)

    def _primary_memory_section(self) -> Generator[Tuple[int, int], None, None]:
        for line in open(f"/proc/{self.__pid}/maps", "rt"):
            line = line.split(None, 5)
            if len(line) > 5:
                if line[1].startswith("rw"):
                    start, end = line[0].split("-", 1)
                    start = int(start, 16)
                    end = int(end, 16)
                    yield start, end - start
                    return

    def _all_memory_sections(self) -> Generator[Tuple[int, int], None, None]:
        for line in open(f"/proc/{self.__pid}/maps", "rt"):
            line = line.split(None, 5)
            if len(line) > 5:
                if line[1].startswith("rw"):
                    start, end = line[0].split("-", 1)
                    start = int(start, 16)
                    end = int(end, 16)
                    yield start, end - start
