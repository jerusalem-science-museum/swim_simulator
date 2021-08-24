import socket 
import json


HOST = '127.0.0.1'
PORT = 8000


# the server stores the current metrics of the monitor. 
speed = '0'
pace = '0'
distance = '0'
calhr = '0'
target_speed = '0'


counter = 0

serverSocket =  socket.socket(socket.AF_INET , socket.SOCK_STREAM)

# server listening on localhost port 8000
serverSocket.bind(( HOST , PORT))
serverSocket.listen()
print(f'Server is up. Listening for requests on {HOST}:{PORT}')

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
def calc_speed(speed):
    speed = float(speed / 2)
    speed = speed / 10
    if speed < 0:
        speed = 0
    if speed > 3.8:
        speed = 3.8
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

            # check if the monitor is not in use.
            if not isOff(msg['speed'] , speed):
                speed = msg['speed']
                pace = msg['pace']
                distance = msg['distance']
                calhr = msg['calhr']



                print(f"Data updated. current speed: {speed} , pace: {pace} , distance: {distance} , calhr: {calhr} ")
                a = {"msg" : "200"}
                resp = json.dumps(a)

                clientConnected.send(f"""HTTP/1.1 200 OK\nServer: row-sim server 1.0\nAccess-Control-Allow-Origin: * \nContent-Type: application/json \nConnection: keep-alive\n\n{resp}\n""".encode('utf-8'))

            # if the monitor is not in use reset the valuse.
            else:
                # send the reset message and the current speed. 
                a = {"msg" : "reset" , 'speed' : speed}
                resp = json.dumps(a)

                clientConnected.send(f"""HTTP/1.1 200 OK\nServer: row-sim server 1.0\nAccess-Control-Allow-Origin: * \nContent-Type: application/json \nConnection: keep-alive\n\n{resp}\n""".encode('utf-8'))

                speed = '0'
                pace = '0'
                distance = '0'
                calhr = '0'
                print('Monitor is not in use. reseting the data.')

        
        # client requests to receive the current speed 
        elif msg['msg'] == 'getData':
            
            a = {'speed' : calc_speed(int(speed)) , 'pace' : pace , 'distance' : distance , 'calhr' : calhr}
            resp = json.dumps(a)
            
            clientConnected.send(f"""HTTP/1.1 200 OK\nServer: row-sim server 1.0\nAccess-Control-Allow-Origin: *\nContent-Type: application/json \nConnection: keep-alive\n\n{resp}\n""".encode('utf-8'))
        
        clientConnected.shutdown(1)
    
    # if there is an error in the request the server will send an responce back.
    except json.decoder.JSONDecodeError:
        clientConnected.shutdown(1)
        pass
    except Exception as e: 
        print(e)
        a = {"msg" : "error"}
        resp = json.dumps(a)

        clientConnected.send(f"""HTTP/1.1 200 OK\nServer: row-sim server 1.0\nContent-Type: application/json\nConnection: keep-alive\n\n{resp}\n""".encode('utf-8'))