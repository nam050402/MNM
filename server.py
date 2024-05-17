import socket
from _thread import*
import sys
import pickle
import time

server = "192.168.48.205"
# "192.168.1.112"
port = 8081
current_player = 0

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("waiting for a connection, Server Started")

# table information
client = []
client.append([1,0])
client.append([2,0])
board = []
for i in range(11):
    board.append([0]*11)
# table information
game_ready = [0,0]
game_state = "ready to play"
send_start = 0

def threaded_client(conn, player):
    global current_player
    global board
    global game_state
    global game_ready
    global send_start
    rematch_offer = False
    reply = []
    reply.append("Send client state")
    reply.append(player)
    reply.append(current_player)
    conn.send(pickle.dumps(reply))
    while True:
        try:
            reply = []
            data = conn.recv(4096)
            if not data:
                print("Disconnected")
                game_state = "ready to play"
                game_ready = [0,0]
                client[player - 1][1] = 0
                current_player -= 1
                break

            data_recieve = pickle.loads(data)
            # print(data_recieve)
            if data_recieve[0]=="waiting for opponent":
                reply.append("send client num")
                reply.append(current_player)
            elif data_recieve[0]=="start game":
                reply.append("board data")
                reply.append(current_player)
                reply.append(board)
            elif data_recieve[0]=="maintain connection":
                if current_player <2:
                    board = []
                    for i in range(11):
                        board.append([0]*11)
                    reply.append("player has disconnected" )
                    reply.append(current_player)
                elif current_player >=2 and game_state == "ready to play":
                    reply.append("board data")
                    reply.append(current_player)
                    reply.append(board)
                elif game_state != "ready to play" and game_ready!= [1,1] and rematch_offer == False:
                    reply.append("you opponent has resign")
                    reply.append(game_ready)
                elif game_state != "ready to play" and game_ready!= [1,1] and rematch_offer:
                    reply.append("wait for opponent")
                    reply.append(game_ready)
                elif game_state != "ready to play" and game_ready == [1,1]:
                    board = []
                    for i in range(11):
                        board.append([0]*11)
                    reply.append("start again")
                    reply.append(-1)
                    time.sleep(0.1)
                    game_state = "ready to play"
                    rematch_offer = False
            elif data_recieve[0]=="play pos data":
                # flag = data_recieve[1]
                board[data_recieve[1][0]][data_recieve[1][1]] = data_recieve[1][2]
                reply.append("board data")
                reply.append(current_player)
                reply.append(board)
            elif data_recieve[0] == "Resign":
                game_state = "not ready"
                game_ready =[0,0]
                reply.append("you has resign")
                reply.append(-1)
            elif data_recieve[0] == "Rematch":
                rematch_offer = True
                game_ready[player -1] = 1
                reply.append("you have offer rematch")
                reply.append(-1)
            elif data_recieve[0] == "game done":
                game_state = "not ready"
                game_ready =[0,0]
                reply.append("game done")
                reply.append(-1)


            conn.sendall(pickle.dumps(reply))
        except:
            print("Connection has died")
            game_state = "ready to play"
            game_ready = [0,0]
            client[player -1][1] = 0
            current_player -= 1
            break

while True:
    conn, addr = s.accept()
    print("connected to:", addr)
    for i in range(2):
        if client[i][1]==0:
            client[i][1] = 1
            start_new_thread(threaded_client,(conn,client[i][0]))
            current_player += 1
            break