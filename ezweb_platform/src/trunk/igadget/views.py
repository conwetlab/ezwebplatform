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

from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import simplejson
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404

from connectable.models import In, Out
from commons.authentication import get_user_authentication, Http403
from commons.get_data import get_igadget_data, get_variable_data
from commons.http_utils import PUT_parameter
from commons.logs_exception import TracedServerError
from commons.resource import Resource
from commons.utils import get_xml_error, json_encode
from gadget.models import Gadget, VariableDef
from gadget.utils import get_or_create_gadget_from_catalogue, get_and_add_gadget
from igadget.models import Position, IGadget, Variable
from workspace.models import Tab, UserWorkSpace, WorkSpace, VariableValue
from workspace.models import  AbstractVariable, SharedVariableValue


def createConnectable(var):
    #If var is and SLOT or and EVENT, a proper connectable object must be created!
    aspect = var.vardef.aspect
    name = var.vardef.name

    connectable = None

    if (aspect == 'SLOT'):
        connectable = Out(name=name, abstract_variable=var.abstract_variable)
    if (aspect == 'EVEN'):
        connectable = In(name=name, variable=var)

    if (connectable == None):
        return {}

    connectable.save()

    connectableId = {}

    connectableId['id'] = connectable.id
    connectableId['name'] = name

    return connectableId


def addIGadgetVariable(igadget, user, varDef, initial_value=None):
    # Sets the default value of variable
    if initial_value:
        var_value = initial_value
    elif varDef.default_value:
        var_value = varDef.default_value
    else:
        var_value = ''

     # Creating the Abstract Variable
    abstractVar = AbstractVariable(type="IGADGET", name=varDef.name)
    abstractVar.save()

    #check if there is a shared value or set a new one
    shared_value = None
    if varDef.shared_var_def:
        shared_value, created = SharedVariableValue.objects.get_or_create(user=user, shared_var_def=varDef.shared_var_def)
        if created:
            #init the value to share
            shared_value.value = var_value
            shared_value.save()
        else:
            #this VariableValue will take the previously shared value
            var_value = shared_value.value

    # Creating Value for Abstract Variable
    variableValue = VariableValue(user=user, value=var_value,
                                  abstract_variable=abstractVar, shared_var_value=shared_value)
    variableValue.save()

    var = Variable(vardef=varDef, igadget=igadget, abstract_variable=abstractVar)
    var.save()

    #Wiring related vars (SLOT&EVENTS) have implicit connectables!
    createConnectable(var)


def SaveIGadget(igadget, user, tab, request):
    gadget_uri = igadget.get('gadget')
    igadget_name = igadget.get('name')
    width = igadget.get('width')
    height = igadget.get('height')
    top = igadget.get('top')
    left = igadget.get('left')
    icon_top = igadget.get('icon_top')
    icon_left = igadget.get('icon_left')
    zIndex = igadget.get('zIndex')
    layout = igadget.get('layout')
    menu_color = igadget.get('menu_color')

    # Creates IGadget position
    position = Position(posX=left, posY=top, posZ=zIndex, height=height, width=width, minimized=False, fulldragboard=False)
    position.save()

    # Creates IGadget icon position
    icon_position = Position(posX=icon_left, posY=icon_top)
    icon_position.save()

    # Creates the new IGadget
    try:
        # Gadget uri does not contain the prefix "/user" yet
        if gadget_uri.startswith("/user") or gadget_uri.startswith("user"):
            gadget_uri_parts = gadget_uri.split("/")
            gadget_uri = "/" + "/".join(gadget_uri_parts[gadget_uri_parts.index("gadgets"):])

        gadget = Gadget.objects.get(uri=gadget_uri, users=user)

        new_igadget = IGadget(name=igadget_name, gadget=gadget, tab=tab, layout=layout, position=position, icon_position=icon_position, transparency=False, menu_color=menu_color)
        new_igadget.save()

        initial_variable_values = None
        if 'variable_values' in request.POST:
            initial_variable_values = simplejson.loads(request.POST['variable_values'])

        variableDefs = VariableDef.objects.filter(gadget=gadget)
        for varDef in variableDefs:
            try:
                initial_value = initial_variable_values[varDef.name]
            except:
                initial_value = None
            addIGadgetVariable(new_igadget, user, varDef, initial_value)

        transaction.commit()

        ids = get_igadget_data(new_igadget, user, tab.workspace)

        return ids

    except Gadget.DoesNotExist, e:
        msg = _('referred gadget %(gadget_uri)s does not exist.') % {'gadget_uri': gadget_uri}

        raise TracedServerError(e, {'igadget': igadget, 'user': user, 'tab': tab}, request, msg)

    except VariableDef.DoesNotExist, e:
        #iGadget has no variables. It's normal
        pass


def UpdateIGadget(igadget, user, tab):

    igadget_pk = igadget.get('id')

    # Checks
    ig = get_object_or_404(IGadget, tab=tab, pk=igadget_pk)

    if 'name' in igadget:
        name = igadget['name']
        ig.name = name

    if 'tab' in igadget:
        newtab_id = igadget['tab']
        if newtab_id < 0:
            raise Exception(_('Malformed iGadget JSON'))

        if newtab_id != tab.id:
            newtab = Tab.objects.get(workspace__users__id=user.id, workspace__pk=tab.workspace_id, pk=newtab_id)
            ig.tab = newtab

    if 'menu_color' in igadget:
        menu_color = igadget['menu_color']
        ig.menu_color = menu_color

    if 'layout' in igadget:
        layout = igadget['layout']
        ig.layout = layout

    if 'transparency' in igadget:
        ig.transparency = igadget['transparency']

    if 'icon_top' in igadget and 'icon_left' in igadget:
        icon_position = ig.icon_position
        if icon_position:
            icon_position.posX = igadget["icon_left"]
            icon_position.posY = igadget["icon_top"]
        else:  # backward compatibility (old gadgets without icon position)
            icon_position = Position(posX=igadget["icon_left"], posY=igadget["icon_top"])
        icon_position.save()
        ig.icon_position = icon_position

    if 'refused_version' in igadget:
        refused_version = igadget['refused_version']
        ig.refused_version = refused_version

    ig.save()

    # get IGadget's position
    position = ig.position

    # update the requested attributes
    if 'width' in igadget:
        width = igadget['width']
        if width <= 0:
            raise Exception(_('Malformed iGadget JSON'))
        position.width = width

    if 'height' in igadget:
        height = igadget['height']
        if height <= 0:
            raise Exception(_('Malformed iGadget JSON'))
        position.height = height

    if 'top' in igadget:
        top = igadget['top']
        if top < 0:
            raise Exception(_('Malformed iGadget JSON'))
        position.posY = top

    if 'left' in igadget:
        left = igadget['left']
        if left < 0:
            raise Exception(_('Malformed iGadget JSON'))
        position.posX = left

    if 'zIndex' in igadget:
        zIndex = igadget['zIndex']
        if not isinstance(zIndex, int):
            raise Exception(_('Malformed iGadget JSON'))
        position.posZ = zIndex

    if 'minimized' in igadget:
        minimized = igadget['minimized']
        if not isinstance(minimized, bool) and not isinstance(minimized, int):
            raise Exception(_('Malformed iGadget JSON'))
        position.minimized = minimized

    if 'fulldragboard' in igadget:
        fulldragboard = igadget['fulldragboard']
        if not isinstance(fulldragboard, bool) and not isinstance(fulldragboard, int):
            raise Exception(_('Malformed iGadget JSON'))
        position.fulldragboard = fulldragboard

    # save the changes
    position.save()


def UpgradeIGadget(igadget, user, new_gadget):
    currentGadget = igadget.gadget

    # get the workspace in which the igadget is being added in order to
    # check if it is shared
    # workspaceId = igadget.tab.workspace.id

    #check equivalency and add the variables needed
    newVariableDefs = VariableDef.objects.filter(gadget=new_gadget)
    equivalentVarDefs = []
    for varDef in newVariableDefs:
        # search for an equivalent variableDef
        equivalentVarDef = VariableDef.objects.filter(name=varDef.name, type=varDef.type, aspect=varDef.aspect, gadget=currentGadget)
        if equivalentVarDef:
            equivalentVarDefs.append(varDef)
            #reassign the variableDef of the Variable
            var = Variable.objects.get(igadget=igadget, vardef=equivalentVarDef[0])
            var.vardef = varDef
            var.save()
        else:
            addIGadgetVariable(igadget, user, varDef)

    # check if the last version gadget hasn't a super-set of the current version gadget variableDefs
    currentGadgetVarDefs = VariableDef.objects.filter(gadget=currentGadget)
    if len(currentGadgetVarDefs) > len(equivalentVarDefs):
        #some of the current version gadget variableDefs aren't in the last version gadget
        raise Exception(_("The gadget cannot be automatically updated because it is incompatible with the last version."))

    igadget.gadget = new_gadget
    igadget.save()


def deleteIGadget(igadget, user):

    if not user.is_superuser:
        workspace = igadget.tab.workspace
        if workspace.creator != user:
            raise Http403

    # Delete all IGadget's variables
    variables = Variable.objects.filter(igadget=igadget)
    for var in variables:
        if (var.vardef.aspect == "SLOT"):
            Out.objects.filter(abstract_variable=var.abstract_variable).delete()

        if (var.vardef.aspect == "EVEN"):
            In.objects.filter(variable=var).delete()

        #Deleting variable value
        VariableValue.objects.filter(abstract_variable=var.abstract_variable).delete()

        var.abstract_variable.delete()
        var.delete()

    # Delete IGadget and its position
    position = igadget.position
    position.delete()
    icon_position = igadget.icon_position
    icon_position.delete()
    igadget.delete()


class IGadgetCollection(Resource):

    def read(self, request, workspace_id, tab_id):
        user = get_user_authentication(request)

        workspace = get_object_or_404(WorkSpace, id=workspace_id)

        data_list = {}
        igadgets = IGadget.objects.filter(tab__workspace__users__id=user.id, tab__workspace__pk=workspace_id, tab__pk=tab_id)
        data_list['iGadgets'] = [get_igadget_data(igadget, user, workspace) for igadget in igadgets]

        return HttpResponse(json_encode(data_list), mimetype='application/json; charset=UTF-8')

    @transaction.commit_on_success
    def create(self, request, workspace_id, tab_id):
        user = get_user_authentication(request)

        if 'igadget' not in request.POST:
            return HttpResponseBadRequest(get_xml_error(_("iGadget JSON expected")), mimetype='application/xml; charset=UTF-8')

        try:
            received_json = request.POST['igadget']
            igadget = simplejson.loads(received_json)
            tab = Tab.objects.get(workspace__users__id=user.id, workspace__pk=workspace_id, pk=tab_id)
            ids = SaveIGadget(igadget, user, tab, request)

            return HttpResponse(json_encode(ids), mimetype='application/json; charset=UTF-8')
        except WorkSpace.DoesNotExist, e:
            msg = _('referred workspace %(workspace_id)s does not exist.') % {'workspace_id': workspace_id}

            raise TracedServerError(e, {'workspace': workspace_id}, request, msg)
        except Exception, e:
            transaction.rollback()
            msg = _("iGadget cannot be created: ") + unicode(e)

            raise TracedServerError(e, {'workspace': workspace_id, 'tab': tab_id}, request, msg)

    @transaction.commit_manually
    def update(self, request, workspace_id, tab_id):
        user = get_user_authentication(request)

        received_json = PUT_parameter(request, 'igadgets')

        if not received_json:
            return HttpResponseBadRequest(get_xml_error(_("iGadget JSON expected")), mimetype='application/xml; charset=UTF-8')

        try:
            tab = Tab.objects.get(workspace__users__id=user.id, workspace__pk=workspace_id, pk=tab_id)
            received_data = simplejson.loads(received_json)
            igadgets = received_data.get('iGadgets')
            for igadget in igadgets:
                UpdateIGadget(igadget, user, tab)

            transaction.commit()

            return HttpResponse('ok')
        except Tab.DoesNotExist, e:
            msg = _('referred tab %(tab_id)s does not exist.') % {'tab_id': tab_id}

            raise TracedServerError(e, {'workspace': workspace_id, 'tab': tab_id}, request, msg)
        except Exception, e:
            transaction.rollback()
            msg = _("iGadgets cannot be updated: ") + unicode(e)

            raise TracedServerError(e, {'workspace': workspace_id, 'tab': tab_id}, request, msg)


class IGadgetEntry(Resource):

    def read(self, request, workspace_id, tab_id, igadget_id):
        user = get_user_authentication(request)

        workspace = get_object_or_404(WorkSpace, id=workspace_id)

        igadget = get_object_or_404(IGadget, tab__workspace__users__id=user.id, tab__workspace=workspace, tab__pk=tab_id, pk=igadget_id)
        igadget_data = get_igadget_data(igadget, user, workspace)

        return HttpResponse(json_encode(igadget_data), mimetype='application/json; charset=UTF-8')

    @transaction.commit_on_success
    def update(self, request, workspace_id, tab_id, igadget_id):
        user = get_user_authentication(request)

        received_json = PUT_parameter(request, 'igadget')

        if not received_json:
            return HttpResponseBadRequest(get_xml_error(_("iGadget JSON expected")), mimetype='application/xml; charset=UTF-8')

        try:
            igadget = simplejson.loads(received_json)
            tab = Tab.objects.get(workspace__users__id=user.id, workspace__pk=workspace_id, pk=tab_id)
            UpdateIGadget(igadget, user, tab)

            return HttpResponse('ok')
        except Tab.DoesNotExist, e:
            msg = _('referred tab %(tab_id)s does not exist.') % {'tab_id': tab_id}

            raise TracedServerError(e, {'workspace': workspace_id, 'tab': tab_id}, request, msg)
        except Exception, e:
            transaction.rollback()
            msg = _("iGadgets cannot be updated: ") + unicode(e)

            raise TracedServerError(e, {'workspace': workspace_id, 'tab': tab_id}, request, msg)

    @transaction.commit_on_success
    def delete(self, request, workspace_id, tab_id, igadget_id):
        user = get_user_authentication(request)

        # Gets Igadget, if it does not exist, a http 404 error is returned
        igadget = get_object_or_404(IGadget, tab__workspace__users__id=user.id, tab__workspace__pk=workspace_id, tab__pk=tab_id, pk=igadget_id)

        deleteIGadget(igadget, user)

        return HttpResponse('ok')


class IGadgetVersion(Resource):

    @transaction.commit_on_success
    def update(self, request, workspace_id, tab_id, igadget_id):
        user = get_user_authentication(request)

        workspace = WorkSpace.objects.get(id=workspace_id)
        if workspace.creator != user:
            raise Http403()

        content_type = request.META.get('CONTENT_TYPE', '')
        if content_type == None:
            content_type = ''

        if content_type.startswith('application/json'):
            received_json = request.raw_post_data
        else:
            received_json = PUT_parameter(request, 'igadget')

        if not received_json:
            return HttpResponseBadRequest(get_xml_error(_("iGadget JSON expected")), mimetype='application/xml; charset=UTF-8')

        try:
            data = simplejson.loads(received_json)
            igadget_pk = data.get('id')

            # get the iGadget object
            igadget = get_object_or_404(IGadget, pk=igadget_pk)

            new_version = data.get('newVersion')
            if workspace.is_shared():
                users = UserWorkSpace.objects.filter(workspace=workspace).values_list('user', flat=True)
            else:
                users = [user]

            if not 'source' in data or data.get('source') == 'catalogue':
                gadget = get_or_create_gadget_from_catalogue(igadget.gadget.vendor, igadget.gadget.name, new_version, user, users, request)
            elif data.get('source') == 'showcase':
                gadget = get_and_add_gadget(igadget.gadget.vendor, igadget.gadget.name, new_version, users)

            UpgradeIGadget(igadget, user, gadget)

            return HttpResponse('ok')
        except Exception, e:
            transaction.rollback()
            msg = unicode(e)

            raise TracedServerError(e, {'workspace': workspace_id, 'tab': tab_id}, request, msg)

        return


class IGadgetVariableCollection(Resource):

    def read(self, request, workspace_id, tab_id, igadget_id):
        user = get_user_authentication(request)

        tab = Tab.objects.get(workspace__users__id=user.id, workspace__pk=workspace_id, pk=tab_id)
        variables = Variable.objects.filter(igadget__tab=tab, igadget__id=igadget_id)
        vars_data = [get_variable_data(variable) for variable in variables]

        return HttpResponse(json_encode(vars_data), mimetype='application/json; charset=UTF-8')

    @transaction.commit_manually
    def update(self, request, workspace_id, tab_id, igadget_id):
        user = get_user_authentication(request)

        received_json = PUT_parameter(request, 'variables')

        # Gets JSON parameter from request
        if not received_json:
            return HttpResponseBadRequest(get_xml_error(_("iGadget variables JSON expected")), mimetype='application/xml; charset=UTF-8')

        try:
            received_variables = simplejson.loads(received_json)

            tab = Tab.objects.get(workspace__users__id=user.id, workspace__pk=workspace_id, pk=tab_id)
            server_variables = Variable.objects.filter(igadget__tab=tab)

            # Gadget variables collection update
            for varServer in server_variables:
                for varJSON in received_variables:
                    if (varServer.vardef.pk == varJSON['pk'] and varServer.igadget.pk == varJSON['iGadget']):
                        varServer.value = varJSON['value']
                        varServer.save()

            transaction.commit()
        except Tab.DoesNotExist, e:
            msg = _('referred tab %(tab_id)s does not exist.') % {'tab_id': tab_id}

            raise TracedServerError(e, {'workspace': workspace_id, 'tab': tab_id, 'igadget': igadget_id}, request, msg)
        except Exception, e:
            transaction.rollback()
            msg = _("igadget varaible cannot be updated: ") + unicode(e)

            raise TracedServerError(e, {'workspace': workspace_id, 'tab': tab_id, 'igadget': igadget_id}, request, msg)

        return HttpResponse("<ok>", mimetype='text/xml; charset=UTF-8')


class IGadgetVariable(Resource):

    def read(self, request, workspace_id, tab_id, igadget_id, var_id):
        user = get_user_authentication(request)

        tab = Tab.objects.get(workspace__user__id=user.id, workspace__pk=workspace_id, pk=tab_id)
        variable = get_object_or_404(Variable, igadget__tab=tab, igadget__pk=igadget_id, vardef__pk=var_id)
        var_data = get_variable_data(variable)

        return HttpResponse(json_encode(var_data), mimetype='application/json; charset=UTF-8')

    def create(self, request, workspace_id, tab_id, igadget_id, var_id):
        return self.update(request, workspace_id, tab_id, igadget_id, var_id)

    def update(self, request, workspace_id, tab_id, igadget_id, var_id):
        user = get_user_authentication(request)

        received_json = PUT_parameter(request, 'value')

        # Gets value parameter from request
        if not received_json:
            return HttpResponseBadRequest(get_xml_error(_("iGadget JSON expected")), mimetype='application/xml; charset=UTF-8')

        new_value = received_json

        tab = Tab.objects.get(workspace__users__id=user.id, workspace__pk=workspace_id, pk=tab_id)
        variable = get_object_or_404(Variable, igadget__tab=tab, igadget__pk=igadget_id, vardef__pk=var_id)
        try:
            variable.value = new_value
            variable.save()
        except Exception, e:
            transaction.rollback()
            msg = _("igadget varaible cannot be updated: ") + unicode(e)

            raise TracedServerError(e, {'workspace': workspace_id, 'tab': tab_id, 'igadget': igadget_id, 'variable': var_id}, request, msg)

        return HttpResponse('ok')
