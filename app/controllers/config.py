#coding: utf-8

# class Config():
import os

config_filename = 'config.txt'

def getConfigResult():
    if os.path.exists(config_filename) == False:
        o = open(config_filename, "w")
        o.write('0')
        o.close()
    f = open(config_filename, "r")
    data = f.read()
    f.close()
    print (data)
    return int(data)

def setConfig(config_num):
    o = open(config_filename, "w")
    o.write(str(config_num))
    o.close()