#! /usr/bin/bash 

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "mada\n" | sudo -S git pull

python3 src/server.py &
echo -e "mada\n" | sudo -S python3 src/app.py &

firefox -kiosk http://127.0.0.1/