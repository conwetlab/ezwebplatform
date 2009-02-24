import httplib, urllib, urlparse
import urllib2

CONTENT_TYPE_LIST = {'gif': 'image/gif', 'jpg': 'image/pjpeg', 'jpeg': 'image/pjpeg', 'png': 'image/x-png', 'bmp': 'image/bmp',
                     'mid': 'audio/mid', 'wav': 'audio/wav', 'mp3': 'audio/mpeg',
                     'avi': 'video/avi', 'asf': 'video/x-ms-asf', 'mpg': 'video/mpeg', 'mpeg': 'video/mpeg', 'wmv': 'video/x-ms-wmv'}


class MMSSender :

    login = ''
    user = ''
    cookie = ''
    server = 'multimedia.movistar.es'

    def Login(self, login, pwd) :
        """Performs login to MMS service
            Input:    login=String with user's telephone number
                      pwd=String with user's password"""

        #print 'Login... (http://' + self.server + '/)'

        # We try to access http://multimedia.movistar.es/
        headers = {"User-Agent" : "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)", "Connection" :  "Keep-Alive"}
        conn=httplib.HTTPConnection(self.server)
        conn.request ("GET", "/", None, headers)
        resp=conn.getresponse()
        if resp.status == 302 :

            ## We are redirected and receive a cookie
            cookieSession = ''
            headresp=resp.getheaders()
            #print headresp
            for n in headresp :
                if n[0] == 'set-cookie' :
                    cookieSession = n[1]
                    cookieSession = cookieSession.replace("; Path=/","")
                    cookieSession = cookieSession.replace("; path=/","")

            #print cookieSession
            if cookieSession != '':
                # Sending login data
                params = urllib.urlencode ({'TM_ACTION': 'LOGIN', 'variant': 'mensajeria', 'locale': 'sp-SP', 'client': 'html-msie-7-winxp', 'directMessageView': '', 'uid': '', 'uidl': '', 'folder': '', 'remoteAccountUID': '', 'login': '1', 'TM_LOGIN': login, 'TM_PASSWORD': pwd})
                headers = {"Content-type":"application/x-www-form-urlencoded", "User-Agent" : "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)", "Connection" :  "Keep-Alive"}
                conn=httplib.HTTPConnection(self.server)
                cookieList = cookieSession.split('=')
                url = '/do/dologin;jsessionid='+cookieList[-1]
                self.user = cookieList[-1]
                conn.request ("POST", url, params, headers)
                resp=conn.getresponse()
                headresp=resp.getheaders()

                moreCookies = ''
                for n in headresp :
                    if n[0] == 'set-cookie' :
                        moreCookies = n[1]

                cookieList = moreCookies.split(';')
                moreCookies = cookieList[0]  # We use only the first part
                moreCookies = moreCookies.replace(',', ';')

                self.cookie = cookieSession + '; ' + moreCookies
                #print 'Cookie: ' + self.cookie

                headers2 = {"Accept": "*/*", "Accept-Encoding": "gzip, deflate", "User-Agent" : "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)", "Connection": "Keep-Alive", "Cookie": self.cookie}
                conn2=httplib.HTTPConnection(self.server)
                conn2.request("GET", '/do/multimedia/create?l=sp-SP&v=mensajeria', None, headers2)
                resp2=conn2.getresponse()
                conn2.close()
            
        return self.user

    def InsertFileURL(self, objURL) :
        name = urlparse.urlparse(objURL).path
        # Adding user agent to the request
        req = urllib2.Request(objURL)
        opener = urllib2.build_opener()
        req.add_header('User-Agent','Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8) Gecko/20051111 Firefox/1.5 BAVM/1.0.0')
        obj = opener.open(req).read()
        self.InsertFile(obj, name)
	

    def InsertFile(self, contents, name) :
        """Inserts an image object in MMS message
            Input:  objPath=String with file path"""
            

        path = name.split('.')
        extension = path[-1]
        contentType = CONTENT_TYPE_LIST[extension.lower()]

        #print 'Inserting file... ' + objURL

        separator="---------------------------7d8219060180"

        # generating object data 
        filenamePart = '--' + separator + '\r\nContent-Disposition: form-data; name="file"; filename="' + name + '"\r\nContent-Type: ' + contentType + '\r\n\r\n'

        final = '\r\n--' + separator + '--\r\n'

        data = filenamePart + contents + final

        contentType = "multipart/form-data; boundary="+separator
        headers = {"Content-type": contentType, "Accept-Language": "es", "Accept": "*/*", "User-Agent" : "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)", "Connection": "Keep-Alive", "Accept-Encoding": "gzip, deflate", "Cache-Control": "no-cache", "Cookie": self.cookie}

        conn=httplib.HTTPConnection(self.server)
        conn.request ("POST", "/do/multimedia/uploadEnd", data, headers)
        resp=conn.getresponse()
        response = resp.read()
        conn.close()
        return response


    def SendMessage(self, subject, dest, msg) :
        """Sends an MMS message
            Input:  subject=String with message subject
                      dest=String with destination telephone number
                      msg=String with message text"""

        #print 'Sending message...'

        separator="-----------------------------7d834539300664"

        # generating object data
        basefolderPart = '--' + separator + '\r\nContent-Disposition: form-data; name="basefolder"\r\n\r\n\r\n'
        folderPart = '--' + separator + '\r\nContent-Disposition: form-data; name="folder"\r\n\r\n\r\n'
        idPart = '--' + separator + '\r\nContent-Disposition: form-data; name="id"\r\n\r\n\r\n'
        publicPart = '--' + separator + '\r\nContent-Disposition: form-data; name="public"\r\n\r\n\r\n'
        namePart = '--' + separator + '\r\nContent-Disposition: form-data; name="name"\r\n\r\n\r\n'
        urlPart = '--' + separator + '\r\nContent-Disposition: form-data; name="url"\r\n\r\n\r\n'
        ownerPart = '--' + separator + '\r\nContent-Disposition: form-data; name="owner"\r\n\r\n\r\n'
        deferredDatePart = '--' + separator + '\r\nContent-Disposition: form-data; name="deferredDate"\r\n\r\n\r\n'
        requestReturnReceiptPart = '--' + separator + '\r\nContent-Disposition: form-data; name="requestReturnReceipt"\r\n\r\n\r\n'
        toPart = '--' + separator + '\r\nContent-Disposition: form-data; name="to"\r\n\r\n'+dest+'\r\n'
        subjectPart = '--' + separator + '\r\nContent-Disposition: form-data; name="subject"\r\n\r\n'+subject+'\r\n'
        textPart = '--' + separator + '\r\nContent-Disposition: form-data; name="text"\r\n\r\n'+msg+'\r\n'

        final = '--' + separator + '--\r\n'

        data = basefolderPart + folderPart + idPart + publicPart + namePart + urlPart + ownerPart + deferredDatePart + requestReturnReceiptPart + toPart + subjectPart + textPart + final

        contentType = "multipart/form-data; boundary="+separator

        referer = 'http://multimedia.movistar.es/do/multimedia/show'
        headers = {"Content-Type": contentType, "Accept-Language": "es", "Accept": "image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/x-ms-application, application/vnd.ms-xpsdocument, application/xaml+xml, application/x-ms-xbap, application/x-shockwave-flash, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*", "User-Agent" : "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)", "Connection": "Keep-Alive", "Accept-Encoding": "gzip, deflate", "Cache-Control": "no-cache", "Cookie": self.cookie, "Referer": referer, "Connection": "Keep-Alive", "UA-CPU": "x86"}

        conn=httplib.HTTPConnection(self.server)
        conn.request ("POST", "/do/multimedia/send?l=sp-SP&v=mensajeria", data, headers)
        resp=conn.getresponse()
        response = resp.read()
        
        conn.close()
        return response

    def Logout(self) :
        """Performs MMS service logout"""

        #print 'Logging out...'
        
        paramsLogout = urllib.urlencode ({'TM_ACTION': 'LOGOUT'})

        headersLogout = {"Content-type":"application/x-www-form-urlencoded", "User-Agent" : "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)", "Connection" :  "Keep-Alive", "Cookie": self.cookie}
        connLogout=httplib.HTTPConnection(self.server)
        connLogout.request ("POST", "/do/logout?l=sp-SP&v=mensajeria",paramsLogout, headersLogout)
        respLogout=connLogout.getresponse()

        connLogout.close()
        
    def SendMMSWithURL(self, login, pwd, objURL, subject, dest, msg):
        self.user = self.Login(login, pwd)
        self.InsertFileURL(objURL)
        response = self.SendMessage(subject, dest, msg)
        self.Logout()
        return response

    def SendMMSWithFile(self, login, pwd, objFile, fileName, subject, dest, msg):
        self.user = self.Login(login, pwd)
        self.InsertFile(objFile, fileName)
        response = self.SendMessage(subject, dest, msg)
        self.Logout()
        return response
