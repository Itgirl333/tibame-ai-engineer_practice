s = input()
# s = '4 5'
x = int(s.split()[0])
y = int(s.split()[1])

i = 1
while i <= x:
    j = 1
    while j <= y:
        print(f'{i}x{j}={i*j}')
        j += 1
    i += 1
