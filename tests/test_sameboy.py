from tests.utils import download_and_extract, TempProcess
from evilemu import find_gameboy_emulators


def test_sameboy():
    download_and_extract("https://github.com/LIJI32/SameBoy/releases/download/v0.15.8/sameboy_winsdl_v0.15.8.zip", "_download/sameboy")
    with TempProcess("_download/sameboy/sameboy.exe", "_download/bgb32/bgbtest.gb", delay=5):
        e = list(find_gameboy_emulators())
        assert len(e) == 1
        assert e[0].read_rom(0x134, 16) == b'BGBWELCOME\x00\x00\x00\x00\x00\x00'
        assert e[0].read_ram16(9) == 0x8001
