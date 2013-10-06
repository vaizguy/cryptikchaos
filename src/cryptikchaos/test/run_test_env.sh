rm -rf ../db/*
xterm -e 'sudo python ./test_server.py' &
xterm -e 'sudo python ../core/main.py'
