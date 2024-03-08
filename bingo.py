def shuffle():
    '''
    Return a string of 25 random numbers.
    '''
    import random
    mylist = list(range(1,26))
    print(mylist)
    random.shuffle(mylist)
    string = ','.join([str(i) for i in mylist])
    return string

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
        
def check(bingo:list):
    '''
    Check if a 2-dem list bingo.
    '''
    line=0

    '''
    for i in range(0, 5):
        flag1 = False
        flag2 = False

        for j in range(0, 5):
            if bingo[i][j] == bingo[i][j]
                flag1 = True
            if bingo[i][j] == bingo[i][j]
                flag2 = True
        if flag1: line += 1
        if flag2: line += 1
    '''

    return
