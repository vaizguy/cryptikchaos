#! /bin/bash

## Path to profile database
PROFILE_PATH="../../../profile"

## For Profiling
if [[ $1 =~ "profile" ]]; then
    # Remove client database
    rm -rf ../db/*_db

    # Launch test server
    xterm -geometry 96x24+0-0 -e \
        'sudo python ./test_server.py' &

    # Launch the main client
    xterm -geometry 96x24+0+0 -e \
        'python -m cProfile -o ./profile.pstats \
        -s time ../core/main.py'

    # Convert Profile statistics to a graph diag.
    ${PROFILE_PATH}/gprof2dot.py \
        -f pstats ./profile.pstats \
        | dot -Tsvg -o ${PROFILE_PATH}/callgraph.svg

    # Remove pstat file
    rm -f ./profile.pstats 

## No profiling
else
    # Remove client database    
    #rm -rf ../db/*_db # Persistant func removed temporarily

    # Launch test server
    xterm -geometry 96x24+0+0 -e 'sudo python ./test_server.py' &

    # Launch the main client
    xterm -geometry 96x24+0-0 -e 'sudo python ../core/main.py'
fi


