import subprocess
from threading import Thread


def running():
    print("hello")
    with subprocess.Popen(['sudo','/sbin/evillimiter','--flush'],stdout=subprocess.PIPE,stderr=subprocess.PIPE) as proc:
        try:
            (os,error) =proc.communicate(input=b"scan\r")
            proc.wait()
        except subprocess.TimeoutExpired:
            print("error")
            proc.kill()

running()

