import sys

in_txt = sys.stdin.read()

# in_txt = """3
# download
# women
# banana
# naan
# then
# street 
# """

lines = in_txt.splitlines()  

for i in range(1, len(lines), 2):
    text1 = lines[i]
    text2 = lines[i+1]
    r = set(text1) & set(text2)
    if r:
        print(''.join(sorted(r)))
    else:
        print('N')


    



    
