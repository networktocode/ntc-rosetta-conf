Architecture
============

This document shows a reference architecture for ``ntc-rosetta-conf``. Note that you are free to deploy it in any way that works for you though.

First thing to bear in mind when deploying ``ntc-rosetta-conf`` is that each instance represents a single device. This means that if you have 100 routers you will need 100 instances. This might sound a bit cumbersome but it has the advantage you limit your blast radius in case an instance fails for some reason and it also helps scaling out the solution by spreading the instances across many servers.

To avoid having to run all those instances manually, having to manage all the different ports to avoid collisions and having to remember which port belongs to which router, we recommend running this behind some dockerized solution and behind a load balancer.

A continuation you can see an example of such type of deployment using ``docker-compose`` and ``haproxy``.

haproxy
-------

Let's start looking at the configuration file:

.. include:: files/haproxy/haproxy.cfg
   :literal:


Let's try to summarize what's going on:

1. First we have some globals and defaults, we can ignore those.
2. Next we define a ``frontend``, this is what we are going to consume from the outside. The frontend is going to be responsible of terminating TLS and enforcing mTLS and forwarding SSL headers to the different instances instances of ``ntc-rosetta-conf``. Finally, the ``frontend`` is going to look at the URL path, look for ``/rtr0{0,1}`` and forward the requests to the corresponding instance of ``ntc-rosetta-conf``.
3. Finally, we are going to define a backend per instance of ``ntc-rosetta-conf``. In this example we have two of them. The backend needs to specify how to connect to it and also it needs to remove the ``/rtr0x`` bit from the URL as that's not part of our service.

docker-compose
--------------

``docker-compose`` is going to be responsible of instantiating the loadbalancer and both instances of ``ntc-rosetta-conf``. There isn't a lot of magic here. Just mount the volumes with the configuration for haproxy, the data directories for each instance of ``ntc-rosetta-conf`` and disable ssl on them as it will be terminated on the loadbalancer:

.. include:: files/docker-compose.yaml
   :literal:

After everything is up now you should be able to access each particular instance via ``/rtr00`` and ``/rtr01`` respectively. For instance; ``https://rosetta:65443/rtr00/restconf/data/openconfig-interfaces:interfaces``

This can look like it's going to be a lot if you have hundreds or thousands of devices but as you probably figured already these two configuration files are very easy to template and automate.
