# coding=utf-8
"""
test inotify-python
"""
import inotify.adapters
import inotify.constants

def _main():
    i = inotify.adapters.Inotify()
    # 监控指定文件夹
    i.add_watch('./coredump', mask=inotify.constants.IN_CREATE)
    i.add_watch('./symbol', mask=inotify.constants.IN_DELETE)
    # 更新监控文件夹
    with open('/tmp/test_file', 'w'):
        pass
    # 阻塞监控文件夹变动
    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event
        print(f"PATH=[{path}] FILENAME=[{filename}] EVENT_TYPES={type_names} [type]{type(type_names)}")

if __name__ == '__main__':
    _main()
