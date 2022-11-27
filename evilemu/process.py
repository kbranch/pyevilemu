import sys
from evilemu.processbase import ProcessBase

if sys.platform == "linux":
    from evilemu.linux.process import Process
else:
    from evilemu.win.process import Process
