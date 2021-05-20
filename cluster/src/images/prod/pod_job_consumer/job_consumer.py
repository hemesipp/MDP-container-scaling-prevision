"""request for packet"""
import time
import subprocess
import requests
import numpy as np
from random import *

if __name__ == "__main__":
    while True:
        #w = random()
        #t = 10*np.exp(w)
        b = 5.0
        t = np.random.exponential(b)
        time.sleep(t)

        bashCommandName = 'echo $HOSTNAME'
        output = subprocess.check_output(['bash', '-c', bashCommandName])

        req = "http://pacman:80/job/" + output.decode()
        r = requests.get(req)
        print(r.text)
        print(type(r.text))
        print(r.text == "Die")
        if str(r.text) == "Die":
            break
    print("out of the loop")
