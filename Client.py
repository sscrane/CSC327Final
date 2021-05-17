#!/usr/bin/env python3

import socket
import time

def ConnectToServer():
    i = 0
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 8000))
        s.send("GET / HTTP/1.1\r\n\r\n".encode("utf-8"))
        while True:
            s.send(str(i).encode("utf-8"))
            i+=1
            time.sleep(1)

    except socket.error as error:
        print("Error: %s" % error)
        return False

    s.close()

def main():
    ConnectToServer()



if __name__ == '__main__':
    main()