def shuffle():
    '''
    Return a list and a string of 25 random numbers.
    '''
    import random
    mylist = list(range(1,26))
    print(mylist)
    random.shuffle(mylist)
    string = ','.join([str(i) for i in mylist])
    return mylist, string

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
def check(block_status:list):
    '''
    Check if a 2-dem list bingo.
    '''
    line=0

    for i in checklist:
        if i == block_status:
            line += 1
    if line < 5:
        return False
    else:
        return True

if __name__ == '__main__':
    mylist = map(bool, input().split())
    print(check(mylist))
