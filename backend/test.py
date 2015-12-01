import subprocess
import time
child = subprocess.Popen(['python3', 'ftp.py', 'upload', 'pg.py', 'qq'])
while child.poll() == None:

    print(child.returncode)
    time.sleep(0.01)
    print("--")
    
