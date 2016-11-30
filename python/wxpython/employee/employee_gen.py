#!/usr/bin/python
# coding:utf-8

import os
import sys
import random

def employee_gen(file):
    with open(file, 'w') as fp:
        for i in range(550):
            fp.write('%03d\t%d.jpg\n' % (i + 1, random.randint(1, 9)))

if __name__ == '__main__':
    employee_gen('employee.txt')