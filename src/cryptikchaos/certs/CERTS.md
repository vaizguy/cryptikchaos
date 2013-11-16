
Certificates:
=============

About:
-----

* Process to generate certificate will mostly be automated in future.
* Current format for certificate names is peerid.crt and peerid.key.
* Both certificate and key will be placed in dir `${PROJECT_PATH}/certs/`

Generate key:

`openssl genrsa > peer_id.key`

Generate self-signed SSL certificate: 

`openssl req -new -x509 -key peer_id.key -out peer_id.pem -days 1000`

Replace `peer_id` with actual peer ID
