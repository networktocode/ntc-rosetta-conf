CLI
===

To start ``ntc-rosetta-cpnf`` you can use its command line::

   $ ntc-rosetta-conf serve --help
   Usage: ntc-rosetta-conf serve [OPTIONS]

   Options:
     --datamodel [openconfig|ntc]    Datamodel to use
     --pid-file TEXT                 PID file
     --log-level [debug|info|warning|error]
                                     Logging level
     --data-file TEXT                Path to json file to load data from and save
                                     on commit
     --listen-on-localhost-only      Listen on localhost only
     --port INTEGER                  Port to listen to
     --ssl-crt TEXT                  SSL Certificate for the webserver
     --ssl-key TEXT                  Private key for the webserver
     --ca-crt TEXT                   CA certificate used to sign client
                                     certificates
     --help                          Show this message and exit.
