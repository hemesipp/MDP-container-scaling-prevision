"""request for packet"""
import time
import subprocess
import requests


if __name__ == "__main__":
    while True:
        time.sleep(2)
        print("Go!")
        time.sleep(5)

        bashCommandName = 'echo $HOSTNAME'
        output = subprocess.check_output(['bash', '-c', bashCommandName])

        req = "http://pacman:80/" + output.decode()
        r = requests.get(req)
        if r.text=="Die":
            break
        print(r.text)
