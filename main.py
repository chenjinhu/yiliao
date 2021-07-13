# 这是一个示例 Python 脚本。
import time

import requests
import hashlib
import sys
import threading
from loguru import logger

logger.remove()  # 删去import logger之后自动产生的handler，不删除的话会出现重复输出的现象
handler_id = logger.add(sys.stderr, level="DEBUG")  # 添加一个可以修改控制的handler


def md5encrypt(cloudtoken, uid, path):
    data = cloudtoken + uid + path
    data = data.encode()
    return hashlib.md5(data).hexdigest()


def search_phone(phone):
    cloudtoken = 'FmDiUHlIhCZpbgFYdpFXKKkwIz3EgUH594pjul0kgLs=@iyzc.cn.rongnav.com;iyzc.cn.rongcfg.com'
    uid = '81678'
    path = '/im/v1/users/query/86/' + phone
    mactoken = md5encrypt(cloudtoken, uid, path)
    headers = {
        'mactoken': mactoken,
        'cloudtoken': cloudtoken,
        'user-agent': 'okhttp/3.11.0',
        'Host': 'www.changtalk.com'
    }
    rsp = requests.get('https://www.changtalk.com' + path, headers=headers, timeout=3)
    if (len(rsp.text) == 0):
        return False
    return True


count = 0

"""注： 可以参考这篇博客https://blog.csdn.net/l835311324/article/details/86608850的示例2，
这个MyThread类继承了threading模块的Thread类，对其下面的run方法进行了重写"""

class MyThread(threading.Thread):
    def __init__(self, threadName):
        print(threadName)
        super(MyThread, self).__init__(name=threadName)

    """一旦这个MyThread类被调用，自动的就会运行底下的run方法中的代码，
    因为这个run方法所属的的MyThread类继承了threading.Thread"""

    def run(self):
        global count
        for i in range(100):
            count += 1
            time.sleep(0.3)
            # print(self.getName(), count)


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':

    import redis

    r = redis.Redis(host='123.207.220.155', port=6379, db=0,password="qq2625112940A12123aFAeADADADG1x22222222")


    with r.pipeline(transaction=False) as p:

        push_list = []
        for count in range(0,99999999):
            phone = "135" + str(count).rjust(8,'0')
            push_list.append(phone)
            if count % 10000 == 0:
                p.lpush("list_china_phone", *push_list)
                push_list = []
                p.execute()
                print('push {}'.format(count))

