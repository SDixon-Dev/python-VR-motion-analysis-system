from pathlib import Path
import sys
import time

# Locate the repository's src folder.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"

# Allow this test utility to import triad_openvr from src.
sys.path.insert(0, str(SRC_DIR))

import triad_openvr

v = triad_openvr.triad_openvr()
v.print_discovered_objects()

if len(sys.argv) == 1:
    interval = 1/250
elif len(sys.argv) == 2:
    interval = 1/float(sys.argv[1])
else:
    print("Invalid number of arguments")
    interval = False
    
if interval:
    while(True):
        start = time.time()
        txt = ""
        for each in v.devices["controller_1"].get_pose_euler():
            txt += "%.4f" % each
            txt += " "
        print("\r" + txt, end="")
        sleep_time = interval-(time.time()-start)
        if sleep_time>0:
            time.sleep(sleep_time)