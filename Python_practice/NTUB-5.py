import sys

in_txt = sys.stdin.read()

# in_txt = """1
# 8 12 21 26 29 32 777 567 65534
# 6 21 22 23 25 32 26 
# """

lines = in_txt.splitlines()  

for i in range(1, len(lines), 2):
    text1 = lines[i].split()[1:]
    text2 = lines[i+1].split()[1:]
    r = set(text1) & set(text2)
    if r:
        print(len(r))
    else:
        print(0)


    



    
