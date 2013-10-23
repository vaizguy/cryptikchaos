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
addtest
```
into the app console.

Then to test successful message exchange enter;
```
sendtest
```
into the application console.

You should get;
">>888: Simple Message Transfer Test Passed."
as output on your Application console. On the test server you will get a message indicating
reciept of random data.

This signifies successful data exchange between client and test server.
