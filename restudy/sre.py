#!/usr/bin/python

import os
import sys
import re

key="3.com,1040715974@qq.com and bjltaoee@cn.tst.com and M201372659@hust.edu.com and nobody@xxx.com"
p1 = '\w+@(\w+\.)?\w+\.com'
pat=re.compile(p1)
print pat.search(key).group()
print pat.findall(key)
print re.findall(p1, key)
