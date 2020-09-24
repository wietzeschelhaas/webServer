import socket
import sys
import os
import HTTPRequest
import mimetypes

class WebServer:

    #more status codes can be implemented later, not sure if needed tho
    statusCodes = {
        200: 'OK',
        404: 'Not Found',
        501: 'Not Implemented',
    }

    def __init__(self,host="127.0.0.1",port=8887):
        self.host = host
        self.port = port

    def contentType(self, mimeType):
        return ('Content-Type: ' + mimeType + '\r\n').encode() 

    #TODO use this for future necessary headers
    def restHeaders(self):
        pass

    def responseLine(self,statusCode):
        return ('HTTP/1.1 ' + str(statusCode) + self.statusCodes[statusCode] + '\r\n').encode()


    def emptyLine(self):
        return '\r\n'.encode()


    def genRespons(self,code = b"", contentType = b"", body = b"",other= b""):
        return code + contentType + other + self.emptyLine() + body

    #documentation for http:
    #https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages
    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host,self.port))

        #The argument here is the number of unaccepted connections that the system will allow before refusing new connections
        sock.listen(1)

        #receive in chunks of 1024 bytes until an empty string is received
        while 1:
            conn,addr = sock.accept()
            print("HTTP request by : ", addr)

            data = conn.recv(1024)
            #sometimes empty bytes are recevied, this keeps it from crashing
            if not data == b'':
                response = self.handleRequest(data)
                conn.sendall(response)
            conn.close()


    def handleRequest(self,data):

        request = HTTPRequest.HTTPRequest(data.decode(("utf-8")))

        response = None 
  

        #if the method is GET
        if request.method =="GET":
            response = self.getHandle(request)
        elif request.method =="OPTIONS":
            #This methods is used when the client wants to know which request methods is supported by the server.
            response = self.optionHandle(request) 
        else:
            #if the client is trying to use a method not yet implemented by the server:
            respone = self.notImplementedHandle(request)

        return response


    

    def getHandle(self,request):

        #print("GET  ", request.uri)


        body = None
        code = None
        #text content as default
        contentType = self.contentType('text/hmtl')
        
        #Remove the first /
        filePath = request.uri.strip('/')

        #TODO MAKE SURE THAT CLIENT CANNOT ACCESS FILES IT DOES NOT HAVE PREMISSION FOR

        if os.path.exists(filePath):
            code = self.responseLine(200)

            ct = mimetypes.guess_type(filePath)[0]
            if ct == None:
                ct = 'text/hmtl'
            contentType = self.contentType(ct)

            print(contentType)

            with open(filePath,'rb') as f:
                body = f.read()
                
            #body = body.decode("utf-8")

        else:
            #file could not be found so we answer with 404
            code = self.responseLine(404)
            body = '404 Not found'.encode()

        response = self.genRespons(code, contentType,body)
        return response


    def optionHandle(self,request):
        code = self.responseLine(200)
        response = self.genRespons(code=code,other= 'Allow: OPTIONS, GET\r\n'.encode())
        
        return response

    def notImplementedHandle(self,request):
        code = self.responseLine(501)
        body = "<h1> 501 Not Implemented</h1>".encode()

        response = self.genRespons(code=code,body=body)
        return response




if __name__ == "__main__":
    webServer = WebServer()
    webServer.start()

