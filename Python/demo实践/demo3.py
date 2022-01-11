
def func():
    num = int(input('请输入一个十进制的整数:')) #将str类型转换成int类型
    #第一种写法使用个数可变的位置参数
    print(num, '的二进制数为:', bin(num))
    #第二种写法，使用‘+’作为连接符（+左右均为str类型）
    print(str(num) + '的二进制数为:' + bin(num))
    #第三种方法，格式化字符串
    print('%s的二进制数为%s:' % (num, bin(num)))
    print('{0}的二进制数为:{1}'.format(num, bin(num)))
    print(f'{num}的二进制数为:{bin(num)}')
    print('--------------------------------------')
    print(f'{num}的八进制数为:{oct(num)}')
    print(f'{num}的十六进制数为:{hex(num)}')

if __name__ == '__main__':
    while True:
        try:
            func()
            break
        except:
            print('只能输入整数！请重新输入:')
