Mutual TLS authentication
#########################

``ntc-rosetta-conf`` utilizes mutual TLS (mTLS) for authentication purposes. In this document we are going to quickly see how mutual TLS authentication works in the context of ``ntc-rosetta-conf``

Intro
=====

This introduction mTLS doesn't aim to be an in-depth explanation of how it works, there are plenty of resources out there that aim to do that. Here we are going to just introduce the basic concepts so we have a basic understanding to operate ``ntc-rosetta-conf``

The basic idea of mTLS is that both the client and the server will validate the other party by looking at their certificate. This is done by checking that the certificate authority that signed the other party is (a) the one we expect, (b) cert hasn't expired and (c) cert hasn't been revoked. Let's see an illustration::


   +--------------------------------------------+ +--------------------------------------------+
   |                client CA                   | |                server CA                   |
   |(certificate authority to sign client certs)| |(certificate authority to sign server certs)|
   +--------------------------------------------+ +--------------------------------------------+
             ____/      |      \____                       ____/      |      \____
            |           |           |                     |           |           |
       +---------+ +---------+ +---------+           +---------+ +---------+ +---------+
       | client1 | | client2 | | client3 |           | server1 | | server2 | | server3 |
       +---------+ +---------+ +---------+           +---------+ +---------+ +---------+


                                   mTLS Authentication Overview
          ==============================================================================
   Client| 1. Start tls handshake                                                       |Server
         | ---------------------------------------------------------------------------> |
         |                     A. Send server certificate and request one to the client |
         | <--------------------------------------------------------------------------- |
         | 2. Validate server cert is valid by checking it was signed by "server CA"    |
         | 3. Send client certificate                                                   |
         | ---------------------------------------------------------------------------> |
         |    B. Validate client cert is valid by checking it was signed by "client CA" |
          ==============================================================================

.. note:: This is gross oversimplification of how TLS and mTLS work. Refer to more in-depth guides/documentation if you are interested in knowing how it works.

Tutorial
========

Let's test the theory. Before we start, if you want to follow this tutorial you need:

   1. Docker. Alternatively, you can install `easypki <https://github.com/google/easypki>`_ and use it outside the docker container.
   2. Create folder ``pki_auto_generated_dir`` in your current path: ``mkdir pki_auto_generated_dir``

Clients
-------

First, we need to provide our users with client certificates, so let's create a couple.

Creating the client CA
______________________

To generate client certificates we are going to need a CA. Ideally, such CA would be an intermediate CA signed by a valid CA but as this is dev we are going to just create a root CA::

   $ docker run -v $PWD:/certs -w /certs \
      creatdevsolutions/easypki create \
         --ca \
         --filename client_ca \
         --expire 365 \
         --private-key-size 2048 \
         --organization "NTC" \
         --organizational-unit "Eng" \
         --locality "Stockholm" \
         --country "Sweden" \
         --province "Stockholm" \
         ntc-rosetta-conf-client-authority

Now, you can find under ``pki_auto_generated_dir/client_ca/{certs,keys}`` our CA cert and key::

   $ ls pki_auto_generated_dir/client_ca/{certs,keys}
   pki_auto_generated_dir/client_ca/certs:
   client_ca.crt

   pki_auto_generated_dir/client_ca/keys:
   client_ca.key

Creating client certificates
____________________________

Now that we have a CA to generate client certificates let's create a couple for Jane and John::

   $ docker run -v $PWD:/certs -w /certs \
      creatdevsolutions/easypki create \
         --client \
         --ca-name "client_ca" \
         --expire 365 \
         --private-key-size 2048 \
         --organization "NTC" \
         --organizational-unit "Eng" \
         --locality "Stockholm" \
         --country "Sweden" \
         --province "Stockholm" \
         --email "jane@networktocode.com" \
         jane@networktocode.com

   $ docker run -v $PWD:/certs -w /certs \
      creatdevsolutions/easypki create \
         --client \
         --ca-name "client_ca" \
         --expire 365 \
         --private-key-size 2048 \
         --organization "NTC" \
         --organizational-unit "Eng" \
         --locality "Stockholm" \
         --country "Sweden" \
         --province "Stockholm" \
         --email "john@networktocode.com" \
         john@networktocode.com

Generated certs and keys will be under the same ``client_ca`` folder from before::

   $ls pki_auto_generated_dir/client_ca/{certs,keys}
   pki_auto_generated_dir/client_ca/certs:
   client_ca.crt  jane@networktocode.com.crt  john@networktocode.com.crt

   pki_auto_generated_dir/client_ca/keys:
   client_ca.key  jane@networktocode.com.key  john@networktocode.com.key

Server certificates
-------------------

Now we are going to need a server certificate for each instance of ``ntc-rosetta-conf``.

Server CA
_________

As with the client CA ideally you'd use an intermediate CA signed by a valid CA but, as this is dev, we are going to create our own root CA::

   $ docker run -v $PWD:/certs -w /certs \
      creatdevsolutions/easypki create \
         --ca \
         --filename server_ca \
         --expire 365 \
         --private-key-size 2048 \
         --organization "NTC" \
         --organizational-unit "Eng" \
         --locality "Stockholm" \
         --country "Sweden" \
         --province "Stockholm" \
         ntc-rosetta-conf-server-authority

This time, we will find certs and keys under ``pki_auto_generated_dir/server_ca/{certs,keys}``::

   $ ls pki_auto_generated_dir/server_ca/{certs,keys}
   pki_auto_generated_dir/server_ca/certs:
   server_ca.crt

   pki_auto_generated_dir/server_ca/keys:
   server_ca.key

Creating server certificates
____________________________

Now it's time to generate the certificates for our ``ntc-rosetta-conf`` instances::

   $ docker run -v $PWD:/certs -w /certs \
      creatdevsolutions/easypki create \
         --ca-name "server_ca" \
         --expire 365 \
         --private-key-size 2048 \
         --organization "NTC" \
         --organizational-unit "Eng" \
         --locality "Stockholm" \
         --country "Sweden" \
         --province "Stockholm" \
         rtr00.lab.local

   $ docker run -v $PWD:/certs -w /certs \
      creatdevsolutions/easypki create \
         --ca-name "server_ca" \
         --expire 365 \
         --private-key-size 2048 \
         --organization "NTC" \
         --organizational-unit "Eng" \
         --locality "Stockholm" \
         --country "Sweden" \
         --province "Stockholm" \
         rtr01.lab.local

Certs and keys will be under the same path as the server CA::

   $ ls pki_auto_generated_dir/server_ca/{certs,keys}
   pki_auto_generated_dir/server_ca/certs:
   rtr00.lab.local.crt  rtr01.lab.local.crt  server_ca.crt

   pki_auto_generated_dir/server_ca/keys:
   rtr00.lab.local.key  rtr01.lab.local.key  server_ca.key

Starting ntc-rosetta-conf
-------------------------

Now that everything is ready, let's start ``ntc-rosetta-conf``. Note the options for ``--ssl-crt`` (server cert), ``--ssl-key`` (server key) and ``--ca-crt`` (client CA cert)::

   $ ntc-rosetta-conf serve \
      --datamodel openconfig \
      --pid-file /tmp/ntc-rosetta-conf-demo.pid \
      --log-level debug \
      --data-file data.json \
      --port 8443 \
      --ssl-crt pki_auto_generated_dir/server_ca/certs/rtr00.lab.local.crt \
      --ssl-key pki_auto_generated_dir/server_ca/keys/rtr00.lab.local.key \
      --ca-crt pki_auto_generated_dir/client_ca/certs/client_ca.crt
   2019-07-17 11:54:59,599 INFO     NTC Rosetta Conf version TBD
   2019-07-17 11:54:59,601 INFO     Using config:
   GLOBAL:
     DATA_JSON_FILE: data.json
     LOGFILE: '-'
     LOG_DBG_MODULES:
     - '*'
     LOG_LEVEL: debug
     PERSISTENT_CHANGES: true
     PIDFILE: /tmp/ntc-rosetta-conf-demo.pid
     TIMEZONE: GMT
     VALIDATE_TRANSACTIONS: true
     YANG_LIB_DIR: asda
   HTTP_SERVER:
     API_ROOT: /restconf
     API_ROOT_RUNNING: /restconf_running
     CA_CERT: pki_auto_generated_dir/client_ca/certs/client_ca.crt
     DBG_DISABLE_CERTS: false
     DOC_DEFAULT_NAME: index.html
     DOC_ROOT: doc-root
     LISTEN_LOCALHOST_ONLY: false
     PORT: 8443
     SERVER_NAME: jetconf-h2
     SERVER_SSL_CERT: pki_auto_generated_dir/server_ca/certs/rtr00.lab.local.crt
     SERVER_SSL_PRIVKEY: pki_auto_generated_dir/server_ca/keys/rtr00.lab.local.key
     UPLOAD_SIZE_LIMIT: 1
   NACM:
     ALLOWED_USERS: []
     ENABLED: true

   2019-07-17 11:55:00,571 INFO     Server started on ('::', 8443, 0, 0)

Client
------

Now we can use curl to query ``ntc-rosetta-conf``. Let's start by trying to use curl without using any client cert::

   $ curl \
         --cacert pki_auto_generated_dir/server_ca/certs/server_ca.crt \
         -X GET \
         https://rtr00.lab.local:8443/restconf/data/openconfig-interfaces:interfaces
   curl: (56) OpenSSL SSL_read: SSL_ERROR_SYSCALL, errno 104

We got an SSL error. This is because the handshake failed as the server requested a client certificate. Let's try passing our client cert and key this time::

   $ curl \
      --cacert pki_auto_generated_dir/server_ca/certs/server_ca.crt \
      --cert pki_auto_generated_dir/client_ca/certs/jane@networktocode.com.crt \
      --key pki_auto_generated_dir/client_ca/keys/jane@networktocode.com.key \
      -X GET \
      https://rtr00.lab.local:8443/restconf/data/openconfig-interfaces:interfaces
   {
       "openconfig-interfaces:interfaces": {
           "interface": []
       }
   }

Now we managed to authenticate ourselves with the server.

.. note:: make sure that ``rtr00.lab.local`` resolves the correct IP. You can do that for the sake of testing by editing ``/etc/hosts``.

.. note:: You probably noticed the line ``--cacert pki_auto_generated_dir/server_ca/certs/server_ca.crt``. We need that option because we are using self-signed certificates.
