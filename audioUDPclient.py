from socket import *
import os
import socket
from audioToMorse import morseAudioToText

class audioUDPclient:
    def __init__(self, port=13000):  # constructor of class UDPclient, with parameter port which defaults to 13000
        self.port = port

    def send(self, serverName='Chris', msg='morse.wav', serverPort=16000):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # creating the socket at the sending client side
        clientSocket.bind(('', self.port))  # binding it to the address of client

        clientSocket.sendto(msg.encode(), (serverName, serverPort)) # use the sendto function (only in UDP) to
        # send the encoded morse msg (using .encode()) and the address of the server
        clientSocket.close()  # closing the socket we opened

    def receive(self):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # creating the socket at the receiving client side
        clientSocket.bind(('', self.port))  # binding the socket to the address of the receiving client


        morse_msg, serverAddress = clientSocket.recvfrom(2048)  # receive the message from the server using recvfrom
        # only in UDP) and store the address of the server in serverAddress

        recoveredMsg = morseAudioToText(morse_msg, 'alphanumeric')  # implementing the function

        for i in range(1, 100): # here we check if there is another file already created
            if not os.path.exists('./recoveredFile.txt'): # if there is no file, we create one
                file2 = open(r"recoveredFile.txt", "w")  # we use the open function with 'w' or write privileges
                file2.write(recoveredMsg)  # write the converted message on the new txt file
                break
            elif not os.path.exists('./recoveredFile('+str(i)+').txt'): # and we keep on incrementing if the last number of file was taken
                file2 = open('recoveredFile('+str(i)+').txt', "w")
                file2.write(recoveredMsg)
                break  # break so that the full loop doesn't occur (so that we don't create 100 files)
        clientSocket.close()  # close the opened socket
        file2.close()  # close the opened file we used to write the output on
