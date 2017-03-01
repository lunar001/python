#!/usr/bin/python

import os
import sys
import requests

class downloader:
    def __init__(self):
        self.url = 'http://51reboot.com/src/blogimg/pc.jpg'
        self.num = 8
        self.name ='pc.jpg'
        r = requests.head(self.url)
        self.total = int(r.headers['Content-length'])
        print type('totalis %s' % (self.total))
    def get_range(self):
        ranges = []
        offset = int(self.total / self.num)
        for i in range(self.num):
            if i == self.num - 1:
                ranges.append((i * offset, ''))
            else:
                ranges.append((i * offset, (i + 1) * offset))
        return ranges
    def run(self):
        f = open(self.name, 'w')
        for ran in self.get_range():
            r = requests.get(self.url, headers = {'Range':'Bytes=%s-%s' % ran, 'Accept-Enconding':'*'})
            f.seek(ran[0])
            f.write(r.content)
        f.close()

if __name__ == '__main__':
    down = downloader()
    down.run()



