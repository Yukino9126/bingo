def get_card():
    '''
    Return a list of 25 random numbers(str).
    '''
    import random
    card = list(map(str, list(range(1,26))))
    random.shuffle(card)
    # string = ','.join([str(i) for i in mylist])
    return card

def gen_checklist():
    checklist = []
    for p in range(5):

        # Horizontal
        nulllist = [False]*25
        for i in range(5):
            nulllist[p * 5 + i] = True
        checklist.append(nulllist)

        # Vertical
        nulllist = [False]*25
        for i in range(5):
            nulllist[p + 5 * i] = True
        checklist.append(nulllist)

    # Slash
    nulllist = [False]*25
    for i in 0, 6, 12, 18, 24:
        nulllist[i] = True
    checklist.append(nulllist)
    nulllist = [False]*25
    for i in 4, 8, 12, 16, 20:
        nulllist[i] = True
    checklist.append(nulllist)

    return checklist

checklist = gen_checklist()
def check(card_status:list):
    '''
    Check if a 2-dem list bingo.
    '''
    line=0

    for c in checklist:
        andlist = [ c[i] & card_status[i] for i in range(25) ]
        if c == andlist:
            line += 1
    print(line)
    if line < 5:
        return False
    else:
        return True

if __name__ == '__main__':
    while True:
        mylist = list(map(int, input().split()))
        print(mylist)
        print(check(mylist))
