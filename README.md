
+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
   __                                _ _  __  ___
  /  \  ____.  _*_   ____  __.__ _^_  |  /   /    _     _  .___.  .___  .___.
 /      |    \  |   |    \   |    |   | /   /      |   |   |   |  |   | |   \
/       |____/  |   |____/   |    |   |/___/       |   |   |   |  |   | |
\       |\      |   |        |    |   |\   \       |-+-|   |-+-|  | 0 | |___.
 \      | \     |   |        |    |   | \   \      |   |   |   |  |   |     |
  \__/ _|  \_. _|_ _|        |   _|_ _|_ \__ \___ _|   |_ _|   |_ |___| /___|

+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

CryptikChaos
============

Basic P2P chat client built on kivy and twisted python frameworks.

Instructions:
-------------

To run the application:
* In module `src/cryptikchaos/env/configuration.py` make sure `constants.ENABLE_TEST_MODE = False`
* Go to `src/cryptikchaos/core/`
* run `python main.py` in terminal.

Setting up test environment:
* Go to `src/cryptikchaos/test/`
* run `./run_test_env.sh` in terminal.
* you will currently be prompted for respective pem passwords on any connection request as well as accessing the peer certificates, if `constants.ENABLE_TLS = True`, these are the private passwords used during creation of certificate signing reqest, more instructions are available in `src/cryptikchaos/certs/CERTS.md`. This is still in development.

Run a simple send message test:
-------------------------------

* Enter `addtest` to add test server to swarm.
* Enter `sendtest` to test successful message exchange.
(as commands in running application console)

You should get `Simple Message Transfer Test Passed.` as output on the application console. On the test server you will get a message indicating reciept of random data.

This signifies successful data exchange between client and test server.

Commands Help:
--------------

Type `help` in application console for command information.

Discussion:
-----------

Feel free to leave your queries/suggestions on our [mailing list](mailto:cryptikchaos@googlegroups.com).
