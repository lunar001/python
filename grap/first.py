#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import urllib
import re
import tool
import os
import sys

class Spider:
    def __init__(self):
        #页面初始化
        self.siteUrl = 'http://mm.taobao.com/json/request_top_list.htm'
        self.tool = tool.Tool()
    def WriteTofile(self, content):
        self.dbgFile = '/data/python/grap/test'
        fobj = open(self.dbgFile, 'a+')
        fobj.write(content)
    #获取索引页面的内容
    def GetPage(self, pageIndex):
        url = self.siteUrl + "?page=" + str(pageIndex)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read().decode('gbk')
    
    #获取索引界面所有的MM信息， list格式
    def GetContents(self, pageIndex):
        page = self.GetPage(pageIndex)
        pattern = re.compile(' <div class="list-item".*?\n.*?', re.S)
        #<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name.*?>(.*?)</a>
        #.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>''', re.S)
        result = re.search(pattern, page)
        result = re.search('<div class="list-item".*?\n.*?', page)
        print result.group()
        return self.tool.replace(result.group(1))
    #获取MM个人详情页面
    def getDetailPage(self, infoURL):
        reponse = urllib2.urlopen(infoURL)
        return response
    #获取个人文子简介
    def GetBrief(self, page):
        pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--', re.S) 
        result = re.search(pattern, page)
        return self.tool.replace(result.group(1))
    
    #获取所有图片
    def GetAllImg(self, page):
        pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--', re.S)
        #个人信息页面所有代码
        content = re.search(pattern, page)
        #从代码中提取图片
        patternImg = re.compile('<img.*?src="(.*?)"', re.S)
        images = re.findall(pattern, content.group(1))
        return images
    
    #保存多张写真图片
    def SaveImgs(self, images, name):
        number = 1
        print u"发现", name, u"共有", len(images), u"张图片"
        for imageUrl in images:
            splitPath = imageUrl.split('.')
            fTail = splitPath.pop()
            if len(fTail) > 3:
                fTail = "jpg"
            fileName = name + "/" + str(number) + "." + fTail
            self.SaveImg(imageUrl, fileName)
            number += 1
    
    #保存图像
    def SaveIcon(self, iconUrl, name):
        splitPath = iconUrl.split('.')
        fTail = splitPath.pop()
        fileName = name + "/icon." + fTail
        self.SaveImgs(iconUrl, fileName)


    #保存个人简介
    def SaveBrief(self, content, name):
        fileName = name + "/" + name + ".txt"
        f = open(fileName, "w+")
        print u"正在保存个人信息为", fileName
        f.write(content.encode('utf-8'))

    #传入图片地址，文件名，保存单张图片
    def SaveImg(self, imageUrl, fileName):
        u = urllib.urlopne(imageUrl)
        data = u.read()
        f = open(fileName, 'wb')
        f.write(data)
        print u"正在保存一张图片为", fileName
        f.close()
 
    #创建新目录
    def mkdir(self, path):
        path = path.strip()
        #判断路径是否存在
        #存在        True
        #不存在      False
        isExists = os.path.exists(path)
        #判断结果
        if not isExists:
            #如果不存在就创建新目录
            print u"新建了名字叫做", path, u"的文件夹"
            os.makedirs(path)
            return True
        else:
            print u"名为", path, u"的文件夹已经创建成功"
            return False

    #将一页淘宝MM的信息保存起来
    def SavePageInfo(self, pageIndex):
        #获取第一页淘宝MM列表
        contents = self.GetContents(pageIndex)
        for item in contents:
            #item[0]个人详情URl, item[1]头像url, item[2]姓名, item[3]年龄,item[4]居住地
            print u"发现一名模特，名字叫", item[2], u"芳龄", item[3], u"她在", item[4]
            print u"正在保存", item[2], u"的信息"
            print u"又意外发现她的个人地址是", item[0]
            #个人详情页面url
            detailURL = item[0]
            detailPage = self.getDetailPage(detailURL)
            brief = self.GetBrief(detailPage)
            images = self.GetAllImg(detailPage)
            self.mkdir(item[2])
            self.SaveBrief(brief, item[2])
            self.SaveIcon(images, item[2])
            self.SaveImgs(images, item[2])
    #传入起止页码，获取MM图片
    def SavePagesInfo(self, start, end):
        for i in range(start, end + 1):
            print u"正在偷偷寻找第", i, u"个地方，看看MM们在不在"
            self.SavePageInfo(i)

spider = Spider()
spider.SavePagesInfo(2, 5)

        


















