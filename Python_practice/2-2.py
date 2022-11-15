s = input()

# s = '1 2 3 4 5'
x = s.split()
y = ''
for i in x:
    y = y + ' ' + str(int(i) + 1)
print(y)