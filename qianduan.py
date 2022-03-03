import eel
import kbqa_test
import os
import bottle_websocket
# 定义html文件所在文件夹名称
eel.init('web')
@eel.expose # 使用装饰器,类似flask里面对路由的定义
def answer(key):
    mykbqa = kbqa_test.KBQA(key)
    content = mykbqa.main()
    print(key)
    print(content)
    return content
eel.start('index.html', port=0, size=(600,300))
os.system('pause')