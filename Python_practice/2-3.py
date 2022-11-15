idx = int(input())
# idx = 6
# 0 1 1 2 3 5 8 13 21 …
x, y = 0, 1
z = x + y

if idx == 1:
    print(0)
elif idx == 2:
    print(1)
else:
    while idx > 3:
        x = y
        y = z
        z = x + y
        idx -= 1
    print(z)
