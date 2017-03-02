mport sys
import os

pathA = '/Users/Desktop/saber/s22/'
pathB = '/Users/Desktop/saber/y22/'
resultFile = '/Users/Desktop/saber/result'
SuccessResult = '*                     Same                     *'
FailedResult =  '*                  Different                   *'
def FindFilenames(pathName):
    if pathName == None:
        return None
    else:
        return os.listdir(pathName)

def FormatString(strContent, lelftPad = 0):
        if strContent == '\n':
                result = '*' + ' ' * 49 + '*' + '\n'
                return result
        length = len(strContent)
        if length > 50:
            if leftPad == 0:
                    return strContent + '\n'
            else:
                firstPart = '*' + ' ' * leftPad
                return firstPart + strContent + '\n'
        else:
            if leftPad == 0:
                firstPart == (50 - length)/2 - 1
                secondPart = (50 -length - firstPart - 1
            else:
                firstPart = leftPad
                secondPart = 50 - length - firstPart -1
            result = '*' + ' ' * firstPart + strContent + ' ' * secondPart
        return result

def OutPutResult(fileName, Result):
    fobj = open(resultFile, 'a')
    fobj.write('\n')
    fobj.write('*' * 50)
    fobj.write('\n')
    firstPart = ' ' * ((50 - len(fileName))/2 - 1)
    secondPart = ' ' * ((50 - len(fileName))/2 - 1)
    fobj.write( '*' + firstPart + fileName +  secondPart + '*')
    fobj.write('\n')
    if Result:
        padPart = ' ' * ((50 - len('Same'))/2 -1)
        fobj.write('*' + padPart + 'Same' + padPart + '*' + '\n')
    else:
        padPart = ' ' * ((50 - len('Different'))/2 -1)
        fobj.write('*' + padPart + 'Different' + padPart + '*' + '\n')
        filePath1 = pathA + fileName
        filePath2 = pathB + fileName
        fobj1 = open(filePath1, 'r')
        fobj2 = open(filePath2, 'r')
        while True:
            line1 = fobj1.readline()
            line2 = fobj2.readline()
            if line1 == '' and line2 != '':
                fobj.write('Y is more than S\n')
                while(line2):
                    fobj.write(line2)
                    line2 = fobj2.readline()
            if line1 != '' and line2 == '':
                fobj.write('S is more than Y\n')
                while(line1):
                    fobj.write(line1)
                    line1 = fobj1.readline()
            if line1 == '' and line2 == '':
                break
            else:
                ret = CompareTwoLine(line1, line2)
                if ret == False:
                    line1 = line1.strip('\n')
                    line1 = line1.rstrip()
                    line2 = line2.strip('\n')
                    line2 = line2.rstrip()
                    fobj.write(line1)
                    fobj.write('\n')
                    fobj.write(line2)
                    fobj.write('\n\n\n')

    fobj.write('*' * 50)
        


def CompareTwoLine(line1, line2):
    ' compare two line, rule can be varied'
    list1 = line1.split(' ')
    list2 = line2.split(' ')
    while ('' in list1):
        list1.remove('')
    while ('\r\n' in list1):
        list1.remove('\r\n')
    
    while ('' in list2):
        list2.remove('')
    while ('\r\n' in list2):
        list2.remove('\r\n')
    if list1[0] == list2[0] and list1[2] == list2[2]:
        return True
    else:
        return False
    

def CompareTwoFile(fileName1, fileName2):
    ''' CompareTwoFile return True is fileName1 and fileName2
        is the same, Return False while not same'''
    same = True
    file1 = open(fileName1, "r")
    file2 = open(fileName2, "r")
    while True:
        line1 = file1.readline()
        line2 = file2.readline()
        if line1 == "" and line2 != "" :
            same = False
            break
        if line1 != "" and line2 == "":
            same = False
            break
        if line1 == "" and line2 == "":
            break;
        if CompareTwoLine(line1, line2): 
            continue
        else:
            same = False
            break
    return same

def Compute(pathName1, pathName2):
    ' compare fileContent'
    fileNameList1 = FindFilenames(pathName1)
    fileNameList2 = FindFilenames(pathName2)
    for fileName in fileNameList1:
        fileName1 = pathA  + (fileName)
        if fileName in fileNameList2:
            fileName2 = pathB + fileName
            ret = CompareTwoFile(fileName1, fileName2)
            OutPutResult(fileName, ret)
    return 

if __name__ == "__main__":
    Compute(pathA, pathB)

