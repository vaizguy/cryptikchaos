#! /bin/bash

# Path to profile database
PROFILE_PATH="../../../debug/profile"
# Path to main app
MAIN_SCRIPT="../../main.py"
# Path to test server app
TEST_SCRIPT="./testserver.py"

# Path to profile pstats file
PSTAT_PATH="$PROFILE_PATH/profile.pstats"

## For Profiling
if [[ $1 =~ "profile" ]]; then
    # Launch test server
    xterm -geometry 96x24+0-0 -e \
        "python $TEST_SCRIPT" &

    # Launch the main client
    xterm -geometry 96x24+0+0 -e \
        "python -m cProfile -o $PSTAT_PATH \
        -s time $MAIN_SCRIPT"

    # Convert Profile statistics to a graph diag.
    ${PROFILE_PATH}/gprof2dot.py \
        -f pstats $PSTAT_PATH \
        | dot -Tsvg -o ${PROFILE_PATH}/callgraph.svg

    # Remove pstat file
    rm -f $PSTAT_PATH

## Use webdebugger
elif [[ $1 =~ "webdebug" ]]; then
    # Launch test server
    xterm -geometry 96x24+0-0 -e \
        "python $TEST_SCRIPT" &

    # Starting debug server
    echo "Starting Debug server on http://localhost:5000/"
    # Launch the main client
    xterm -geometry 96x24+0+0 -e \
        "python $MAIN_SCRIPT -m webdebugger"

## No profiling
else
    # Launch test server
    xterm -geometry 96x24+0+0 -e "python $TEST_SCRIPT" &

    # Launch the main client
    xterm -geometry 96x24+0-0 -e "python $MAIN_SCRIPT"
fi


