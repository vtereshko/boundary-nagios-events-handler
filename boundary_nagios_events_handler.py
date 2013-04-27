#!/usr/bin/env python

# -*- coding: utf-8 -*-

# boundary nagios events handler
# boundary_nagios_events_handler.py

# Copyright (c) 2013 Valentino Tereshko <valentino@boundary.com>
#  Nagios notifications via Boundary Events
#
# This file is part of boundary-nagios-events-handler.
#
# boundary-nagios-events-handler is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import sys

try:
    import json
except ImportError:
    import simplejson as json
try:
    import urllib2
    import base64
    import os
    from optparse import OptionParser
    import ConfigParser
    import datetime
except ImportError, err:
    sys.stderr.write("ERROR: Couldn't load module. %s\n" % err)
    sys.exit(-1)

__all__ = ['parse_options', 'parse_config', 'create_event', 'main', ]

#API_URL= 'https://api.boundary.com'
API_URL= 'http://ashbdrydata07p.ood.ops:8060'

# metadata
__author__ = "Valentino Tereshko"
__email__ = "valentino@boundary.com"
__licence__ = "GPLv3 or later"
__description__ = "Boundary Events via Nagios plugin"
__url__ = "https://github.com/vtereshko/boundary-nagios-events-handler"
VERSION = (0, 1, 3)
__version__ = '.'.join(map(str, VERSION))


# global variables
SCOPE = 'https://www.boundary.com'
DT_FORMAT = '%Y-%m-%dT%H:%M:00.000+02:00'


def parse_options():
    """
    Commandline options arguments parsing.
    """

    # build options and help
    version = "%%prog %s" % __version__
    parser = OptionParser(version=version)
    
    parser.add_option(
        "-m", "--message", metavar="MESSAGE", action="store",
        type="string", dest="message", default="", help="message text"
    )
    parser.add_option(
        "-c", "--config", metavar="CONFIG", action="store",
        type="string", dest="config", help="path to config file",
        default="/etc/boundary-nagios-events-handler.ini")
    parser.add_option(
        "-q", "--quiet", metavar="QUIET", action="store_true",
        default=False, dest="quiet", help="be quiet"
    )

    options = parser.parse_args(sys.argv)[0]

    return options


def parse_config(options):
    """
    Get settings from config file.
    """
    if os.path.exists(options.config):
        config = ConfigParser.ConfigParser()
        try:
            config.read(options.config)
        except Exception:
            if not options.quiet:
                sys.stderr.write("ERROR: Config file read %s error." % options.config)
            sys.exit(-1)

        try:
            configdata = {
		'orgid': config.get('boundary-nagios-events-handler','orgid'),
		'apikey': config.get('boundary-nagios-events-handler','apikey'),
		'message': options.message
            }
        except ConfigParser.NoOptionError, err:
            if not options.quiet:
                sys.stderr.write("ERROR: Config file missing option error. %s\n" % err)
            sys.exit(-1)

        # check mandatory config options supplied
        mandatories = ["orgid","apikey"]
        if not all(configdata[mandatory] for mandatory in mandatories):
            if not options.quiet:
                sys.stdout.write("Mandatory config option missing\n")
            sys.exit(0)

        return configdata
    else:
        if not options.quiet:
            sys.stderr.write("ERROR: Config file %s does not exist\n" % options.config)
        sys.exit(0)


def encode_apikey(apikey):
    b64_auth = base64.encodestring(
            ':'.join([apikey, ''])
            ).replace('\n', '')
    return ' '.join(['Basic', b64_auth])

def create_event(options, config):
    """
    Create event in boundary.
    """
    auth_header = encode_apikey(config['apikey'])
    url = '/'.join([API_URL, config['orgid'], 'events'])
    message = config['message']
    orgid = config['orgid']
    event = {
	'source':{'ref':'Nagios','type':'Nagios'},
	'title': 'Nagios notification',
#	'message' : message,
	'fingerprintFields':['@title'],
	'organizationId': orgid
	    }
   
    event_json = json.dumps(event)
    
    req = urllib2.Request(
            url, event_json, {'Content-type': 'application/json'}
        )

    req.add_header('Authorization', auth_header)
    response = urllib2.urlopen(req)
    # disable this line depending out what Watchtower API returns? invalid json? http? 
    # json.load(response)

def main():
    """
    Processing notification call main function.
    """

    # getting info for creating event
    options = parse_options()
    config = parse_config(options)

    create_event(options, config)


if __name__ == "__main__":
    main()
