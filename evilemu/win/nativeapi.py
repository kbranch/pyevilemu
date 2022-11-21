import ctypes.wintypes

# Use ctypes to get access to win32 API.
# This file contains all used APIs and sets up the right parameter/return times


class MODULEINFO(ctypes.Structure):
    _fields_ = [
        ("lpBaseOfDll", ctypes.wintypes.LPVOID),
        ("SizeOfImage", ctypes.wintypes.DWORD),
        ("EntryPoint", ctypes.wintypes.LPVOID),
    ]


class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BaseAddress", ctypes.wintypes.ULARGE_INTEGER),
        ("AllocationBase", ctypes.wintypes.ULARGE_INTEGER),
        ("AllocationProtect", ctypes.wintypes.DWORD),
        ("PartitionId", ctypes.wintypes.WORD),
        ("RegionSize", ctypes.wintypes.ULARGE_INTEGER),
        ("State", ctypes.wintypes.DWORD),
        ("Protect", ctypes.wintypes.DWORD),
        ("Type", ctypes.wintypes.DWORD),
    ]

# DWORD GetLastError();
GetLastError = ctypes.windll.kernel32.GetLastError
GetLastError.restype = ctypes.wintypes.DWORD

# HANDLE OpenProcess([in] DWORD dwDesiredAccess, [in] BOOL bInheritHandle, [in] DWORD dwProcessId);
OpenProcess = ctypes.windll.kernel32.OpenProcess
OpenProcess.argtypes = [ctypes.wintypes.DWORD, ctypes.wintypes.BOOL, ctypes.wintypes.DWORD]
OpenProcess.restype = ctypes.wintypes.HANDLE
# BOOL EnumProcesses([out] DWORD *lpidProcess, [in] DWORD cb, [out] LPDWORD lpcbNeeded);
EnumProcesses = ctypes.windll.psapi.EnumProcesses
EnumProcesses.argtypes = [ctypes.wintypes.PDWORD, ctypes.wintypes.DWORD, ctypes.wintypes.LPDWORD]
EnumProcesses.restype = ctypes.wintypes.BOOL
# BOOL CloseHandle([in] HANDLE hObject);
CloseHandle = ctypes.windll.kernel32.CloseHandle
CloseHandle.argtypes = [ctypes.wintypes.HANDLE]
CloseHandle.restype = ctypes.wintypes.BOOL
# BOOL EnumProcessModules([in] HANDLE hProcess, [out] HMODULE *lphModule, [in] DWORD cb, [out] LPDWORD lpcbNeeded);
EnumProcessModulesEx = ctypes.windll.psapi.EnumProcessModulesEx
EnumProcessModulesEx.argtypes = [ctypes.wintypes.HANDLE, ctypes.POINTER(ctypes.wintypes.HMODULE), ctypes.wintypes.DWORD, ctypes.wintypes.LPDWORD, ctypes.wintypes.DWORD]
EnumProcessModulesEx.restype = ctypes.wintypes.BOOL
# DWORD GetModuleBaseNameA([in] HANDLE hProcess, [in, optional] HMODULE hModule, [out] LPSTR lpBaseName, [in] DWORD nSize);
GetModuleBaseNameA = ctypes.windll.psapi.GetModuleBaseNameA
GetModuleBaseNameA.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.HMODULE, ctypes.wintypes.LPSTR, ctypes.wintypes.DWORD]
GetModuleBaseNameA.restype = ctypes.wintypes.DWORD
# BOOL ReadProcessMemory([in] HANDLE hProcess, [in] LPCVOID lpBaseAddress, [out] LPVOID lpBuffer, [in] SIZE_T nSize, [out] SIZE_T *lpNumberOfBytesRead);
ReadProcessMemory = ctypes.windll.kernel32.ReadProcessMemory
ReadProcessMemory.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.ULARGE_INTEGER, ctypes.wintypes.LPVOID, ctypes.wintypes.ULARGE_INTEGER, ctypes.wintypes.PULARGE_INTEGER]
ReadProcessMemory.restype = ctypes.wintypes.BOOL
# BOOL WriteProcessMemory([in] HANDLE hProcess, [in] LPCVOID lpBaseAddress, [in] LPVOID lpBuffer, [in] SIZE_T nSize, [out] SIZE_T *lpNumberOfBytesWritten);
WriteProcessMemory = ctypes.windll.kernel32.WriteProcessMemory
WriteProcessMemory.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.ULARGE_INTEGER, ctypes.wintypes.LPVOID, ctypes.wintypes.ULARGE_INTEGER, ctypes.wintypes.PULARGE_INTEGER]
WriteProcessMemory.restype = ctypes.wintypes.BOOL
# BOOL GetModuleInformation([in] HANDLE hProcess, [in] HMODULE hModule, [out] LPMODULEINFO lpmodinfo, [in] DWORD cb);
GetModuleInformation = ctypes.windll.psapi.GetModuleInformation
GetModuleInformation.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.HMODULE, ctypes.POINTER(MODULEINFO), ctypes.wintypes.DWORD]
GetModuleInformation.restype = ctypes.wintypes.BOOL
# SIZE_T VirtualQueryEx([in] HANDLE hProcess, [in, optional] LPCVOID lpAddress, [out] PMEMORY_BASIC_INFORMATION lpBuffer, [in] SIZE_T dwLength);
VirtualQueryEx = ctypes.windll.kernel32.VirtualQueryEx
VirtualQueryEx.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.LPCVOID, ctypes.POINTER(MEMORY_BASIC_INFORMATION), ctypes.wintypes.ULARGE_INTEGER]
VirtualQueryEx.restype = ctypes.wintypes.ULARGE_INTEGER


PROCESS_VM_OPERATION = 0x08
PROCESS_VM_READ = 0x10
PROCESS_VM_WRITE = 0x20
PROCESS_QUERY_INFORMATION = 0x0400
LIST_MODULES_ALL = 0x03
