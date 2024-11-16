import abc
import sys
from typing import Generator, Tuple, List


class ProcessBase(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def find_processes(executable_name: str) -> Generator["ProcessBase", None, None]:
        ...

    @abc.abstractmethod
    def read_memory(self, addr: int, size: int) -> bytes:
        ...

    @abc.abstractmethod
    def write_memory(self, addr: int, data: bytes) -> None:
        ...

    @abc.abstractmethod
    def _primary_memory_section(self) -> Generator[Tuple[int, int], None, None]:
        ...

    @abc.abstractmethod
    def _all_memory_sections(self) -> Generator[Tuple[int, int], None, None]:
        ...

    def read_pointer32(self, addr: int) -> int:
        pointer = bytes()
        for i in range(4):
            pointer += self.read_memory(addr + i, 1)

        return int.from_bytes(pointer, byteorder=sys.byteorder)

    def read_pointer64(self, addr: int) -> int:
        pointer = bytes()
        for i in range(8):
            pointer += self.read_memory(addr + i, 1)

        return int.from_bytes(pointer, byteorder=sys.byteorder)

    def read_pointer_chain32(self, addr: int, *offsets: int) -> int:
        ptr = self.read_pointer32(addr)
        for offset in offsets:
            ptr = self.read_pointer32(ptr + offset)
        return ptr

    def read_pointer_chain64(self, addr: int, *offsets: int) -> int:
        ptr = self.read_pointer64(addr)
        for offset in offsets:
            ptr = self.read_pointer64(ptr + offset)
        return ptr

    def search(self, data: bytes, *, all_memory: bool = False) -> Generator[int, None, None]:
        """Search for all occurances of [data] in the memory of this process.
            By default only search the primary memory, which is quick and fast.
            Searching all memory allows you to find anything, but is inefficient and error prone.
        """
        for start, size in self._all_memory_sections() if all_memory else self._primary_memory_section():
            try:
                mem = self.read_memory(start, size)
            except IOError:
                continue
            idx = mem.find(data)
            while True:
                if idx == -1:
                    break
                yield start + idx
                idx = mem.find(data, idx + 1)

    def search_chunks(self, *data: Tuple[int, bytes], all_memory: bool = False) -> Generator[int, None, None]:
        """Search for all occurances of [offset, data] in the memory of this process.
            By default only search the primary memory, which is quick and fast.
            Searching all memory allows you to find anything, but is inefficient and error prone.
        """
        first_data = data[0][1]
        for start, size in self._all_memory_sections() if all_memory else self._primary_memory_section():
            try:
                mem = self.read_memory(start, size)
            except IOError:
                continue
            idx = mem.find(first_data)
            while True:
                if idx == -1:
                    break
                for offset, chunk in data:
                    if mem[idx + offset:idx + offset + len(chunk)] != chunk:
                        break
                else:
                    yield start + idx
                idx = mem.find(first_data, idx + 1)
