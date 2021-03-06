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

from django.db import models
from django.utils.translation import ugettext as _

from igadget.models import Variable
from workspace.models import WorkSpaceVariable, AbstractVariable

class InOut(models.Model):
    
    name = models.CharField(_('Name'), max_length=30)
    workspace_variable = models.ForeignKey(WorkSpaceVariable, verbose_name=_('WorkSpaceVariable'))
    friend_code = models.CharField(_('Friend code'), max_length=30, blank=True, null=True)

    def __unicode__(self):
        return str(self.pk) + " " + self.name


class In(models.Model):
    
    name = models.CharField(_('Name'), max_length=30)
    variable = models.ForeignKey(Variable, verbose_name=_('Variable'))  
    inouts = models.ManyToManyField(InOut, verbose_name=_('InOut'))

    def __unicode__(self):
        return str(self.pk) + " " + self.name


class Out(models.Model):
    
    name = models.CharField(_('Name'), max_length=30)
    abstract_variable = models.ForeignKey(AbstractVariable, verbose_name=_('AbstractVariable'))
    inouts = models.ManyToManyField(InOut, verbose_name=_('InOut'))

    def __unicode__(self):
        return str(self.pk) + " " + self.name
