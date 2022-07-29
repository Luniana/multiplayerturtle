import socket
import threading
from string import ascii_lowercase, ascii_uppercase
import random
s = socket.socket()
s.bind(("192.168.1.102", 42069))  #my own address and port
s.listen(8)

chars = list(ascii_lowercase) + list(ascii_uppercase) + [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

players = {}

def genClientId():
    id = ""
    random.shuffle(chars)
    for i in range(1, 11):
        id += str(random.choice(chars))
    return id


def msgHandler(senderid, msg):
    for id in players.keys():
        if not players[id] == players[senderid]:
            players[id].send(f"newPos={id},{msg}".encode())


def connHandler(conn, addrclient, clientid):
    for id in players.keys():
        if not id == clientid:
            players[id].send(("newClient=" + clientid).encode())
    while True:
        msg = conn.recv(2048).decode()
        print(addrclient, msg)
        msgHandler(clientid, msg)


def rawlistener():
    while True:
        conn, addrclient = s.accept()
        newid = genClientId()
        players[newid] = conn
        handle = threading.Thread(target=connHandler, args=[conn, addrclient, newid])
        handle.start()

listener = threading.Thread(target=rawlistener)
listener.start()
print("listening")