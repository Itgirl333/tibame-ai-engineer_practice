x = input()
# x = '星期六 100 10'

week = x.split(' ')[0]
if week in ['星期五', '星期六', '星期日']:
    print('不開市')
else:
    print(int(x.split(' ')[1]) * int(x.split(' ')[2]))
