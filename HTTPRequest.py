class HTTPRequest:

    def __init__(self,data):
        self.method = None
        self.uri = None
        self.httpVersion = '1.1'

        lines = data.split('\r\n')

        #the first line of http request should be the method and which document the client wants to read
        request = lines[0]
        print(lines[0])
        words = request.split(" ")
        self.method = words[0]
        self.uri = words[1]

        if len(words) > 2:
            self.httpVersion = words[2]