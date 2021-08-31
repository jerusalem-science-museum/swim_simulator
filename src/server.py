import socket 
import json
import sys

HOST = '127.0.0.1'
PORT = 8000


# the server stores the current metrics of the monitor. 
speed = '0'
power = '0'
pace = '0'
distance = '0'
calhr = '0'
disconnect = False
gameEnded = False
gameTime = 30 # time in secondes for each user. 
counter = gameTime 


serverSocket =  socket.socket(socket.AF_INET , socket.SOCK_STREAM)

# server listening on localhost port 8000
try:
    serverSocket.bind(( HOST , PORT))
    serverSocket.listen()
    print(f'Server is up. Listening for requests on {HOST}:{PORT}')
except OSError:
    sys.exit('The address is in use please wait 1 min before trying again')

# function to calculate the speed. 
def calc_speed(speed):
    speed = float(speed / 3)
    speed /= 10
    speed = max(speed, 0)
    speed = min(speed,1.5)
    return speed

while True:
    (clientConnected , clientAddress) = serverSocket.accept()

    # handle connection.
    try:
        tmp = clientConnected.recv(1024)
        data = tmp.decode('utf-8').partition('\r\n\r\n') # extract the massage body.
        print(f"received connection from {clientAddress[0]}:{clientAddress[1]}  Message: {data[2]}")
        msg = json.loads(data[2]) # convert body to json.

        # the server has a list of actions that he can handle.
        # client send a request to update the speed.
        if msg['msg'] == 'updateData':

            speed = msg['speed']
            power = msg['speed']
            pace = round(msg['pace'])
            distance = msg['distance']
            calhr = round(msg['calhr'])


            print(f"Data updated. current speed: {speed} , pace: {pace} , distance: {distance} , calhr: {calhr} ")
            a = {"msg" : "200" , "ended" : gameEnded , "speed" : speed}
            resp = json.dumps(a)

            clientConnected.send(f"""HTTP/1.1 200 OK\nServer: row-sim server 1.0\nAccess-Control-Allow-Origin: * \nContent-Type: application/json \nConnection: keep-alive\n\n{resp}\n""".encode('utf-8'))

            # if the game has ended the valuse are set to 0. 
            if counter < 0 or counter == 0:
                speed = '0'
                power = '0'
                distance = '0'
                calhr = '0'
                pace = '0'

        # if there is a change in the speed the client will send a game started meassage. 
        elif msg['msg'] == 'gameStarted':
            gameEnded = False
            counter = gameTime # reset the game counter. 

            a = {"msg" : "OK"}
            resp = json.dumps(a)

            clientConnected.send(f"""HTTP/1.1 200 OK\nServer: row-sim server 1.0\nAccess-Control-Allow-Origin: * \nContent-Type: application/json \nConnection: keep-alive\n\n{resp}\n""".encode('utf-8'))

        # client requests to receive the current speed 
        elif msg['msg'] == 'getData':
            
            # the web app makes a requests every 1s. 
            # the server will decrement the game counter every time the web app will request the data.
            counter -= 1
            
            # if the counter is 0 end the game. 
            if counter == 0:
                gameEnded = True
                print('game has ended. reseting the values.')

            a = {'speed' : calc_speed(int(speed)) , 'power' : power , 'pace' : pace , 'distance' : distance , 'calhr' : calhr , 'disconnected' : disconnect , "time" : counter}
            resp = json.dumps(a)
            
            clientConnected.send(f"""HTTP/1.1 200 OK\nServer: row-sim server 1.0\nAccess-Control-Allow-Origin: *\nContent-Type: application/json \nConnection: keep-alive\n\n{resp}\n""".encode('utf-8'))
        
        # monitor gets disconnected. 
        elif msg['msg'] == 'DisconnectError':
            disconnect = True

            a = {"msg" : "Disconnected"}
            resp = json.dumps(a)

            clientConnected.send(f"""HTTP/1.1 200 OK\nServer: row-sim server 1.0\nAccess-Control-Allow-Origin: * \nContent-Type: application/json \nConnection: keep-alive\n\n{resp}\n""".encode('utf-8'))

        # monitor gets reconnected. 
        elif msg['msg'] == 'DisconnectErrorFixed':
            disconnect =  False

            a = {"msg" : "Connected"}
            resp = json.dumps(a)

            clientConnected.send(f"""HTTP/1.1 200 OK\nServer: row-sim server 1.0\nAccess-Control-Allow-Origin: * \nContent-Type: application/json \nConnection: keep-alive\n\n{resp}\n""".encode('utf-8'))

        clientConnected.shutdown(1)

    # if there is an error in the request the server will send an responce back.
    except json.decoder.JSONDecodeError:
        disconnect = False
        a = {"msg" : "JsonError"}
        resp = json.dumps(a)

        clientConnected.send(f"""HTTP/1.1 200 OK\nServer: row-sim server 1.0\nAccess-Control-Allow-Origin: * \nContent-Type: application/json \nConnection: keep-alive\n\n{resp}\n""".encode('utf-8'))        
        clientConnected.shutdown(1)
        pass
    
    except Exception as e: 
        print(e)
        a = {"msg" : "error"}
        resp = json.dumps(a)

        clientConnected.send(f"""HTTP/1.1 200 OK\nServer: row-sim server 1.0\nContent-Type: application/json\nConnection: keep-alive\n\n{resp}\n""".encode('utf-8'))