#!/bin/bash

# Start the server
py server.py &

# Start multiple clients
py client.py &
py client.py &
py client.py &
