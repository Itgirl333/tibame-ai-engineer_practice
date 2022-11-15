x = input()

l = ['+', '*', '-', '/']
for i in l:
    if i in x:
        x = x.split(i)
        if i == '+':
            print(int(x[0]) + int(x[1]))
        elif i == '-':
            print(int(x[0]) - int(x[1]))
        elif i == '*':
            print(int(x[0]) * int(x[1]))
        else:
            print(int(x[0]) // int(x[1]))
