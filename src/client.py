from utils import *
from colors import *
import socket, zmq


def print_card(card, card_status):
    print('+----------------+')
    for i in range(5):
        print('| ', end='')
        for j in range(5):
            if card_status[i*5+j]:
                print(fgRed + '{:2s}'.format(card[i*5+j]) + endColor, end=' ')
            else:
                print('{:2s}'.format(card[i*5+j]), end=' ')
        print('|')
    print('+----------------+')

def init_zmq(host, req_port, sub_port):
    if host =='': host = '*'
    context = zmq.Context()
    # Request
    reqsock = context.socket(zmq.REQ)
    reqsock.connect(f'tcp://{host}:{req_port}')
    # Subscribe
    subsock = context.socket(zmq.SUB)
    subsock.connect(f'tcp://{host}:{sub_port}')
    subsock.setsockopt_string(zmq.SUBSCRIBE, '')
    return reqsock, subsock

def subscribe(zmqsock):
    msg = zmqsock.recv_string()
    return msg

def client(network, reqport, subport):
    # create zmq
    reqsock, subsock = init_zmq(network, reqport, subport)

    # set bingo list
    card_status = [False] * 25
    
    # prompt
    print(fgYellow + """
______ _                   
| ___ (_)                  
| |_/ /_ _ __   __ _  ___  
| ___ \ | '_ \ / _` |/ _ \ 
| |_/ / | | | | (_| | (_) |
\____/|_|_| |_|\__, |\___/ 
                __/ |      
               |___/       
            """ + endColor)
    name = input('Enter your name to join the game: ')
    card = get_card()
    text = name + ',' + ','.join([i for i in card])

    # print bingo card
    print()
    print(f'Hello {name}. Here is your bingo card:')
    print_card(card, card_status)

    # send name & numbers to server
    reqsock.send_string(text)

    # receive user_id & start_sec from server
    data = reqsock.recv_string()
    user_id, start_sec = data.split(',')
    print(f"You are the {user_id} player in the game.")
    print(f"Game will be started in {start_sec} second(s).")

    message = subscribe(subsock)
    print(message)   

    # start listen to server to get the lucky number
    while True:
        message = subscribe(subsock)
        
        if message.split(',')[0] == 'Bingo': # someone has bingo, game over
            # print('Somebody has Bingo. Game Over!')
            print(fgMagenta + message + endColor) # who wins
            print("Game Over.")
            break
        elif message == "Game Over!":
            print("Game Over. No one wins.")
            break
        else: # message is digit
            if message in card:
                idx = card.index(message)
                card_status[idx] = True
                print(message) # card number the server send this time
                print_card(card, card_status)
            
            if check(card_status): # Bingo!        
                data = name + ',Bingo'
                reqsock.send_string(data)
                # server check
                try:
                    reqsock.RCVTIMEO = 2000

                    message = reqsock.recv_string()
                    if message == "You are wrong.":
                        print('You are wrong')
                    elif message == 'You win!':
                        print('You win!')
                except zmq.error.Again:
                    pass
                '''
                    print(bgYellow +'Bingo! You win!' + endColor) 
                    break
                '''
