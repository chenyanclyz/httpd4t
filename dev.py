#coding:utf-8
'''python2 code
author's email: chenyan@feling.net

运行dev.py,会调用相同路径下的httd4t.py, 在8888端口监听，
如果相同路径下有py文件发生改变，就重启httpd4t.py

需要第三方模块
easy_install watchdog
'''

import os, sys, time, subprocess

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import logging
logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(levelname)s %(message)s',
                datefmt='%M:%S',
                )

class Hander(FileSystemEventHandler):

    def restart(self):
        global process
        process.kill()
        process.wait()
        process = subprocess.Popen(['python','httpd4t.py','8888'], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

    def on_any_event(self, event):
        if event.src_path.endswith('.py'):
            logging.info(event.src_path+' has been modified, restarting...')
            self.restart()

def start():
    observer = Observer()
    observer.schedule(Hander(), '.', recursive=True)
    observer.start()
    logging.info('start watching...')
    global process
    process = subprocess.Popen(['python','httpd4t.py','8888'], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    start()
