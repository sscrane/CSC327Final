import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "127.0.0.1"
port = 8000
s.bind((host, port))
s.listen()
client, address = s.accept()
print("%s accepted at %s" % (client, address))

while True:

    message = client.recv(1024)
    print(message.decode())
    #time.sleep(10)


client.close()