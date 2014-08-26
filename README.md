![vaizlabs](/src/cryptikchaos/data/vaizlabs_logo.png)

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

Basic ReST Document CLI built on kivy and twisted python.

#####_THIS PROJECT IS PURELY FOR EDUCATIONAL PURPOSES AND IS UNDER DEVELOPMENT._

Screenshot:
-----------

![Cryptikchaos-0.6.1](https://cloud.githubusercontent.com/assets/2795461/4050700/a66b9d06-2d5a-11e4-9259-add88df6a699.png)

Dependencies:
-------------

**Tested with:**

| Module         | Version    | Description        | 
|----------------|------------|--------------------|
| Python         | 2.7.6      | Language           |
| Kivy           | 1.7.2      | Python NUI FWK     | 
| Twisted Python | 13.2.0     | Communications FWK | 
| Pympler        | 0.2.1      | Memory Profiler    |
| Networkx       | 1.8.1      | Network Graph PKG  |
| PyCrypto       | 2.6        | AES Crypto PKG     |

Run Main application:
---------------------

* In module `src/cryptikchaos/core/env/configuration.py` ensure; 
```python
constants.ENABLE_TEST_MODE = False
```
* Go to `src/cryptikchaos/test`
* run `python main.py` in terminal.

Setting up chat test environment:
---------------------------------

**Test Interface and Communications Protocol**
* In module `src/cryptikchaos/core/env/configuration.py` enforce following values;
```python
constants.ENABLE_TEST_MODE = True
constants.ENABLE_TLS = False
```
* If `constants.ENABLE_TLS = True`, you will be prompted for respective pem passwords on any connection request as well as accessing the peer certificates, these are the private passwords used during creation of certificate signing reqest, more instructions are available in `src/cryptikchaos/certs/CERTS.md`. This is still in development.

**Test Communications Protocol with Trial**
* Go to `src/cryptikchaos/core/comm` and run `trial test.test_server` or `./run_test`

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

Visit us at, https://felix-vaizlabs.rhcloud.com


