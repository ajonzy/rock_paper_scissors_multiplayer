import socket
from _thread import *
import pickle
from game import Game

server = "192.168.1.151"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server started")

connected = set()
games = {}
idCount = 0

def threaded_client(conn, p, gameID):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameID in games:
                game = games[gameID]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    reply = game
                    conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameID]
        print("Closing Game ", gameID)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    idCount += 1
    p = 0
    gameID = (idCount - 1)//2

    if idCount % 2 == 1:
        games[gameID] = Game(gameID)
        print("Creating a new game...")
    else:
        games[gameID].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameID))