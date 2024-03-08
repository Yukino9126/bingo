def shuffle():
    '''
    Return a string of 25 random numbers.
    '''
    import random
    mylist = list(range(1,26))
    print(mylist)
    random.shuffle(mylist)
    string = ' '.join([str(i) for i in mylist])
    return string

def check(bingo:list):
    '''
    Check if a 2-dem list bingo.
    '''
    line=0

    for i in range(0,5):
        #if bingo[][] == 
        line += 1

    return
