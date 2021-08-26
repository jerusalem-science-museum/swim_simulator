#! /usr/bin/bash 

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

python3 src/server.py &
python3 src/app.py
