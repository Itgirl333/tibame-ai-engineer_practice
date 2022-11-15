import sys

in_txt = sys.stdin.read()

# in_txt = """3
# 10,5,20,110
# 12,3,10,92
# 15,5,10,150
# """

lines = in_txt.splitlines()  

def f(a,b,c,d):
    x = (d - c*a) // (b-c)
    y = a - x
    print(x, y, sep=',')

for line in lines[1:]:
    line = line.split(',') 
    a = int(line[0])
    b = int(line[1])
    c = int(line[2])
    d = int(line[3])
    f(a,b,c,d)

    



    
