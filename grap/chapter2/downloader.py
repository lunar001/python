#!/usr/bin/python

import urlparse
import urllib2
import random
import time
from datetime import datetime, timedelta
import socket
import throttle
DEFAULT_AGENT = 'wswp'
DEFAULT_DELAY = 5
DEFAULT_RETRIES = 1
DEFAULT_TIMEOUT = 60

class Downloader:
    def __init__(self, delay = DEFAULT_DELAY, user_agent = DEFAULT_AGENT,
        num_retries = DEFAULT_RETRIES, timeout = DEFAULT_TIMEOUT, opener = None, cache = None):
        socket.setdefaulttimeout(timeout)
        self.throttle =throttle.Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.opener = opener
        self.cache = cache
    
    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                # url is no available in cache
                pass
            else:
                if self.num_retries > 0 and 500 <= result['code'] < 600:
                    result = None
        if result is None:
            # result was not loaded from cache so still to download
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {'User-agent': self.user_agent}
            result = self.download(url, headers, proxy = proxy, num_retries = self.num_retries)
            if self.cache:
                #save result to cache
                self.cache[url] = result
        return result['html']

    def download(self, url, headers, proxy, num_retries, data = None):
        print 'Downloading:', url
        request = urllib2.Request(url, data, headers or {})
        opener = self.opener or urllib2.build_opener()
        if proxy:
            proxy_params = {urlparse.urlparse(url).scheme: proxy}
            opener.add_handler(urllib2.ProxyHandler(proxy_params))
        try:
            response = opener.open(request)
            html = response.read()
            code = response.code
        except:
            print 'Download error:', str(e)
            html = ''
            if hasattr(e, 'code'):
                code = e.code
                if num_retries > 0 and 500 <= code <600:
                    # what's the meaning of self._get
                    return self._get(url, headers, proxy, num_retries - 1, data)
            else:
                code = None
        return {'html': html, 'code': code}





