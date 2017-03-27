#!/usr/bin/python

import os
import sys

class Iterable: 
    def __iter__(self):
        return self
    def __init__(self):
        self.start = -1
    def __next__(self):
        self.start += 2
        if self.start > 10:
            raise StopIteration
        return self.start
if __name__ == '__main__':

    I = Iterable()
    print next(I)
    I = iter(I)
    for i in I:
        print (i)

