#!/usr/bin/python

import os
import sys
import urllib2
import urlparse
import re
import itertools
import Throttle

def download(url, user_agent = 'wswp', proxy = None, num_retries = 2):
    print 'Downloading:', url
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers = headers)
    opener = urllib2.build_opener()
    if proxy:
        proxy_params = {urlparse.urlparse(url).schemme:proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        html = opener.open(request).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return download(url, num_retries - 1)
    return html
def crawl_sitemap(url):
    # download the sitemap file
    sitemap = download(url)
    # extract the sitemap links
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    #down each link:
    for link in links:
        html = download(link)
        print html
def crawl_idtree(url):
    # maximum number of consecutive download errors allowed
    max_errors = 5
    #current number of consecutive download errors
    num_errors = 0
    for page in itertools.count(1):
        url = 'http://example.webscraping.com/view/-%d' % page
        html = download(url)
        if html is None:
            num_errors += 1
        if num_errors == max_errors:
            break
        else:
            print 'success'
            num_errors = 0
            
            
def link_crawler(seed_url, link_regex, user_agent = 'wswp', max_depth = 1):
    crawl_queue= [seed_url]
    seen ={}
    seen[seed_url] = 0 
    throttle = Throttle.Throttle(10)
    while crawl_queue:
        url = crawl_queue.pop()
        throttle.wait(url)
        html = download(url)
        depth = seen[url]
        print depth
        if depth != max_depth:
            print get_links(html)
            for link in get_links(html):
                if re.match(link_regex, link):
                    link = urlparse.urljoin(seed_url, link)
                if link not in seen:
                    seen[link] = depth + 1
                    crawl_queue.append(link)

def get_links(html):
    webpage_regex = re.compile('<a href="(.*?)"', re.IGNORECASE)
    return webpage_regex.findall(html)

if __name__ == '__main__':
    print sys.argv
    link_crawler(sys.argv[1], sys.argv[2])
