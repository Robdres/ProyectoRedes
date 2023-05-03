import pexpect as pexp
import re
import ctypes
import time

from threading import Thread

class Limiter():
    def __init__(self,Limit):
        self.thread = Thread(target=self.start,args="")
        self.p = pexp.spawn("evillimiter --flush")

    def setup(self,id,direction,rate):
        self.p.timeout = 3600
        self.p.sendline("scan")
        self.p.sendline("hosts")
        self.p.sendline("limit")
        self.p.expect(True)

    def start(self):
        self.thread.start()

    def stop(self):
        self.p.close()

limite_101 = Limiter(ip,down,limit)

limite_101.start()
limite_101.stop()

