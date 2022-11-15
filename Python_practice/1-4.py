x = input()
# x = '1 3 5 10 11,2 4 5 10 11'

l = x.split(',')[0]
r = x.split(',')[1]

num1 = l.split(' ')
num2 = r.split(' ')

count = 0
for i in num1:
    if i in num2:
        count += 1

if count < 3:
    print(0)
else:
    print(10**(count - 1))
