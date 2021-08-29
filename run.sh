#! /usr/bin/bash 

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


python3 src/server.py &
echo -e "mada\n" | sudo -S python3 src/app.py

sleep 10

xdg-open http://127.0.0.1/
