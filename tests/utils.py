import requests
import zipfile
import io
import subprocess
import time
from typing import Optional
import os


def download_and_extract(url: str, path: str) -> None:
    if os.path.isdir(path):
        return
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(path)


class TempProcess:
    def __init__(self, *cmd: str, delay=1.0):
        self.__cmd = cmd
        self.__process: Optional[subprocess.Popen] = None
        self.__delay = delay

    def __enter__(self):
        assert self.__process is None
        self.__process = subprocess.Popen(self.__cmd)
        time.sleep(self.__delay)

    def __exit__(self, exc_type, exc_val, exc_tb):
        assert self.__process is not None
        self.__process.kill()
        self.__process = None
