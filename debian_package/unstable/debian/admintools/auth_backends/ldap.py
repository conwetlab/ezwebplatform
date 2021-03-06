# -*- coding: utf-8 -*-

#...............................licence...........................................
#
#     (C) Copyright 2008 Telefonica Investigacion y Desarrollo
#     S.A.Unipersonal (Telefonica I+D)
#
#     This file is part of Morfeo EzWeb Platform.
#
#     Morfeo EzWeb Platform is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Morfeo EzWeb Platform is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with Morfeo EzWeb Platform.  If not, see <http://www.gnu.org/licenses/>.
#
#     Info about members and contributors of the MORFEO project
#     is available at
#
#     http://morfeo-project.org
#
#...............................licence...........................................#


#
import os
import shutil

import gettext
from gettext import gettext as _

from configobj import ConfigObj
from admintools.common import Command, AuthMethod
from optparse import make_option

class LDAPResources:
  def __init__(self, resources):
    self.resources = resources

  def get_ldap_settings_path(self):
    return self.resources.CONFIG_BASE_PATH + "ldap.conf"

  def get_ldap_settings(self):
    filename = self.get_ldap_settings_path()

    exists = os.path.exists(filename)
    if exists:
      cfg = ConfigObj(filename, encoding="utf_8")
    else:
      cfg = ConfigObj()
      cfg.filename = filename
      cfg.encoding= "utf_8"

    cfg.initial_comment  = []
    cfg.initial_comment.append("#")
    cfg.initial_comment.append("# DO NOT EDIT THIS FILE")
    cfg.initial_comment.append("#")
    cfg.initial_comment.append("# It is automatically generated by the EzWeb admin tools")
    cfg.initial_comment.append("")

    return cfg

  def save_ldap_settings(self, cfg, backup):
    if backup and os.path.exists(cfg.filename):
      self.resources.printMsg("Backing up \"%s\"... " % cfg.filename)
      shutil.copyfile(cfg.filename, cfg.filename + "~")
      self.resources.printlnMsgNP("Done")

    self.resources.printMsg("Saving EzWeb LDAP settings (%s)... " % cfg.filename)
    cfg.write()
    os.chmod(cfg.filename, 0600)
    self.resources.printlnMsgNP("Done")


class AuthMethod(AuthMethod):

  def __init__(self, resources):
    self.ldapResources = LDAPResources(resources)
    self.resources = resources

  def getMiddlewareClasses(self):
    return []

  def getBackends(self):
    return ['authentication.ldapaccess.LDAPBackend']

  def processConf(self, site_cfg):

    ldap_url = site_cfg.get('ldap', 'server')
    ldap_search_dn = site_cfg.get('ldap', 'search-dn')


    conf  = "# LDAP Auth Backend conf\n"
    conf += "AD_LDAP_URL = '" + ldap_url + "'\n"
    conf += "AD_SEARCH_DN = '" + ldap_search_dn + "'\n"
    return conf

class FillConfigCommand(Command):

  def __init__(self, resources):
    self.ldapResources = LDAPResources(resources)
    self.resources = resources

  def execute(self, site_cfg):

    schema_name = site_cfg.getDefault('default', 'ldap' , 'schema')

    schema = self.ldapResources.get_ldap_settings()

    if schema.has_key(schema_name):
      schema = schema[schema_name]
    else:
      schema = {}

    # LDAP url
    if site_cfg.getDefault('', 'ldap', 'server') == '':
      if schema.has_key("server") and schema["server"] != '':
        site_cfg.set(schema["server"], 'ldap', 'server')
      else:
        site_cfg.set('localhost', 'ldap', 'server')

    # LDAP search DN
    if site_cfg.getDefault('', 'ldap', 'search-dn') == '':
      if schema.has_key("search-dn") and schema["search-dn"] != '':
        site_cfg.set(schema["search-dn"], 'ldap', 'search-dn')
      else:
        site_cfg.set('localhost', 'ldap', 'search-dn')

class UpdateCommand(Command):

  option_list = [make_option("--ldap-server", action="store",
                             dest="ldap_server", help=_("LDAP server to use")),
                 make_option("--ldap-search-dn", action="store",
                             dest="ldap_search_dn", help=_("Distinguished Name"))
                ]

  def __init__(self, resources):
    self.resources = resources

  def execute(self, site_cfg, options):

    if options.ldap_server != None:
      site_cfg.setAndUpdate(options.ldap_server, 'ldap', 'server')

    if options.ldap_search_dn != None:
      site_cfg.setAndUpdate(options.ldap_search_dn, 'ldap', 'search-dn')


class GetDefaultsCommand(Command):
  option_list = []

  def __init__(self, resources):
    self.ldapResources = LDAPResources(resources)

  def execute(self, schema_name, options):
    schema_settings = self.ldapResources.get_ldap_settings()

    if schema_settings.has_key(schema_name):
      cfg = schema_settings[schema_name]
    else:
      cfg = {}

    if cfg.has_key("server"):
      print "SERVER_URL=" + cfg["server"]
    else:
      print "SERVER_URL="

    if cfg.has_key("search-dn"):
      print "SEARCH_DN=" + cfg["search-dn"]
    else:
      print "SEARCH_DN="


class SetDefaultsCommand(Command):
  option_list = [make_option("--ldap-server", action="store",
                             dest="ldap_server", help=_("LDAP server to use")),
                 make_option("--ldap-search-dn", action="store",
                             dest="ldap_search_dn", help=_("Distinguished Name"))
                ]

  def __init__(self, resources):
    self.ldapResources = LDAPResources(resources)

  def execute(self, schema_name, options):
    schema_settings = self.ldapResources.get_ldap_settings()

    if schema_settings.has_key(schema_name):
      cfg = schema_settings[schema_name]
    else:
      schema_settings[schema_name] = {}
      cfg = schema_settings[schema_name]

    if options.ldap_server != None:
      cfg["server"] = options.ldap_server

    if options.ldap_search_dn != None:
      cfg["search-dn"] = options.ldap_search_dn

    self.ldapResources.save_ldap_settings(schema_settings, options.backup)

