from socket import *
class UDPserver:
    def __init__(self, port=16000):
        self.port = port

    def runServer(self):
        morseMsg = 1
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind(('Chris', self.port))
        print("The server is ready to receive")
        while 1:
            if morseMsg == 1:
                morseMsg, clientAddress = serverSocket.recvfrom(2048)
            else:
                if clientAddress[1] == 13000:
                    serverSocket.sendto(morseMsg, ('Chris', 12000))  # ie if morse message has an actual string value
                    morseMsg = 1
                else:
                    serverSocket.sendto(morseMsg, ('Chris', 13000))
                    morseMsg = 1


server = UDPserver()
server.runServer()