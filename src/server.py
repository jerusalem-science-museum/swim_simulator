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
gameTime = 30
counter = gameTime 


serverSocket =  socket.socket(socket.AF_INET , socket.SOCK_STREAM)

# server listening on localhost port 8000
try:
    serverSocket.bind(( HOST , PORT))
    serverSocket.listen()
    print(f'Server is up. Listening for requests on {HOST}:{PORT}')
except OSError:
    sys.exit('The address is in use plseas wait 1 min before trying again')
# function to check if the monitor is not in use. 
# it checks the speed and if the speed hasent changed for 15 secondes it returns true.
def isOff(MSGspeed , speed):
    global counter
    if counter == 45:
        counter = 0
        return True
    if speed == MSGspeed:
        counter=counter+1
    return False

# function to calculate the speed based on the limits of the js playback function.
# TODO increse the speed gradualy

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

        # TODO send back reset to the gameended.

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

            if counter < 0 or counter == 0:
                speed = '0'
                power = '0'
                distance = '0'
                calhr = '0'
                pace = '0'

        # TODO send reset compleate msg. 
        elif msg['msg'] == 'gameStarted':
            gameEnded = False
            counter = gameTime

            a = {"msg" : "OK"}
            resp = json.dumps(a)

            clientConnected.send(f"""HTTP/1.1 200 OK\nServer: row-sim server 1.0\nAccess-Control-Allow-Origin: * \nContent-Type: application/json \nConnection: keep-alive\n\n{resp}\n""".encode('utf-8'))

        # client requests to receive the current speed 
        elif msg['msg'] == 'getData':
            
            counter -= 1

            if counter == 0:
                gameEnded = True

                print('game has ended. reseting the values.')

            a = {'speed' : calc_speed(int(speed)) , 'power' : power , 'pace' : pace , 'distance' : distance , 'calhr' : calhr , 'disconnected' : disconnect , "time" : counter}
            resp = json.dumps(a)
            
            clientConnected.send(f"""HTTP/1.1 200 OK\nServer: row-sim server 1.0\nAccess-Control-Allow-Origin: *\nContent-Type: application/json \nConnection: keep-alive\n\n{resp}\n""".encode('utf-8'))
        
        elif msg['msg'] == 'DissconnectError':
            disconnect = True

            a = {"msg" : "Disconnected"}
            resp = json.dumps(a)

            clientConnected.send(f"""HTTP/1.1 200 OK\nServer: row-sim server 1.0\nAccess-Control-Allow-Origin: * \nContent-Type: application/json \nConnection: keep-alive\n\n{resp}\n""".encode('utf-8'))


        
        elif msg['msg'] == 'DissconnectErrorFixed':
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