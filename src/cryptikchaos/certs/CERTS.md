
Certificates:
=============

About:
-----

* Process to generate certificate will mostly be automated in future.
* Current format for key and certificate names is peerid.key and peerid.crt.
* Both certificate, key and CA should be generated in directory, `${PROJECT_PATH}/certs/`

Instructions:
------------

* Go to the `${PROJECT_PATH}/certs/` directory.

* To create a certificate authority, use the CA.pl script:
```/usr/lib/ssl/misc/CA.pl -newca```

* Rename the `demoCA` directory to `cryptikchaosCA`.

* To create a new certificate signing request:
```/usr/lib/ssl/misc/CA.pl -newreq```

* Finally sign the certificate:
```/usr/lib/ssl/misc/CA.pl -sign```

* to prevent passwords from having to be manually entered you can use the openssl command to decrypt the keys:
```openssl rsa -in newkey.pem -out newrsakey.pem```

* The last 2 steps will have to be done twice to generate both client and test server keys and certificates not before renaming them respectively with required .crt and .key extensions.
