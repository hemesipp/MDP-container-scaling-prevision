"""request for packet"""
import time
import socket
import subprocess
import requests
import uvicorn

def netcat(hostname, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    s.sendall(content)
    s.shutdown(socket.SHUT_WR)
    while 1:
        time.sleep(3)
        data = s.recv(1024)
        if data == "":
            break
        print("Received:", data.decode())
    print("Connection closed.")
    s.close()


if __name__ == "__main__":
    while True:
        time.sleep(2)
        print("Go!")
        time.sleep(2)

        bashCommandName = 'echo $HOSTNAME'
        output = subprocess.check_output(['bash', '-c', bashCommandName])

        req = "http://pacman:80/" + output.decode()
        r = requests.get(req)
        print(r.text)

        """
        content="GET / HTTP/1.1" \
                 "Host: 0.0.0.0"

        netcat("pacman", 80, content.encode())
        """