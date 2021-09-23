@[TOC](Linux常用命令)
chmod 777（可读、可写、可执行）用户所有组，用户所在的组，其他用户组
查看进程的指令 ps -aux
查看端口的 netstat -ano | findstr 8080
查看内存/CPU利用率 top
查看ip地址 hostname -i / ip addr /  ipconfig
查看磁盘利用率 df
创建文件 touch
查看日志 git log
从已经提交（commit）的文件中删除文件，并添加新的文件

```sql
从git add中删除一个文件 ： git restore --staged
git commit --amend
git push --force origin zjc_dev
```
回退到之前的commit版本
git reset --hard 目标版本   回退到以前的版本

```sql
git reset --hard 目标版本   回退到以前的版本
```

 - tail

(1) 实时监控100行日志/所有日志

```sql
tail -100f test.log
tail -f test.log
```

(2)查询日志最后100行的日志记录

```sql
tail -n 100 test.log
```

(3)查询日志第100行之后的所有日志记录

```sql
tail -n +100 test.log
```

 - head

head 和 tail 正好相反，tail 是查询后多少行记录，而head 是查询前多少行记录

(1)查询日志的前100行记录

```sql
head -n 100 test.log
```

(2)查询日志文件中除了最后100行所有的记录

```sql
head -n +100 test.log
```

3、cat
tac 是倒序查看，cat反写
(1)查看带有关键字的日志（可以得到关键字附近的行号）

```sql
cat -n test.log | grep '关键字'
```

（2）选择关键字的行号100，然后查看它后20行的日志记录

```sql
cat -n test.log |tail -n +100 |head -n 20
```

解释：tail -n +100 表示查看100行之后的日志记录
      head -n 20 表示再查看100行之后日志记录中的前20行日志记录

4、当日志内容比较多，打印在屏幕上不方便时
(1)使用more、less命令

```sql
cat -n test.log |grep '关键字' |more
```

```sql
cat -n test.log |grep '关键字' |less
```
(2)使用 XXX.txt 将其保存到文件中

```sql
cat test.log |grep '关键字' >test.txt
```
