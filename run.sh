#! /usr/bin/bash 

parallel ::: "python3 src/app.py" "python3 src/server.py"