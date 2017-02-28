# _*_coding:utf-8 _*_

# a = "你好"
# b = a.encode(encoding='utf-8')
# c = b.decode()
# print(c)


def func():
    global x
    x = 2
    print 'x is', x

    print 'Changed local x to', x

def test():
    print(x)

test()
print 'Value of x is', x