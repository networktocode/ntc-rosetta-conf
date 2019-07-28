ietf-yang-library
#################

This module contains monitoring information about the YANG
modules and submodules that are used within a YANG-based
server.
Copyright (c) 2016 IETF Trust and the persons identified as
authors of the code.  All rights reserved.
Redistribution and use in source and binary forms, with or
without modification, is permitted pursuant to, and subject
to the license terms contained in, the Simplified BSD License
set forth in Section 4.c of the IETF Trust's Legal Provisions
Relating to IETF Documents
(http://trustee.ietf.org/license-info).
This version of this YANG module is part of RFC 7895; see
the RFC itself for full legal notices.

Types
=====
revision-identifier
-------------------

Represents a specific date in YYYY-MM-DD format.


**type**: ``string``


**pattern**: ``\d{4}-\d{2}-\d{2}``

Data nodes
==========
/modules-state
--------------

Contains YANG module monitoring information.

**nodetype**: ``container``


-----

/modules-state/module-set-id
----------------------------

Contains a server-specific identifier representing
the current set of modules and submodules.  The
server MUST change the value of this leaf if the
information represented by the 'module' list instances
has changed.

**nodetype**: ``leaf``

**Type**: ``string``



-----

/modules-state/module
---------------------

Each entry represents one revision of one module
currently supported by the server.

**nodetype**: ``list``


-----

/modules-state/module/name
--------------------------

The YANG module or submodule name.

**nodetype**: ``leaf`` (list key)

**Type**: ``yang:yang-identifier``



-----

/modules-state/module/revision
------------------------------

The YANG module or submodule revision date.
A zero-length string is used if no revision statement
is present in the YANG module or submodule.

**nodetype**: ``leaf`` (list key)

**Type**: ``union``


*  **Type**: ``revision-identifier``


*  **Type**: ``string``



-----

/modules-state/module/schema
----------------------------

Contains a URL that represents the YANG schema
resource for this module or submodule.
This leaf will only be present if there is a URL
available for retrieval of the schema for this entry.

**nodetype**: ``leaf``

**Type**: ``inet:uri``



-----

/modules-state/module/namespace
-------------------------------

The XML namespace identifier for this module.

**nodetype**: ``leaf``

**Type**: ``inet:uri``



-----

/modules-state/module/feature
-----------------------------

List of YANG feature names from this module that are
supported by the server, regardless of whether they are
defined in the module or any included submodule.

**nodetype**: ``leaf-list``

**Type**: ``yang:yang-identifier``



-----

/modules-state/module/deviation
-------------------------------

List of YANG deviation module names and revisions
used by this server to modify the conformance of
the module associated with this entry.  Note that
the same module can be used for deviations for
multiple modules, so the same entry MAY appear
within multiple 'module' entries.
The deviation module MUST be present in the 'module'
list, with the same name and revision values.
The 'conformance-type' value will be 'implement' for
the deviation module.

**nodetype**: ``list``


-----

/modules-state/module/deviation/name
------------------------------------

The YANG module or submodule name.

**nodetype**: ``leaf`` (list key)

**Type**: ``yang:yang-identifier``



-----

/modules-state/module/deviation/revision
----------------------------------------

The YANG module or submodule revision date.
A zero-length string is used if no revision statement
is present in the YANG module or submodule.

**nodetype**: ``leaf`` (list key)

**Type**: ``union``


*  **Type**: ``revision-identifier``


*  **Type**: ``string``



-----

/modules-state/module/conformance-type
--------------------------------------

Indicates the type of conformance the server is claiming
for the YANG module identified by this entry.

**nodetype**: ``leaf``

**Type**: ``enumeration``


* ``implement``: Indicates that the server implements one or more
protocol-accessible objects defined in the YANG module
identified in this entry.  This includes deviation
statements defined in the module.
For YANG version 1.1 modules, there is at most one
module entry with conformance type 'implement' for a
particular module name, since YANG 1.1 requires that,
at most, one revision of a module is implemented.
For YANG version 1 modules, there SHOULD NOT be more
than one module entry for a particular module name.


* ``import``: Indicates that the server imports reusable definitions
from the specified revision of the module but does
not implement any protocol-accessible objects from
this revision.
Multiple module entries for the same module name MAY
exist.  This can occur if multiple modules import the
same module but specify different revision dates in
the import statements.



-----

/modules-state/module/submodule
-------------------------------

Each entry represents one submodule within the
parent module.

**nodetype**: ``list``


-----

/modules-state/module/submodule/name
------------------------------------

The YANG module or submodule name.

**nodetype**: ``leaf`` (list key)

**Type**: ``yang:yang-identifier``



-----

/modules-state/module/submodule/revision
----------------------------------------

The YANG module or submodule revision date.
A zero-length string is used if no revision statement
is present in the YANG module or submodule.

**nodetype**: ``leaf`` (list key)

**Type**: ``union``


*  **Type**: ``revision-identifier``


*  **Type**: ``string``



-----

/modules-state/module/submodule/schema
--------------------------------------

Contains a URL that represents the YANG schema
resource for this module or submodule.
This leaf will only be present if there is a URL
available for retrieval of the schema for this entry.

**nodetype**: ``leaf``

**Type**: ``inet:uri``



-----

/yang-library-change
--------------------

Generated when the set of modules and submodules supported
by the server has changed.

**nodetype**: ``notification``


-----

/yang-library-change/module-set-id
----------------------------------

Contains the module-set-id value representing the
set of modules and submodules supported at the server at
the time the notification is generated.

**nodetype**: ``leaf``

**Type**: ``leafref``


* **path reference**: ``/modules-state/module-set-id``



-----



