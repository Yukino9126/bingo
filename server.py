import socket
import bingo
import time
from colors import *
from inputfun import myInput as input

MAX_BYTES = 65535

def clientinfo(data, client):
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
        client == '3rd'
    else:
        client = str(client) + 'th'

    return name, cardnum, client

def startgame(sock, clientdict):
    """
    Tell the players start game.
    """
    for i in range(len(clientdict)):
        data = "Time is up\n" "Let's start Bingo !!\n"
        sock.sendto(data.encode('ascii'), clientdict[i]['address'])
        
def checkBingo(cardnum, currentList):
    """
    Bouble check if the player lie when he/she send 'Bingo' to the server.
    """
    card_status = [False]*25
    for i in currentList:
        if i in cardnum:
            idx = cardnum.index(i)
            card_status[idx] = True
        if bingo.check(card_status): # Bingo!
             return 1
    return 0

def sendnum(sock, clientdict, cards):
    """
    Send lucky number the players and wait for 2 minutes to recv 'Bingo' from players, then do double check his/her card.
    When the player wins, the server would send the message who the winner is  to the others.
    """
    currentList = []
    
    # Test
    delay = input(bgWhite + fgBlack + "How long do you need to wait the player to send 'Bingo'? [default: {}]: " + endColor, 2)

    # send lucky number
    for i in range(len(cards)):
        print('I say ', cards[i])
        
        # broadcast lucky number
        for j in range(len(clientdict)):
            sock.sendto(str(cards[i]).encode('ascii'), clientdict[j]['address'])
            
            # record lucky number has sent
            currentList.append(cards[i])
            
            try:
                # wait 2 minutes check if someone bingo
                sock.settimeout(float(delay))

                # recv 'Bingo' message
                bingomess, address = sock.recvfrom(MAX_BYTES)
                if bingomess.decode('ascii') == 'Bingo':
                    print(fgRed + bgYellow + f'message: {address} bingo, please check '+ endColor) # tell server to check if he/she lies
                    
                    # check if lie
                    for i in range(len(clientdict)):
                        if address[0] in clientdict[i]['address'][0] and checkBingo(clientdict[i]['cardnum'], currentList):
                            data = 'Bingo,' + clientdict[i]['name'] + ' from ' + address[0]
                            print(data) # tell server who bingo
                            # broadcast to everyone who bingo
                            for j in range(len(clientdict)):
                                sock.sendto(data.encode('ascii'), clientdict[j]['address'])
                            return 0
                    
                    # lie
                    sock.sendto('You are wrong.'.encode('ascii'), address)
                   
            except socket.timeout:
                continue
   

def server(interface, port):

    # create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print('Listening at', sock.getsockname())
    
    deadline = 0
    client = 0
    clientdict = []
    
    # Test:
    delay = input(bgWhite + fgBlack + "From now on, we will begin in ? seconds [default : {}]: " + endColor, 20)
    
    while True:
        try:
            # recv name & card
            data, address = sock.recvfrom(MAX_BYTES)
            data = data.decode('ascii')
            #print(data)
            
            client += 1 # next player's order
            
            # collect all client's name, card, order
            name, cardnum, clientnum = clientinfo(data, client)
            printplayerinfo = clientnum + " players: " + name + "\naddress: " + address[0] + "\ncard: "  
            print(fgGreen + printplayerinfo +  ','.join(str(cardnum[i]) for i in range(25)) + endColor + '\n-------------------------------')
            clientdict.append({'name':name, 'client':clientnum, 'address':address, 'cardnum':cardnum})

            # The game will start until the first player come in
            if client == 1:
                deadline = time.time() + float(delay)
            sock.settimeout(deadline - time.time())

            # remain time
            remaintime = deadline - time.time()
           
            # The player's order and the remain time
            message = str(clientnum) + ',' + str(int(remaintime))
            sock.sendto(message.encode('ascii'), address)

        except socket.timeout:
           # Time is up and start game
           startgame(sock, clientdict)
           break

    # get lucky number  
    cards = bingo.get_card()
    
    # send lucky number
    continuegame = sendnum(sock, clientdict, cards)

    # someone bingo
    if not continuegame :
        print('Game over')
        # broadcast to everyone who bingo
    
    # Game over    
    for i in range(len(clientdict)):
        data = "Game Over!"
        sock.sendto(data.encode('ascii'), clientdict[i]['address'])
      
