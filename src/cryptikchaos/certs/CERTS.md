
Certificates:
=============

About:
-----

* Process to generate certificate will mostly be automated in future.
* Current format for certificate names is peerid.crt and peerid.key.
* Both certificate and key will be placed in dir `${PROJECT_PATH}/certs/`

Instructions:
------------

* To create a certificate authority, use the CA.pl script:
```/usr/lib/ssl/misc/CA.pl -newca```

* Rename the `demoCA` directory to `cryptikchaosCA`.

* To create a new certificate signing request:
```/usr/lib/ssl/misc/CA.pl -newreq```

* Finally sign the certificate:
```/usr/lib/ssl/misc/CA.pl -sign```

* The last 2 steps will have to be done twice to generate both client and test server keys and certificates not before renaming them respectively.
