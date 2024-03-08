def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print('Listening at', sock.getsockname())
    delay = 5.0  # seconds
    sock.settimeout(delay)
    num = 1
    while True:
        try:
            data, address = sock.recvfrom(MAX_BYTES)
            text = data.decode('ascii')
            # string -> list
            dim = reclient(text)
            if dim != '':
                message = sendclient(num, sock.getsockname())
                sock.sendto(message.encode('ascii'), address)
            num +=1
        except socket.timeout as exc:
            print('Timeout: I did not receive any message.')


def reclient(text):
    # delete '/join' and change to 2-dimin
    for i in range(0,25):
        recvlist[i] = text[i+1]
    return dim

def sendclient(num, name):
    message = name + ", You are the " + num + 'player\n'
    return message

