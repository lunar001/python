#!/usr/bin/python
import os
import sys
import re

host='you destination ip'
remoteDir=' your remote dir name'
localDir = 'your local dir name'
orignalDir='your original dir name'

def FindNameList(pathName):
    if pathName == None:
        return None
    else:
        return os.listdir(pathName)

def DownLoadFile(remotePathFile, localPathFile):
    cmd = 'scp ' + remotePathFile + ' ' + localPathFile
    #print cmd
    ret = 0
    ret = os.system(cmd)
    if ret != 0:
        print cmd , "excute error"
        return ret
    return ret

def DownLoad(userName, host, remoteDir, orignalDir, localDir):
    fileList = FindNameList(orignalDir)
    for fileName in fileList:
        pattern = '\w+\.h'
        if re.match(pattern, fileName):
            remotePathFile = userName + '@' + host + ':' + remoteDir + fileName
            localPathFile = localDir + fileName
            ret = DownLoadFile(remotePathFile, localPathFile)
            if ret == 0:
                print 'Download ' + fileName + 'successfully'
            else:
                return -1
        else:
            os.mkdir(localDir + fileName + '/')
            DownLoad(userName, host, remoteDir + fileName + '/', orignalDir + fileName + '/', localDir + fileName + '/')
    return 0


if __name__ == '__main__':
    userName = sys.argv[1]
    print userName
    ret = DownLoad(userName, host, remoteDir, orignalDir, localDir)
    if ret != 0:
        print "Download failed"


