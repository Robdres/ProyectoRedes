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

class Limiter():
    def __init__(self,id,limit):
        self.id = id
        # if(direction == "up"):
        #     self.direction = '--upload'
        # else:
        #     self.direction = '--download'
            
        self.limit=str(limit[0]) + dic[limit[1]]
        self.thread = Thread(target=self.setup,args="")
        self.p = pexp.spawn("evillimiter --flush")

    def setup(self):
        self.p.timeout = 3600
        self.p.sendline("scan")
        self.p.sendline("hosts")
        self.p.sendline("limit " + str(self.id) +" " +self.limit)
        self.p.expect(['Main() >>> '])
        self.stop()

    def stop(self):
        self.p.interact()
        self.p.sendline('exit')

limite_101 = Limiter(2,[100,'MB'])

limite_101.thread.run()

