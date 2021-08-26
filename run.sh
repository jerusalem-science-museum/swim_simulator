#! /usr/bin/bash 
# TODO abslout path 
# parallel  ::: "sudo python3 src/app.py" "python3 src/server.py"

python3 src/server.py &
python3 src/app.py
