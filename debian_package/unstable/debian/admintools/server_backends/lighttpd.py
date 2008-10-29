import sys
import os
import grp
import shutils

import string
from random import Random

import gettext
from gettext import gettext as _

from admintools.common import Template, Command, EzWebAdminToolResources
from optparse import OptionParser, make_option
from configobj import ConfigObj


class LighttpdResources:

  TEMPLATES_PATH           = "/etc/ezweb-platform/lighttpd-templates/"
  AVAILABLE_SITE_BASE_PATH = "/etc/lighttpd/conf-available/"
  ENABLED_SITE_BASE_PATH   = "/etc/lighttpd/conf-enabled/"
  DEFAULT_LOG_BASE_PATH    = "/var/log/lighttpd/"

  def __init__(self, resources):
    self.resources = resources

  def get_available_link_path(self, conf_name):
    return self.AVAILABLE_SITE_BASE_PATH + "11-ezweb-platform-" + conf_name + ".conf"

  def get_enabled_link_path(self, conf_name):
    return self.ENABLED_SITE_BASE_PATH + "11-ezweb-platform-" + conf_name + ".conf"

  def get_vhost_template(self, connection_type):
    return self.TEMPLATES_PATH + connection_type + ".vhost"

  def get_vhost_path(self, conf_name):
    return self.resources.SITE_CONFIG_BASE_PATH + conf_name + "/lighttpd.vhost"

  def get_log_path(self, conf_name):
    return self.DEFAULT_LOG_BASE_PATH + "ezweb-platform-" + conf_name

  def get_default_admin_email(self, cfg):
    return "webmaster@localhost"

  def get_lighttpd_settings(self):
    filename = self.resources.CONFIG_BASE_PATH + "lighttpd.conf"

    exists = os.path.exists(filename)
    if exists:
      cfg = ConfigObj(filename, encoding="utf_8")
    else:
      cfg = ConfigObj()
      cfg.filename = filename
      cfg.encoding= "utf_8"

    if not cfg.has_key("default"):
      cfg["default"] = {}

    if not isinstance(cfg['default'], dict):
      raise Exception() # TODO

    return cfg


  def save_lighttpd_settings(self, cfg, backup = False):
    if backup and os.path.exists(cfg.filename):
      self.resources.printMsg("Backing up \"%s\"... " % cfg.filename)
      shutil.copyfile(cfg.filename, cfg.filename + "~")
      self.resources.printlnMsgNP("Done")

    cfg.initial_comment  = []
    cfg.initial_comment.append("#")
    cfg.initial_comment.append("# DO NOT EDIT THIS FILE")
    cfg.initial_comment.append("#")
    cfg.initial_comment.append("# It is automatically generated by the EzWeb admin tools")
    cfg.initial_comment.append("")

    self.resources.printMsg("Saving EzWeb Lighttpd settings (" + cfg.filename + ")... ")
    cfg.write()
    os.chmod(cfg.filename, 0600)
    self.resources.printlnMsg("Done")

  def update_vhost(self, cfg):
    templatepath = self.get_vhost_template(cfg['server']['connection_type'])
    try:
      templatefile = open(templatepath, "r")
    except IOError, e:
      if e.errno == 2:
        self.resources.printlnMsg("Unknow connection method \"" + cfg['server']['connection_type'] + "\". May be you need to install support for it.")
        sys.exit(1)
      else:
        raise e

    template = templatefile.read()
    templatefile.close()
    template = Template(template)

    lighttpd_settings = self.get_lighttpd_settings()
    schema_cfg = lighttpd_settings['default']
    server_cfg = cfg['server']

    # Fill the template
    template.replace("CONF_NAME", cfg['name'])
    template.replace("DOCUMENT_ROOT", server_cfg['document_root'])

    if server_cfg.has_key('server_name') and server_cfg['server_name'] != "":
      servername = server_cfg['server_name']
    elif schema_cfg.has_key('server_name') and schema_cfg['server_name'] != "":
      servername = schema_cfg['server_name']
    else:
      servername = "localhost"

    template.replace("SERVER_NAME", servername)

    if server_cfg.has_key('admin_user_email') and server_cfg['admin_user_email']:
      template.replace("SERVER_ADMIN_EMAIL", server_cfg['admin_user_email'])
    else:
      template.replace("SERVER_ADMIN_EMAIL", self.get_default_admin_email(cfg))

    template.replace("LOG_BASE_PATH", self.get_log_path(cfg['name']))

    filepath = self.get_vhost_path(cfg['name'])
    self.resources.printMsg("Updating lighttpd vhost (" + filepath + ")... ")
    file = open(filepath, "w")
    file.write(template)
    file.close()
    self.resources.printlnMsg("Done")

class UpdateCommand(Command):

  option_list = [make_option("--server-name","--server-name", action="store",
                             dest="server_name", help=_("Try to run a dist-upgrade")),
                 make_option("--server-port","--server-port", action="store",
                             dest="server_port", help=_("Try to run a dist-upgrade")),
                 make_option("--document-root","--document-root", action="store",
                             dest="document_root", help=_("Try to run a dist-upgrade")),
                ]

  def __init__(self, resources):
    self.lighttpdResources = LighttpdResources(resources)
    self.resources = resources

  def execute(self, options, site_cfg):
    server_cfg = site_cfg['server']

    if options.document_root != None:
      server_cfg["document_root"] = options.document_root

    if options.server_name != None:
      server_cfg["name"] = options.server_name

    if options.server_port != None:
      server_cfg["port"] = options.server_port

class ProcessCommand(Command):

  option_list = []

  def __init__(self, resources):
    self.lighttpdResources = LighttpdResources(resources)
    self.resources = resources

  def execute(self, site_cfg, options):
    self.lighttpdResources.update_vhost(site_cfg)

    # Creating document root
    self.resources.makedirs(cfg['server']['document_root'])

    # Creating log path and files
    log_path = self.lighttpdResources.get_log_path(cfg['name'])
    self.resources.makedirs(log_path)

    www_group = grp.getgrnam("www-data").gr_gid
    filepath = log_path + "/error.log"
    file = open(filepath, "a")
    file.close()
    os.chown(filepath, -1, www_group)
    os.chmod(filepath, 0660)

    filepath = log_path + "/access.log"
    file = open(filepath, "a")
    file.close()
    os.chown(filepath, -1, www_group)
    os.chmod(filepath, 0660)

    conf_name = site_cfg['name']

    # vhost links
    self.resources.link(self.lighttpdResources.get_vhost_path(conf_name),
                        self.lighttpdResources.get_available_link_path(conf_name))
    self.resources.link(self.lighttpdResources.get_available_link_path(conf_name),
                        self.lighttpdResources.get_enabled_link_path(conf_name))

class PurgeCommand(Command):

  option_list = []

  def __init__(self, resources):
    self.lighttpdResources = LighttpdResources(resources)
    self.resources = resources

  def execute(self, site_cfg, options):
    conf_name = site_cfg['name']
    filepath = self.apache2Resources.get_vhost_path(conf_name)
    try:
      os.remove(filepath)
    except:
      pass

    # unlink vhost files
    self.resources.unlink(self.lighttpdResources.get_vhost_path(conf_name),
                          self.lighttpdResources.get_available_link_path(conf_name))
    self.resources.unlink(self.lighttpdResources.get_available_link_path(conf_name),
                          self.lighttpdResources.get_enabled_link_path(conf_name))


class GetDefaultsCommand(Command):

  option_list = []

  def __init__(self, resources):
    self.lighttpdResources = LighttpdResources(resources)
    self.resources = resources

  def execute(self, schema_name, options):
    schema_settings = self.lighttpdResources.get_lighttpd_settings()

    if schema_settings.has_key(schema_name):
      cfg = schema_settings[schema_name]
    else:
      schema_settings[schema_name] = {}
      cfg = schema_settings[schema_name]

    if cfg.has_key("server_name"):
      print "SERVER_NAME=" + cfg["server_name"]
    else:
      print "SERVER_NAME="

    if cfg.has_key("server_port"):
      print "SERVER_PORT=" + cfg["server_port"]
    else:
      print "SERVER_PORT="


class SetDefaultsCommand(Command):

  option_list = [make_option("--server-name","--server-name", action="store",
                             dest="server_name", help=_("Try to run a dist-upgrade")),
                 make_option("--server-port","--server-port", action="store",
                             dest="server_port", help=_("Try to run a dist-upgrade"))
                ]

  def __init__(self, resources):
    self.lighttpdResources = LighttpdResources(resources)
    self.resources = resources

  def execute(self, schema_name, options):
    schema_settings = self.lighttpdResources.get_lighttpd_settings()

    if schema_settings.has_key(schema_name):
      cfg = schema_settings[schema_name]
    else:
      schema_settings[schema_name] = {}
      cfg = schema_settings[schema_name]

    if options.server_name != None:
      cfg["server_name"] = options.server_name

    if options.server_port != None:
      cfg["server_port"] = options.server_port

    self.lighttpdResources.save_lighttpd_settings(schema_settings)


class ListTypesCommand(Command):

  def __init__(self, resources):
    self.lighttpdResources = LighttpdResources(resources)
    self.resources = resources

  def execute(self):
    for subdir, dirs, files in os.walk(self.lighttpdResources.TEMPLATES_PATH):
      for template in files:
        print("lighttpd " + template.replace(".vhost", "")); # TODO