def myInput(prompt, default=''):
    print(prompt.format(default), end='')
    answer = input()
    if answer == '':
        answer = default
    return answer
