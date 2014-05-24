
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

Dependencies:
-------------

**Tested with:**

Minimum Requirements;

| Module         | Version    | Description        | 
|----------------|------------|--------------------|
| Python         | 2.7.6      | Language           |
| Kivy           | 1.7.2      | Python NUI FWK     | 
| Twisted Python | 13.2.0     | Communications FWK | 

Optional Packages;

| Module   | Version | Description       |
|----------|---------|-------------------|
| Pympler  | 0.2.1   | Memory Profiler   |
| Networkx | 1.8.1   | Network Graph PKG |


Run Main application:
---------------------

* In module `src/cryptikchaos/env/configuration.py` ensure; 
```python
constants.ENABLE_TEST_MODE = False
```
* Go to `src/cryptikchaos/test`
* run `python main.py` in terminal.

Setting up test environment:
----------------------------

* In module `src/cryptikchaos/env/configuration.py` enforce following values;
```python
constants.ENABLE_TEST_MODE = True
constants.ENABLE_TLS = False
```
* If `constants.ENABLE_TLS = True`, you will be prompted for respective pem passwords on any connection request as well as accessing the peer certificates, these are the private passwords used during creation of certificate signing reqest, more instructions are available in `src/cryptikchaos/certs/CERTS.md`. This is still in development.

Run a simple send message test:
-------------------------------

* Set up test environment following the mentioned instructions.
* Go to `src/cryptikchaos/test` directory.
* Run `./run_test_env.sh` script, this will start the console and a test server mimicking an external peer.
* Enter `addtest` in console to add test server to swarm.
* Enter `sendtest` in console to test successful message exchange.

You should get `Simple Message Transfer Test Passed.` as output on the application console. On the test server you will get a message indicating reciept of random data.

This signifies successful data exchange between client and test server.

Commands Help:
--------------

Type `help` in application console for command information.

Discussion:
-----------

Feel free to leave your queries/suggestions on our [mailing list](mailto:cryptikchaos@googlegroups.com).
