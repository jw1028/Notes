#循环输出26个字母对应的ASCII码值
#97代表的是a的ASCII值
x = 97
for X in range(1, 27):
    print(chr(x), '-->', x)
    x += 1
print('-----------------')
x = 97
while x < 123:
    print(chr(x), '-->', x)
    x += 1
