s = input()
# s = 'A123456789'

d = {
    'A': 10,
    'B': 11,
    'C': 12,
    'D': 13,
    'E': 14,
    'F': 15,
    'G': 16,
    'H': 17,
    'I': 34,
    'J': 18,
    'K': 19,
    'L': 20,
    'M': 21,
    'N': 22,
    'O': 35,
    'P': 23,
    'Q': 24,
    'R': 25,
    'S': 26,
    'T': 27,
    'U': 28,
    'V': 29,
    'W': 32,
    'X': 30,
    'Y': 31,
    'Z': 33
}

x = d[s[0]]
num1 = x // 10 + x % 10 * 9

y = [int(s[i]) * (9 - i) for i in range(1, 10)]
num2 = sum(y) + int(s[-1])

if (num1 + num2) % 10:
    print('不合法')
else:
    print('合法')


