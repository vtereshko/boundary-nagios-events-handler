.. boundary-nagios-events-handler
.. README.rst

A boundary-nagios-events-handler documentation
===================================

    *boundary-nagios-events-handler is a Boundary-plugin that posts Nagios notification to Boundary via Boundary's Events API*

    *Based on *nagios-notification-google-calendar (git clone https://github.com/vint21h/nagios-notification-google-calendar.git)*
    *Also based on boundary-splunk-app (https://github.com/boundary/boundary_splunk_app)*

.. contents::

Installation
------------
* Obtain your copy of source code from git repository: ``git clone https://github.com/vtereshko/boundary-nagios-events-handler.git``. Or download latest release from https://github.com/vtereshko/boundary-nagios-events-handler/.
* Run ``python ./setup.py install`` from repository source tree or unpacked archive under root user.

Configuration
-------------
* Read and understand Nagios documentation.
* Add Nagios variable ``$NG$=/usr/bin/boundary_nagios_events_handler.py``
* Create Nagios commands definitions like this:

::

    # 'post-boundary-event' command
    define command{
        command_name    post-boundary-event
        command_line    $NG$/boundary_nagios_events_handler.py -m "Host '$HOSTALIAS$' is $HOSTSTATE$ - Info: $HOSTOUTPUT$" 
    }


* Populate ``/etc/boundary_nagios_events_handler.ini`` with your settings.
* orgid=<org_id>
* apikey=<api_key>
* <org_id> and <api_key> can be found in Boundary App > Organization > Organization Settings

Licensing
---------
boundary-nagios-events-handler is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
For complete license text see COPYING file.


Contacts
--------
**Project Website**: https://github.com/vtereshko/boundary-nagios-events-handler

**Author**: Valentino Tereshko <valentino@boundary.com>
