consensus 
=========

Overview
--------

''consensus'' is a web application designed to help organisations hold polls 
and elections to find a consensus amongst its stakeholders.

This project is in its very early stages.

Aims
----

''consensus'' will provide an environment where organisations may hold 
elections, some features for the future:

  * When setting up an election, those who are eligible to vote will be very 
    easily specified, either by the user's username, or the role that they hold
    in the organisation

  * Any polling strategy may be used, be it FPTP (Simple Majority), STV or a
    method which is custom to your organisation (some coding to a published 
    interface required ;-) )

  * Easy to install and administer on most platforms (\*BSD, Linux, OS X and 
    Windows will hopefully be supported).
    
Limitations
-----------

Currently, consensus does not support secure voting (in the academic sense). 
Elections are not anonymous, and currently they are suceptible to tampering by
whoever administers the consesus system.

Getting Started
---------------

- cd <directory containing this file>

- $venv/bin/python setup.py develop

- $venv/bin/initialize_consensus_db development.ini

- $venv/bin/pserve development.ini
