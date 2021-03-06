# Copyright (c) 2010 Moxie Marlinspike
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA
#

from twisted.internet.protocol import ClientFactory
import logging

class GoogleConnectionFactory(ClientFactory):

    def __init__(self, command, uri, postData, headers, identity, client):
        self.command      = command
        self.uri          = uri
        self.postData     = postData
        self.headers      = headers
        self.identity     = identity
        self.client       = client

    def buildProtocol(self, addr):
        return self.protocol(self.command, self.uri, self.postData, self.headers, self.identity, self.client)
    
    def clientConnectionFailed(self, connector, reason):
        logging.warning("Connection to Google failed!")
        self.client.setResponseCode(int(501), "Server Error")
        self.client.setHeader("Connection", "close")
        self.client.write("<html><body>GoogleSharing connection to Google denied!<p>This means that the GoogleSharing proxy server you have configured was unable to complete a connection to the Google service you requested, or that Google is temporarily refusing connections from that proxy.  Please try again.</body></html>")
        self.client.finish()

