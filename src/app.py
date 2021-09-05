#! /usr/bin/env python3 

from pyrow import pyrow as conn
import json
import sys
import time
import requests

import logging.config
import yaml

# configure the logger with a yaml conf file.
with open('src/conf/logger.yaml', 'r') as stream:
    config = yaml.load(stream, Loader=yaml.FullLoader)

logging.config.dictConfig(config)


class DisconnectError(Exception):
    pass

# function that is called at the start of the program and pings the server until it recives a responce. 
def check_connection():
    while True:
        try:
            r =  requests.post('http://127.0.0.1:8000/' , data = json.dumps({'msg' : 'Testconn'}).encode('utf-8'))
            if r.text:
                return True     
        except Exception as e:
            logging.info('Server might be down')
        time.sleep(1)

# func to establish connection to the monitor
# returns the object for comunicating with the monitor 
# exits the program on error
def get_erg():
    try:
        # connect to the monitor
        erg_list = conn.find()
        for i in erg_list:
            return conn.PyErg(i)
    except:
        logging.exception('monitor is not connected')
        sys.exit('An error has occurred. The monitor is not connected.\n Or the user isnt root.')

# function to reconnect to the monitor in case of a disconnect while the app is running.
def reconnect():
    
    r = requests.post('http://127.0.0.1:8000/', data = json.dumps({'msg' : 'DisconnectError'}).encode('utf-8'))
    resp = r.json() 
    print(resp['msg']) # print the responce from the server.
    
    while True:
        erg_list = conn.find()
        for i in erg_list:
            erg = conn.PyErg(i)
            if erg is None:
                time.sleep(1)
            else:
                r = requests.post('http://127.0.0.1:8000/', data = json.dumps({'msg' : 'DisconnectErrorFixed'}).encode('utf-8'))
                resp = r.json()
                print(resp['msg'])
                return erg

# function that converts the data from the monitor to a dict. 
def get_data(monitor):
        # check if the monitor has been disconnected.
    if monitor is None:
        raise DisconnectError()

    data = monitor.get_monitor()

    return {'msg' : 'updateData', 'speed' : data['power'] , 'pace' : data['pace'] , 'distance' : data['distance'] , 'calhr' : data['calhr'] , 'time' : data['time'], "started" : True}

# func that returns the raw data based on the disaired metric
def get_metric(metric , monitor):
    # check if the monitor has been disconnected.
    if monitor is None:
        raise DisconnectError()

    # get the raw data from the monitor 
    data = monitor.get_monitor()
    try:
        return data[metric]
    except:
        logging.info('An invalid metric has been requested from the monitor.')


# the main function that runs the client.
def run():
    if check_connection():
        monitor = get_erg()
        if monitor is None:
            monitor =  reconnect()

    # while loop that send a request to update the speed every X secondes.
    while True:
        try:
            r = requests.post('http://127.0.0.1:8000/', data = json.dumps(get_data(monitor)).encode('utf-8'))
            resp =  r.json()
            print(resp) # print the responce from the server.

            # if the sever send a reset messeage the app will sleep until there is a change in the speed.
            if resp['ended'] == True:
                resp_speed = resp['speed']
                print('game ended')
                time.sleep(10)
                resp_speed  = get_metric('power' , monitor)

                while True:
                    # if the speed from the server and the speed that the monitor is reporting are the same it will sleep. 
                    if resp_speed == get_metric('power' , monitor) or get_metric('power' , monitor) == 0:
                        time.sleep(1)
                    else:
                        r = requests.post('http://127.0.0.1:8000/', data = json.dumps({'msg' : 'gameStarted'}).encode('utf-8'))
                        resp =  r.json()
                        print(resp) # print the responce from the server.
                        break

        except UnboundLocalError:
            logging.warning('Monitor disconnected')
            monitor = reconnect()

        except DisconnectError:
            logging.warning('Monitor disconnected')
            monitor = reconnect()

        except AttributeError:
            logging.info('The monitor is not connected.')

        except Exception as e:
            logging.error(e)
            logging.info('The server might be down.')
        
        time.sleep(0.3) # sleep for 1 secondes. 


if __name__ == '__main__':
    run()    




