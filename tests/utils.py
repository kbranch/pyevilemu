import requests
import zipfile
import io
import subprocess
import time
from typing import List, Optional


def download_and_extract(url: str, path: str) -> None:
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(path)


class TempProcess:
    def __init__(self, *cmd: str):
        self.__cmd = cmd
        self.__process: Optional[subprocess.Popen] = None

    def __enter__(self):
        assert self.__process is None
        self.__process = subprocess.Popen(self.__cmd)
        time.sleep(1.0)

    def __exit__(self, exc_type, exc_val, exc_tb):
        assert self.__process is not None
        self.__process.kill()
        self.__process = None
