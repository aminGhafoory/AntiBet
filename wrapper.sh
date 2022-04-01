#!/bin/bash

# Start the first process
python main.py &
  
# Start the second process
uvicorn api:app --host 0.0.0.0 --port 8000 &
  
# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?

