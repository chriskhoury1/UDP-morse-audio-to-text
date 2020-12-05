from audioUDPclient import audioUDPclient

client1 = audioUDPclient(13000)
client2 = audioUDPclient(12000)
x = 'a'
while x != 0:  # while the input is not 0, keep prompting the user which client he would like to choose
    if x == 1:  # client 1
        client1.send('Chris', 'morse.wav')  # client1 will send to 'Chris' the file 'morse.wav'
        client2.receive()  # client2 will receive the file from 'Chris' from port 16000
    elif x == 2:  # the opposite for client 2
        client2.send('Chris', 'morse.wav')
        client1.receive()
    x = int(input('Choose which user is the sender (0 to exit): '))



