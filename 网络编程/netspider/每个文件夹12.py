import os, shutil

path = 'C:/Files/watchjavonline'

a = os.listdir(path)
for each in a:  # 类
    files = os.listdir('%s/%s' % (path, each))
    count = 0
    a = 1
    for i in files:
        if os.path.isdir('%s/%s/%s' % (path, each, i)):
            continue
        if i.endswith('.txt'):
            continue
        try:
            os.mkdir('%s/%s/%s' % (path, each, str(a)))
        except FileExistsError:
            pass
        shutil.move('%s/%s/%s' % (path, each, i), '%s/%s/%s/%s' % (path, each, str(a), i))
        count += 1

        if count == 100:
            count = 0
            a += 1
