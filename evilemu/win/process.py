import ctypes.wintypes
import evilemu.win.nativeapi
import evilemu.process
from typing import Generator, Tuple


class Process(evilemu.process.ProcessBase):
    @staticmethod
    def find_processes(executable_name: str) -> Generator["Process", None, None]:
        process_list = (ctypes.wintypes.DWORD * 2048)()
        process_count = ctypes.wintypes.DWORD(0)
        if not evilemu.win.nativeapi.EnumProcesses(process_list, ctypes.sizeof(process_list), process_count):
            raise ValueError("EnumProcesses failed")
        process_count = min(2048, process_count.value // ctypes.sizeof(ctypes.wintypes.DWORD))
        for n in range(process_count):
            access = evilemu.win.nativeapi.PROCESS_VM_READ | evilemu.win.nativeapi.PROCESS_QUERY_INFORMATION | evilemu.win.nativeapi.PROCESS_VM_WRITE | evilemu.win.nativeapi.PROCESS_VM_OPERATION
            proc = evilemu.win.nativeapi.OpenProcess(access, False, process_list[n])
            if proc is None:
                continue
            buffer = ctypes.create_string_buffer(128)
            evilemu.win.nativeapi.GetModuleBaseNameA(proc, None, buffer, ctypes.sizeof(buffer))
            if buffer.value == executable_name.encode("ascii"):
                yield Process(proc)
            else:
                evilemu.win.nativeapi.CloseHandle(proc)

    def __init__(self, process_handle: ctypes.wintypes.HANDLE):
        self.__handle = process_handle

    def __del__(self):
        evilemu.win.nativeapi.CloseHandle(self.__handle)

    def read_memory(self, addr: int, size: int) -> bytes:
        base_addr = addr & ~0xFFF
        base_size = ((size - 1) | 0xFFF) + 1
        mem_buffer = (ctypes.c_byte * base_size)()
        if not evilemu.win.nativeapi.ReadProcessMemory(self.__handle, base_addr, mem_buffer, ctypes.sizeof(mem_buffer), None):
            raise IOError("Failed to read process memory...")
        return bytes(mem_buffer)[addr - base_addr:addr - base_addr + size]

    def write_memory(self, addr: int, data: bytes) -> None:
        if not evilemu.win.nativeapi.WriteProcessMemory(self.__handle, addr, data, len(data), None):
            raise IOError("Failed to write process memory...")

    def _primary_memory_section(self) -> Generator[Tuple[int, int], None, None]:
        module_list = (ctypes.wintypes.HMODULE * 32)()
        module_count = ctypes.wintypes.DWORD(0)
        evilemu.win.nativeapi.EnumProcessModulesEx(self.__handle, module_list, ctypes.sizeof(module_list), module_count, evilemu.win.nativeapi.LIST_MODULES_ALL)
        info = evilemu.win.nativeapi.MODULEINFO()
        evilemu.win.nativeapi.GetModuleInformation(self.__handle, module_list[0], info, ctypes.sizeof(info))
        yield info.lpBaseOfDll, info.SizeOfImage

    def _all_memory_sections(self) -> Generator[Tuple[int, int], None, None]:
        info = evilemu.win.nativeapi.MEMORY_BASIC_INFORMATION()
        ptr = 0
        while True:
            if evilemu.win.nativeapi.VirtualQueryEx(self.__handle, ptr, info, ctypes.sizeof(info)) != ctypes.sizeof(info):
                break
            if info.State != 0x1000:
                ptr += info.RegionSize
                continue
            # if info.Type != 0x20000 and info.Type != 0x40000:
            #     continue
            yield ptr, info.RegionSize
            ptr += info.RegionSize
