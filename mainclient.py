import turtle
import serverinfo
import socket
import threading

players = {}

s = socket.socket()
s.connect(serverinfo.addr)  # my own address and port

screen = turtle.Screen()
self = turtle.Turtle()


def newClientTurtle(name):
    players[name] = turtle.Turtle()
    print(players[name])

def msgHandler(msg):
    if msg.startswith("newClient="):
        msg = msg[10:]
        newClientTurtle(msg)


def rawlistener():
    while True:
        msg = s.recv(2048).decode()
        print(msg)
        msgHandler(msg)

def move(x, y):
    s.send(f"{x} {y}".encode())
    self.goto(x, y)


listener = threading.Thread(target=rawlistener)
listener.start()
turtle.onscreenclick(move, btn=1)

turtle.mainloop()