import turtle
import serverinfo
import socket
import threading

players = {}

s = socket.socket()
s.connect(serverinfo.addr)  # my own address and port

screen = turtle.Screen()
self = turtle.Turtle()


def moveTurtle(id, pos):
    pos = tuple(pos.split(' '))
    players[id].goto((float(pos[0]), float(pos[1])))


def newClientTurtle(name):
    players[name] = turtle.Turtle()
    print(players[name])

def msgHandler(msg):
    if msg.startswith("newClient="):
        msg = msg[10:]
        newClientTurtle(msg)
    if msg.startswith("newPos="):
        msg = msg[7:]
        idpos = msg.split(',')
        moveTurtle(id=idpos[0], pos=idpos[1])



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