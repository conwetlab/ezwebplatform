# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.core import serializers
from django.utils import simplejson

from django_restapi.resource import Resource
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *

from django.db import transaction

from commons.authentication import user_authentication
from commons.get_data import get_igadget_data
from commons.utils import json_encode

from gadget.models import Gadget, VariableDef
from igadget.models import *

@transaction.commit_on_success
def SaveIGadget(igadget, user, screen_id, igadget_id):
    uri = igadget.get('uri')
    if not igadget_id:
        if uri.find('igadgets'):
            igadget_id = uri.partition('/igadgets/')[2]
        else:
            igadget_id = uri.partition('/igadget/')[2]

    gadget_uri = igadget.get('gadget')
    width = igadget.get('width')
    height = igadget.get('height')
    top = igadget.get('top')
    left = igadget.get('left')
   
    if not igadget_id or not uri or not gadget_uri or not width or not height or not top or not left:
        raise Exception('Malformed iGadget JSON')   

    #Gets current user screen
    try:
        screen = Screen.objects.get(id=screen_id)
    except Screen.DoesNotExist: 
        #TODO Screen would have to be created yet. Remove from last release 
        screen_uri = "/user/" + user.username + '/screen/' + str(screen_id)
        screen = Screen (id=screen_id, uri=screen_uri, name='myScreen', user=user) 
        screen.save()            
            
    position = Position (uri=uri + '/position', posX=left, posY=top, height=height, width=width)
    position.save()
            
    try:
        gadget = Gadget.objects.get(uri=gadget_uri)
        new_igadget = IGadget (id=igadget_id ,uri=uri, gadget=gadget, screen=screen, position=position)
        new_igadget.save()
        variableDefs = VariableDef.objects.filter(template=gadget.template)
        for varDef in variableDefs:
            if not gadget.default_value:
                var_value = gadget.default_value
            else:
                var_value = ''
            var = Variable (uri=uri + '/variable/' + varDef.name, vardef=varDef, igadget=new_igadget, value=var_value)
            var.save() 
    except Gadget.DoesNotExist:
        raise Gadget.DoesNotExist('iGadget without associated gadget')
    except VariableDef.DoesNotExist:
        #iGadget has no variables
        pass


class IGadgetCollection(Resource):
    def read(self, request, user_name, screen_id=None):
        user = user_authentication(user_name)
        
        #TODO by default. Remove in final release
        if not screen_id:
            screen_id = 1
        
        data_list = {}
        if not screen_id:
            screens = Screen.objects.filter(user=user)
            for screen in screens:
                igadget = IGadget.objects.filter(screen=screen.id)
                data = serializers.serialize('python', igadget, ensure_ascii=False)
                data_list = [get_igadget_data(d) for d in  data]
        else:
            igadget = IGadget.objects.filter(screen=screen_id)
            data = serializers.serialize('python', igadget, ensure_ascii=False)
            data_list['iGadgets'] = [get_igadget_data(d) for d in  data]
        return HttpResponse(json_encode(data_list), mimetype='application/json; charset=UTF-8')

    @transaction.commit_manually
    def create(self, request, user_name, screen_id=None):
        user = user_authentication(user_name)

        #TODO by default. Remove in final release
        if not screen_id:
            screen_id = 1
        
        if not request.has_key('igadgets'):
            return HttpResponseBadRequest('<error>iGadget JSON expected</error>')

        #TODO we can make this with deserializers (simplejson)      
        received_json = request.POST['igadgets']
	    
        try:
            received_data = eval(received_json)
        except Exception, e:
            return HttpResponseBadRequest('<error>%s</error>' % e)
        igadgets = received_data.get('iGadgets')
        try:
            for igadget in igadgets:
                SaveIGadget(igadget, user, screen_id, igadget_id=None)
            transaction.commit()
            return HttpResponse('ok')
        except Exception, e:
            transaction.rollback()
            return HttpResponseServerError('<error>iGadgets cannot be saved: %s</error>' % e)


class IGadgetEntry(Resource):
    def read(self, request, user_name, igadget_id, screen_id=None):
        user = user_authentication(user_name)
              
        #TODO by default. Remove in final release
        if not screen_id:
            screen_id = 1
        
        data_list = {}
        if not screen_id:
            screens = Screen.objects.filter(user=user)
            for screen in screens:
                igadget = IGadget.objects.filter(id=igadget_id, screen=screen.id)
                data = serializers.serialize('python', igadget, ensure_ascii=False)
                data_list = [get_igadget_data(d) for d in  data]
        else:
            igadget = IGadget.objects.filter(screen=screen_id)
            data = serializers.serialize('python', igadget, ensure_ascii=False)
            igadget_data = get_igadget_data(data[0])
        return HttpResponse(json_encode(igadget_data), mimetype='application/json; charset=UTF-8')
    
    def create(self, request, user_name, igadget_id, screen_id=None):
        user = user_authentication(user_name)

        #TODO by default. Remove in final release
        if not screen_id:
            screen_id = 1

        if not request.has_key('igadget'):
            return HttpResponseBadRequest('<error>iGadget JSON expected</error>')

        #TODO we can make this with deserializers (simplejson)
        received_json = request.POST['igadget']
        
        try:
            igadget = eval(received_json)
        except Exception, e:
            return HttpResponseBadRequest('<error>%s</error>' % e)

        try:
            SaveIGadget(igadget, user, screen_id, igadget_id)
            return HttpResponse('ok')
        except Exception, e:
            return HttpResponseServerError('<error>iGadget cannot be saved: %s</error>' % e)


    def delete(self, request, user_name, igadget_id, screen_id=None):
        user = user_authentication(user_name)

        #TODO by default. Remove in final release
        if not screen_id:
            screen_id = 1

        igadget = get_object_or_404(IGadget, user=user, id=igadget_id)
        igadget.delete()
        
class GadgetVariable(Resource):
    def read(self, request, user_name, igadget_id, var_name, screen_id=None):
        user = user_authentication(user_name)
        igadget = IGadget.objects.get(id=igadget_id, user=user)
        data = serializers.serialize('python', igadget, ensure_ascii=False)
        print data
        #return HttpResponse(json_encode(data_fields), mimetype='application/json; charset=UTF-8')
        return HttpResponse('')
    
    def update(self, request, user_name, igadget_id, var_name, screen_id=None):
        user = user_authentication(user_name)
        gadget = get_object_or_404(Gadget, user=user, vendor=vendor, name=name, version=version)
        gadget.save()
        return HttpResponse('')