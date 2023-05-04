import re
import ctypes
import time
import subprocess
import multiprocessing
from threading import Thread


class Blocker():
    def __init__(self,id):
        self.id = id
        self.stop_event = multiprocessing.Event()

    def start(self):
        self.stop_event = multiprocessing.Event()
        self.thread = Thread(target=self.setup, args=(self.stop_event,))
        self.thread.run()

    def setup(self,event):
        self.p = subprocess.Popen(['python3','./application/API/block_script.py',str(self.id)],stdout=subprocess.PIPE)

    def stop(self):
        self.stop_event.set()
