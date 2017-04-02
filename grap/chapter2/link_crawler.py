#!/usr/bin/pytnon

import re
import urlparse
import urllib2
import time
import datetime
import robotparser
from downloader import Downloader

class Crawler:
    def __init__(self, seed_url, link_regex = None, delay = 5, max_depth = 1, max_urls = -1,
            user_agent = 'wswp', proxies = None, num_retries = 1, scrape_callback = None, cache = None):
        self.seed_url_ = seed_url
        self.link_regex_ = link_regex
        self.delay_ = delay
        self.max_depth_ = max_depth
        self.max_urls_ = -1
        self.user_agent_ = user_agent
        self.proxies_ = proxies
        self.num_retries_ = num_retries
        self.scrape_callback_ = scrape_callback
        self.cache_ = cache

    def get_robots(self, url):
        """ 
        Initialize robots parser for this domain
        """
        rp = robotparser.RobotFileParser()
        rp.set_url(urlparse.urljoin(url, '/robots.txt'))
        rp.read()
        return rp

    def link_crawler(self):
        crawl_queue = [self.seed_url_]
        # the URL's that have been seen and at what depth
        seen = {self.seed_url_: 0}
        # track how may URL's have been download
        num_urls = 0
        rp = self.get_robots(self.seed_url_)
        D = Downloader(delay = self.delay_, user_agent = self.user_agent_, proxies = self.proxies_, 
            num_retries = self.num_retries_, cache = self.cache_)
        while crawl_queue:
            url = crawl_queue.pop()
            depth = seen[url]
            #check url passes robot.txt restrictions
            if rp.can_fetch(self.user_agent_, url):
                html = D(url) #Downloader is a call object
                links = []
                if self.scrape_callback_:
                    links.extend(self.scrape_callback_(url, html) or []) 

                if depth != self.max_depth_:
                # can still crawl further
                    if self.link_regex_:
                        links.extend(link for link in self.get_links(html) if re.match(self.link_regex_, link))
                    for link in links:
                        link = self.normalize(self.seed_url_, link)
                        if link not in seen:
                            seen[link] = depth + 1
                        if self.same_domain(self.seed_url_, link):
                            crawl_queue.append(link)
                num_urls += 1
                if num_urls == self.max_urls_:
                    break
            else:
                print 'Blocked by robots.txt:', url


    def normalize(self, url, link):
        """
        Normalize this URL by removing hash and adding domain
        """
        link_, _ = urlparse.urldefrag(link) # remove hash to avoid duplicates
        return urlparse.urljoin(url, link)


    def same_domain(self, url1, url2):
        """
        Return True if both URL's belong to same domain
        """
        return urlparse.urlparse(url1).netloc == urlparse.urlparse(url2).netloc

    def get_links(self, html):
        """
        Return a list of links from html
        """
        webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
        return webpage_regex.findall(html)


