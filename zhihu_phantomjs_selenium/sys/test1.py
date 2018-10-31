import arg
url = arg.Arg
if url == 'none':
    url = 'default url'
print('from test1')
print(url)

# 爬取过程
def fun(url='12345'):
    print('this is from def fun:',url)

fun(url)

# 调用存储过程