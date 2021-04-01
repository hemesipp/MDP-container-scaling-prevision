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

        req = "http://pacman:80/work/" + output.decode()
        r = requests.get(req)
        print(r.text)
        print(type(r.text))
        print(r.text=="Die")
        if r.text == "Die":
            break
    print("out of the loop")
