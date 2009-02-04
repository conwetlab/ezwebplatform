# -*- coding: cp1252 -*-
from mms import MMSSenderAPI
import web
import sys

class view:       
    def POST(self):

        try:
            parameters = web.input(objectFile={})
            if (not parameters.has_key('login')):
                return web.badrequest()
            login = parameters.get('login')
            
            if (not parameters.has_key('password')):
                return web.badrequest()
            password = parameters.get('password')
            
            if (not parameters.has_key('to')):
                return web.badrequest()
            to = parameters.get('to')
            
            if (not parameters.has_key('attachment')):
                return web.badrequest()
            
            if (not parameters.has_key('objectURL')):
                return web.badrequest()
            
            if (not parameters.has_key('objectFile')):
                return web.badrequest()
            
            if (parameters.get('attachment')=="URL"):
                if (len(parameters.get('objectURL'))==0):
                    return web.badrequest()
                else:
                    objectURL = parameters.get('objectURL')
                    objectFile = None
            elif (parameters.get('attachment')=="File"):
                if (len(parameters.get('objectFile').filename)==0):
                    return web.badrequest()
                else:
                    objectFile = parameters.get('objectFile')
                    objectURL = None
            else:
                return web.badrequest()
            
            if (not parameters.has_key('subject')):
                return web.badrequest()
            subject = parameters.get('subject')
            
            if (not parameters.has_key('message')):
                return web.badrequest()
            message = parameters.get('message')
            mmsender=MMSSenderAPI.MMSSender()
            if objectURL:
                response = mmsender.SendMMSWithURL(login, password, objectURL, subject, to, message)
            else:
                response = mmsender.SendMMSWithFile(login, password, objectFile.value, objectFile.filename, subject, to, message)

            if response.find('Tu mensaje ha sido enviado')>=0:
                print "<html><body><strong>Message sent succesfully!</strong></body></html>"
                return
            print "<html><body><strong>Error sending message!</strong></body></html>"
        except Exception, e:
            web.ctx.status = "500 Internal Server Error"
            web.ctx.headers = [('Content-Type', 'text/html')]
            web.ctx.output = "Message not sent: %s." % e
            
                
        
        