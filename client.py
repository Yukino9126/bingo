from bingo import *
import socket

MAX_BYTES = 65535

def client(network, port):
    # set broadcast
    # broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    # set unicast
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    name = input('Enter your name:')
    numbers = shuffle()
    text = name + ',' + numbers
    # print(text)

    # send name & numbers to server
    sock.sendto(text.encode('ascii'), (network, port))

    # receive data from server
    data, address = sock.recvfrom(MAX_BYTES)
    user_id, start_sec = data.decode('ascii').split(',')

    print(user_id, start_sec)

    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        message = data.decode('ascii')

        if message == 'Bingo':
            print('Somebody is Bingo, game over!')
            break
        else: # message is digit
            pass




if __name__ == '__main__':
    client('', 8000)

