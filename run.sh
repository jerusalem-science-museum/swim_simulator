#! /usr/bin/bash 

# parallel  ::: "sudo python3 src/app.py" "python3 src/server.py"

python3 src/server.py & python3 src/app.py