#!/usr/bin/python

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
    #获取索引页面的内容
    def GetPage(self, pageIndex):
        url = self.siteUrl + "?page=" + str(pageIndex)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read().decode('gbk')
    
    #获取索引界面所有的MM信息， list格式
    def getContents(self, pageIndex):
        page = self.getPage(pageIndex)
        pattern = re.compile('<div class="list-item".*?pic-word.*?
        <a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name.*?>(.*?)</a>
        .*?<strong>(.*?)</strong>.*?<span>(.*?)</span>', re.S)
        result = re.search(pattern, page)
        return self.tool.replace(result.group(1))
    
    #获取个人文子简介
    def getBrief(self, page):
        pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--', re.S) 
        result = re.search(pattern, page)
        return self.tool.replace(result.group(1))
    
    #获取所有图片
    def getAllImg(self, page):
        pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--', re.S)
        #个人信息页面所有代码
        content = re.search(pattern, page)
        #从代码中提取图片
        patternImg = re.compile('<img.*?src="(.*?)"', re.S)
        images = re.findall(pattern, content.group(1))
        return images
    
    #保存多张写真图片
    def saveImgs(self, images, name):
        number = 1
        print u"发现", name, u"共有", len(images), u"张图片"
        for imageUrl in images:
            splitPath = imageUrl.split('.')
            fTail = splitPath.pop()
            if len(fTail) > 3:
                fTail = "jpg"
            fileName = name + "/" + str(number) + "." + fTail
            self.saveImg(imageUrl, fileName)
            number += 1
    
    #保存图像
        def SaveIcon(self.iconUrl, name):
            splitPath = iconUrl.split('.')
            fTail = splitPath.pop()
            fileName = name + "/icon." + fTail
            self.saveImgs(iconUrl, fileName)



