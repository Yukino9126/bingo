from bingo import *
import socket

MAX_BYTES = 65535

def client(network, port):
    # set socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # set bingo list
    block_status = [False] * 25
    
    name = input('Enter your name:')
    numbers, numbers_str = shuffle()
    text = name + ',' + numbers_str
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
            if message in numbers:
                idx = numbers.index(message)
                block_status[idx] = True
                if check(block_status): # Bingo!
                    sock.sendto('Bingo'.encode('ascii'), (network, port))
                    pass


if __name__ == '__main__':
    client('', 8000)

