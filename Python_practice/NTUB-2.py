import sys

in_txt = sys.stdin.read()

# in_txt = """5
# 2,3
# 11,13
# 12,14
# 3,5
# 5,7
# """

lines = in_txt.splitlines()  

def isZhi(x):
    for i in range(2, int(x**0.5)+1):
        if x % i == 0:
            return False
    else:
        return True


for line in lines[1:]:
    x = int(line.split(',')[0])
    y = int(line.split(',')[1])
    if y-x == 2 and isZhi(x) and isZhi(y):
        print('Y')
    else:
        print('N')



    
