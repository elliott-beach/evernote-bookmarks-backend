# start the server
source start.sh

# run tests
pytest test_main.py

# kill the server
# see http://stackoverflow.com/questions/2618403/how-to-kill-all-subprocesses-of-shell
pkill -P $$
