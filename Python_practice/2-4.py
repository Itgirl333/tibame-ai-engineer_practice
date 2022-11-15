import sys

in_txt = sys.stdin.read()
in_list = in_txt.split()

# in_list = s.splitlines()
for idx, text in enumerate(in_list, start=1):
    print(f'{text}{idx}')