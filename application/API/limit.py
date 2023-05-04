import re
import ctypes
import time
import subprocess

from threading import Thread
import multiprocessing


class Limiter():
    def __init__(self,id):
        self.id = id
        self.stop_event = multiprocessing.Event()
            

    def setup_limit(self,limit):
        self.limit=str(limit[0]) + limit[1]

    def start(self):
        self.stop_event = multiprocessing.Event()
        self.thread = Thread(target=self.setup, args=(self.stop_event,))
        self.thread.run()

    def setup(self,event):
        self.p = subprocess.Popen(['python3','application/API/limit_script.py',str(self.id),self.limit],stdout=subprocess.PIPE)

    def stop(self):
        self.stop_event.set()

