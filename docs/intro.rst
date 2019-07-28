Intro
=====

``ntc-rosetta-conf`` is a RESTCONF interface for `ntc-rosetta <https://github.com/networktocode/ntc-rosetta>`_. This RESTCONF interface allows you to manipulate a candidate and running databases using supported models by ``ntc-rosetta`` and it also exposes a few RPC endpoints to translate, parse and merge configurations.

Installing
----------

This python package is available through pip so you can install with the following command::

   pip install ntc-rosetta-conf


Starting the restconf interface
-------------------------------

::

   $ ntc-rosetta-conf serve \
     --datamodel openconfig \
     --pid-file /tmp/ntc-rosetta-conf-demo.pid \
     --log-level debug \
     --data-file data.json \
     --port 8443 \
     --ssl-crt pki_auto_generated_dir/server_ca/certs/rtr00.lab.local.crt \
     --ssl-key pki_auto_generated_dir/server_ca/keys/rtr00.lab.local.key \
     --ca-crt pki_auto_generated_dir/client_ca/certs/client_ca.crt

Consuming the restconf interface
--------------------------------

::

   $ curl --http2 -k --cert-type PEM -E $USER_CERT \
       -X GET \
       https://localhost:8443/restconf/data/openconfig-interfaces:interfaces
   {
       "openconfig-interfaces:interfaces": {
           "interface": [
               {
                   "name": "eth0",
                   "config": {
                       "name": "eth0",
                       "description": "an interface description",
                       "type": "iana-if-type:ethernetCsmacd"
                   }
               },
               {
                   "name": "eth1",
                   "config": {
                       "name": "eth1",
                       "description": "another interface",
                       "type": "iana-if-type:ethernetCsmacd"
                   }
               }
           ]
       }
   }
   $ curl -s --http2 -k --cert-type PEM -E $USER_CERT \
       -X POST \
       -d @docs/tutorials/4_translate/translate_running.json \
       $BASE_URL/restconf/operations/ntc-rosetta-conf:translate | jq -r ".native"

   interface eth0
      description an interface description
      exit
   !
   interface eth1
      description another interface
      exit
   !
