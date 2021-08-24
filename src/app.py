#! /usr/bin/env python3 

from pyrow import pyrow as conn
import json
import sys
import time
import requests

class DisconnectError(Exception):
    pass

# func to establish connection to the monitor
# returns the object for comunicating with the monitor 
# exits the program on error
def get_erg():
    try:
        # connect to the monitor
        erg_list = conn.find()
        for i in erg_list:
            erg = conn.PyErg(i)
            print(erg)
            return erg
    except:
        sys.exit('An error has occurred. The monitor is not connected.\n Or the user isnt root.')

# function to reconnect to the monitor in case of a disconnect while the app is running.
def reconnect():
    while True:
        erg_list = conn.find()
        for i in erg_list:
            erg = conn.PyErg(i)
            if erg is None:
                time.sleep(1)
            else:
                return erg


# function that converts the data from the monitor to a dict. 
def get_data(monitor):
        # check if the monitor has been disconnected.
        if monitor is not None:
            data = monitor.get_monitor()
            
            return {'msg' : 'updateData', 'speed' : data['power'] , 'pace' : data['pace'] , 'distance' : data['distance'] , 'calhr' : data['calhr']}
        else:
            raise DisconnectError()

# func that returns the raw data based on the disaired metric
def get_metric(metric , monitor):
    # check if the monitor has been disconnected.
    if monitor is not None:
        # get the raw data from the monitor 
        data = monitor.get_monitor()
        try:
            return data[metric]
        except:
            print('An invalid metric has been requested from the monitor.')
    else:
        raise DisconnectError()


# the main function that runs the client.
def run():
    
    monitor = get_erg()
    if monitor is None:
        monitor =  reconnect()

    # while loop that send a request to update the speed every X secondes.
    while True:
        try:
            r = requests.post('http://127.0.0.1:8000', data = json.dumps(get_data(monitor)).encode('utf-8'))
            print(r.json()) # print the responce from the server.
            resp =  r.json()
            
            # if the sever send a reset messeage the app will sleep until there is a change in the speed.
            if resp['msg'] == 'reset':
                resp_speed = resp['speed']
                while True:
                    # if the speed from the server and the speed that the monitor is reporting are the same it will sleep. 
                    if resp_speed == get_metric('power' , monitor) or get_metric('power' , monitor) == 0:
                        time.sleep(1)
                    else:
                        break

        except UnboundLocalError:
            monitor = reconnect()
        
        except DisconnectError:
            monitor = reconnect()

        except AttributeError:
            print('The monitor is not connected.')

        except Exception as e:
            print('An error has occurred')
            print('The server might be down.')
            pass
        time.sleep(1) # sleep for 1 secondes. 


if __name__ == '__main__':
    
    # if the monitor is disconnected run will return false. 
    # TODO handle the disconnect. 
    run()    




