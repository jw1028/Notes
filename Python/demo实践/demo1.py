#一、使用print方式进行输出（输出的目的地是文件）
fp = open('e:/text.txt','w')
print('奋斗吧', file=fp)
fp.close()

#第二种方式，使用文件读写操作
with open('e:/text1.txt','w') as file:
    file.write('奋斗吧！')
