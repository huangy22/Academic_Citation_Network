#!/usr/bin/python
import pprint
import gzip,os,sys,time
from numpy import *

def SaveDict(filename, mode, root):
    set_printoptions(threshold=inf)
    if filename[-4:]!=".txt":
        filename+=".txt"
    with open(filename, mode) as f:
        f.write(pprint.pformat(root, depth=100))

def LoadDict(filename):
    if filename[-4:]!=".txt":
        filename+=".txt"
    with open(filename, "r") as f:
        return eval(f.read())
