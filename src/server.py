import socket, zmq
import time
from  utils import *
from colors import *
from inputfun import myInput as input


def clientinfo(data:list, client:int):
    """
    Catch player's name & card & order
    """
    # split name & card
    name = data.split(',')[0]
    cardnum = data.split(',')[1:]

    # Which order number?
    if client == 1:
        client = '1st'
    elif client == 2:
        client = '2nd'
    elif client == 3:
        client = '3rd'
    else:
        client = str(client) + 'th'

    return name, cardnum, client


def broadcast(sock:socket.socket, data:str):
    """
    Broadcast to every players.
    """
    sock.send_string(data)

def init_zmq(host, rep_port, pub_port):
    if host =='': host = '*'
    context = zmq.Context()
    # Response
    repsock = context.socket(zmq.REP)
    repsock.bind(f'tcp://{host}:{rep_port}')
    # Publish
    pubsock = context.socket(zmq.PUB)
    pubsock.bind(f'tcp://{host}:{pub_port}')
    return repsock, pubsock

def startgame(repsock, pubsock, clientdict:list):
    """
    Tell the players start game.
    """
    data = "Time is up\n" "Let's start Bingo !!\n"
    broadcast(repsock, data)


def checkBingo(cardnum:list, currentList:list):
    """
    Bouble check if the player lie when he/she send 'Bingo' to the server.
    """
    card_status = [False]*25
    for i in currentList:
        if i in cardnum:
            idx = cardnum.index(i)
            card_status[idx] = True
        if check(card_status): # Bingo!
             return 1
    return 0


def sendnum(repsock, pubsock, clientdict:list, cards:list):
    """
    Send lucky number the players and wait for 2 seconds to recv 'Bingo' from players, then do double check his/her card.
    When the player wins, the server would send the message who the winner is  to the others.
    """
    currentList = []
    
    # Test
    delay = input(bgWhite + fgBlack + "How long do you need to wait the player to send 'Bingo'?(seconds) [default: {}]: " + endColor, 2)

    # send lucky number
    for i in range(len(cards)):
        print('I say ', cards[i])
        
        # broadcast lucky number
        broadcast(pubsock, cards[i])

        # record lucky number has sent
        currentList.append(cards[i])
            
        try:
            # wait 2 seconds check if someone bingo
            repsock.RCVTIMEO = int(delay) * 1000

            # recv 'Bingo' message
            data = repsock.recv_string().split(',')
            if data[1] == 'Bingo':
                print(fgRed + bgYellow + f'message: {data[0]} bingo, please check '+ endColor) # tell server to check if he/she lies
                        
                # check if lie
                for i in range(len(clientdict)):
                   if data[0] in clientdict[i]['name'] and checkBingo(clientdict[i]['cardnum'], currentList):
                       data = 'Bingo,' + clientdict[i]['name']
                       print(data) # tell server who bingo
                       
                       # broadcast to everyone who bingo
                       broadcast(pubsock, data)
                       repsock.send_string('You win!')
                       return 0
                    
                # lie
                repsock.send_string('You are wrong.')
                   
        except zmq.error.Again:
            continue
   

def server(interface:str, repport:int, pubport:int):

    # create ZMQ
    repsock, pubsock = init_zmq(interface, repport, pubport)
    print(f'REP: {interface}:{repport}')
    print(f'PUB: {interface}:{pubport}')
    
    deadline = 0
    client = 0
    clientdict = []
    
    # Test:
    delay = input(bgWhite + fgBlack + "From now on, we will begin in ? seconds [default : {}]: " + endColor, 20)
    
    while True:
        try:
            data = repsock.recv_string()
            
            client += 1 # next player's order
            
            # collect all client's name, card, order
            name, cardnum, clientnum = clientinfo(data, client)
            printplayerinfo = str(clientnum) + " players: " + name + "\ncard: "  
            print(fgGreen + printplayerinfo +  ','.join(str(cardnum[i]) for i in range(25)) + endColor + '\n-------------------------------')
            clientdict.append({'name':name, 'client':clientnum, 'cardnum':cardnum})

            # The game will start until the first player come in
            if client == 1:
                deadline = time.time() + float(delay)
            repsock.RCVTIMEO = int((deadline - time.time()) * 1000)

            # remain time
            remaintime = deadline - time.time()
           
            # The player's order and the remain time
            message = str(clientnum) + ',' + str(int(remaintime))
            repsock.send_string(message)

        except zmq.error.Again:
           # Time is up and start game
           startgame(pubsock, pubsock, clientdict)
           break

    # get lucky number  
    cards = get_card()
    
    # send lucky number
    continuegame = sendnum(repsock, pubsock, clientdict, cards)

    # someone bingo
    if not continuegame :
        print('Game over!')
