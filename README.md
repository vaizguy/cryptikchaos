cryptikchaos
============

Basic P2P chat client built on kivy and twisted python frameworks.

Instructions:
-------------

In Terminal:

To run the test environment to test client commands go to src/cryptikchaos/test and run
```
./run_test_env.sh
```

Type "help" in app console for command help.

To add test server enter;
```
addpeer 888 localhost
```
into the app console.

Then to test successful message exchange enter;
```
test
```
as command, you will get ">>888: Simple Message Transfer Test Passed." as output.
