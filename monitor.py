# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import config

def read_file(seek, path):
    realpath = os.path.realpath(path)
    f = open(realpath, 'r', encoding='gbk')

    size = os.path.getsize(path)
    if (seek > size):
        logging.error("invalid seek:%d > size:%d", seek, size)
        seek = 0
    f.seek(seek)

    content = ""
    for line in f.readlines():
        content = content + line
    next_seek = f.tell()
    f.close()
    return next_seek, content

class MyLoggingEventHandler(FileSystemEventHandler):
    """Logs all the events captured."""
    def __init__(self):
        self._time0 = time.time()
        self._seek = 0

    def on_created(self, event):
        if event.is_directory:
          logging.info("created directory: %s", event.src_path)
          return
        self._seek = 0
        self._seek, content = read_file(self._seek, os.path.realpath(event.src_path))

        #send_hint(content)
        config.send_content = content
        logging.info("created file: %s, clear seek", event.src_path)

    def on_modified(self, event):
        # 保证1秒只触发一次
        time1 = time.time()
        if (time1 - self._time0) < 1:
            return
        self._time0 = time1

        if event.is_directory:
          logging.info("modify directory: %s", event.src_path)
          return

        self._seek, content = read_file(self._seek, os.path.realpath(event.src_path))

        #send_hint(content)
        config.send_content = content
        logging.info("modify file:%s, seek:%d", event.src_path, self._seek)

def monitor(path):
    logging.info("monitor path: %s", path)
    event_handler = MyLoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    return observer

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    observer = monitor(path)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()