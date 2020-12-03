==============
 Introduction
==============

-------------------------------
A program suite for doing CBGM.
-------------------------------

The program suite consists of:

#. a :mod:`web client <client>`,
#. an :mod:`API server <server>`, and
#. a set of :mod:`scripts` to manipulate the CBGM database.

.. pic:: uml
   :caption: Overview of the program suite

   skinparam backgroundColor transparent

   component "Web Client" as client
   note left of client: javascript

   component "API Server" as api
   note left of api: python

   component "Scripts" as scripts
   note right of scripts: python

   database "Database" as db
   note left of db: postgres

   client --> api
   api --> db
   scripts --> db
   api -[hidden]> scripts

The web client runs in the browser.

The API server can manage multiple databases.
Each book and phase gets its own database.

The scripts can be run manually on the VM to
manage the whole :ref:`CBGM process <cbgm>`, that is:

- importing new books,
- doing the CBGM (passing from one phase to the next),
- and eventually updating the apparatus.


Links
=====

The application is online at: http://ntg.uni-muenster.de/acts/ph4/

The source code is online at: https://github.com/scdh/intf-cbgm/

Developer 2016 - 2020: Marcello Perathoner <marcello.perathoner@uni-koeln.de>
