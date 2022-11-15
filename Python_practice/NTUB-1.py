import sys

in_txt = sys.stdin.read()
lines = in_txt.splitlines()

# s = '1112223334444555566667777'
# s = '54321'
# s = '3337777899922222222222222222'

for s in lines:
    length = 1
    lengths = [1]
    x = int(s[0])
    for i in s[1:]:
        y = int(i)
        if y >= x:
            length += 1
        else:
            length = 1
        lengths.append(length)
        x = y
    print(max(lengths))
    
