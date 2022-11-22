from tests.utils import download_and_extract, TempProcess
from evilemu import find_gameboy_emulators


def test_bgb32():
    download_and_extract("https://bgb.bircd.org/bgb.zip", "_download/bgb32")
    with TempProcess("_download/bgb32/bgb.exe", "_download/bgb32/bgbtest.gb"):
        e = list(find_gameboy_emulators())
        assert len(e) == 1
        assert e[0].read_rom(0x134, 16) == b'BGBWELCOME\x00\x00\x00\x00\x00\x00'
        assert e[0].read_ram16(9) == 0x8001


def test_bgb64():
    download_and_extract("https://bgb.bircd.org/bgbw64.zip", "_download/bgb64")
    with TempProcess("_download/bgb64/bgb64.exe", "_download/bgb64/bgbtest.gb"):
        e = list(find_gameboy_emulators())
        assert len(e) == 1
        assert e[0].read_rom(0x134, 16) == b'BGBWELCOME\x00\x00\x00\x00\x00\x00'
        assert e[0].read_ram16(9) == 0x8001
