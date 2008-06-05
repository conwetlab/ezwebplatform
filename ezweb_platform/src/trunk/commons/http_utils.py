# -*- coding: utf-8 -*-

# MORFEO Project 
# http://morfeo-project.org 
# 
# Component: EzWeb
# 
# (C) Copyright 2004 Telefónica Investigación y Desarrollo 
#     S.A.Unipersonal (Telefónica I+D) 
# 
# Info about members and contributors of the MORFEO project 
# is available at: 
# 
#   http://morfeo-project.org/
# 
# This program is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published by 
# the Free Software Foundation; either version 2 of the License, or 
# (at your option) any later version. 
# 
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
# GNU General Public License for more details. 
# 
# You should have received a copy of the GNU General Public License 
# along with this program; if not, write to the Free Software 
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA. 
# 
# If you want to use this software an plan to distribute a 
# proprietary application in any way, and you are not licensing and 
# distributing your source code under GPL, you probably need to 
# purchase a commercial license of the product.  More info about 
# licensing options is available at: 
# 
#   http://morfeo-project.org/
#

from urlparse import urlparse

from urllib import urlopen, urlcleanup

from django.conf import settings

def download_http_content (uri):
    urlcleanup()
    
    try:
        proxy = settings.PROXY_SERVER
        
        #The proxy must not be used with local address
        host = urlparse(uri)[1]
    
        if (host.startswith(('localhost','127.0.0.1'))):
            proxy = False
        else:
            proxy = {'http': 'http://' + proxy}
            
    except Exception:
        proxy = False
        
    if proxy:
        return urlopen(uri,proxies=proxy).read()
    else:
        return urlopen(uri).read()


def PUT_parameter (request, parameter_name):
    # Checking PUT space!
    value = request.PUT[parameter_name]
    
    if (value):
        return value
    
    # Checking GET and POST space!
    return request.REQUEST[parameter_name]

