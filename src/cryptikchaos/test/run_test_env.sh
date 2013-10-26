rm -rf ../db/*_db
xterm -geometry 96x24+0+0 -e 'sudo python ./test_server.py' &
xterm -geometry 96x24+0-0 -e 'sudo python ../core/main.py'
