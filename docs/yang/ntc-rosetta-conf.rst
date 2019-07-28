ntc-rosetta-conf
################

This module describes all the operations that ntc-rosetta-conf can perform.

Identities
==========
base: *RESULT*
--------------

Base identity for results

success
-------

**base identity**: RESULT


Operation succeeded

error
-----

**base identity**: RESULT


Operation failed

base: *PLATFORM*
----------------

Base identity for device's platform

ios
---

**base identity**: PLATFORM


IOS device

junos
-----

**base identity**: PLATFORM


Junos device

Data nodes
==========
/device
-------

Top-level container for device configuration and state

**nodetype**: ``container``


-----

/device/config
--------------

Top-level container for device configuration

**nodetype**: ``container``


-----

/device/config/platform
-----------------------

Device platform. Some RPC methods will require you to set this

**nodetype**: ``leaf``

**Type**: ``identityref``


* **base**: ``PLATFORM``



-----

/ping
-----

Ping the server

**nodetype**: ``rpc``


-----

/ping/input
-----------
**nodetype**: ``input``


-----

/ping/output
------------
**nodetype**: ``output``


-----

/ping/output/result
-------------------

Whether the operation succeeded or not

**nodetype**: ``leaf``

**Type**: ``identityref``


* **base**: ``ntc-rosetta-conf:RESULT``



-----

/ping/output/error-message
--------------------------

If the operation failed, message describing the error

**nodetype**: ``leaf``

**Type**: ``string``



-----

/merge
------

Call ntc-rosetta merge method. Visit https://ntc-rosetta.readthedocs.io/en/latest/tutorials/ios_merging.html for details

**nodetype**: ``rpc``


-----

/merge/input
------------
**nodetype**: ``input``


-----

/merge/input/replace
--------------------

Replace argument for the given operation

**nodetype**: ``leaf``

**Type**: ``boolean``



-----

/merge/output
-------------
**nodetype**: ``output``


-----

/merge/output/result
--------------------

Whether the operation succeeded or not

**nodetype**: ``leaf``

**Type**: ``identityref``


* **base**: ``ntc-rosetta-conf:RESULT``



-----

/merge/output/error-message
---------------------------

If the operation failed, message describing the error

**nodetype**: ``leaf``

**Type**: ``string``



-----

/merge/output/native
--------------------

Configuration in native format

**nodetype**: ``leaf``

**Type**: ``string``



-----

/parse
------

Call ntc-rosetta parse method. Visit https://ntc-rosetta.readthedocs.io/en/latest/tutorials/ios_parsing.html for detauls.
Loads the parsed object into the candidate database.

**nodetype**: ``rpc``


-----

/parse/input
------------
**nodetype**: ``input``


-----

/parse/input/native
-------------------

Native confguration to parse

**nodetype**: ``leaf``

**Type**: ``string``



-----

/parse/input/validate
---------------------

Valiadte the configuration prior to load it into the candidate databbase

**nodetype**: ``leaf``

**Type**: ``boolean``



-----

/parse/output
-------------
**nodetype**: ``output``


-----

/parse/output/result
--------------------

Whether the operation succeeded or not

**nodetype**: ``leaf``

**Type**: ``identityref``


* **base**: ``ntc-rosetta-conf:RESULT``



-----

/parse/output/error-message
---------------------------

If the operation failed, message describing the error

**nodetype**: ``leaf``

**Type**: ``string``



-----

/translate
----------

Call ntc-rosetta parse method. Visit https://ntc-rosetta.readthedocs.io/en/latest/tutorials/ios_translate.html

**nodetype**: ``rpc``


-----

/translate/input
----------------
**nodetype**: ``input``


-----

/translate/input/database
-------------------------

Database to translate

**nodetype**: ``leaf``

**Type**: ``enumeration``



-----

/translate/input/replace
------------------------

Replace argument for the given operation

**nodetype**: ``leaf``

**Type**: ``boolean``



-----

/translate/output
-----------------
**nodetype**: ``output``


-----

/translate/output/result
------------------------

Whether the operation succeeded or not

**nodetype**: ``leaf``

**Type**: ``identityref``


* **base**: ``ntc-rosetta-conf:RESULT``



-----

/translate/output/error-message
-------------------------------

If the operation failed, message describing the error

**nodetype**: ``leaf``

**Type**: ``string``



-----

/translate/output/native
------------------------

Configuration in native format

**nodetype**: ``leaf``

**Type**: ``string``



-----



