from bingo import *
import socket

MAX_BYTES = 65535

def print_card(card):
    print('+----------------+')
    for i in range(5):
        print('| ', end='')
        for j in range(5):
            print('{:2s}'.format(card[i*5+j]), end=' ')
        print('|')
    print('+----------------+')


def client(network, port):
    # create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # set bingo list
    card_status = [False] * 25
    
    # prompt
    print("""
______ _                   
| ___ (_)                  
| |_/ /_ _ __   __ _  ___  
| ___ \ | '_ \ / _` |/ _ \ 
| |_/ / | | | | (_| | (_) |
\____/|_|_| |_|\__, |\___/ 
                __/ |      
               |___/       
            """)
    name = input('Enter your name to join the game: ')
    card = get_card()
    text = name + ',' + ','.join([i for i in card])

    # print bingo card
    print()
    print(f'Hello {name}. Here is your bingo card:')
    print_card(card)

    # send name & numbers to server
    sock.sendto(text.encode('ascii'), (network, port))

    # receive user_id & start_sec from server
    data, address = sock.recvfrom(MAX_BYTES)
    user_id, start_sec = data.decode('ascii').split(',')
    print("You are the {user_id}'th player in the game.")
    print('Game will be started in {start_sec} second(s).')

    # start listen to server to get the lucky number
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        message = data.decode('ascii')

        if message == 'Bingo': # someone has bingo, game over
            print('Somebody has Bingo. Game Over!')
            break
        else: # message is digit
            if message in card:
                idx = card.index(message)
                card_status[idx] = True
            if check(card_status): # Bingo!
                sock.sendto('Bingo'.encode('ascii'), (network, port))
                print('Bingo! You win!')
                break
