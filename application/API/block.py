import pexpect as pexp
import re
import ctypes
import time

from threading import Thread

dic = {
        'B':'bit',
        'MB':'mbit',
        'KB':'kbit',
        'GB':'gbit',
    }

class Blocker():
    def __init__(self,id):
        self.id = id
        self.thread = Thread(target=self.setup,args="")
        self.p = pexp.spawn("evillimiter --flush")

    def setup(self):
        self.p.timeout = 3600
        self.p.sendline("scan")
        self.p.sendline("hosts")
        self.p.sendline("block " + str(self.id))
        self.p.expect(['Main() >>> '])


    def stop(self):
        self.p.sendline('exit')
        self.p.close()

limite_101 = Blocker(2)

limite_101.thread.run()
limite_101.stop()

