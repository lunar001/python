#!/usr/bin/python

import urlparse
import datetime
import time

class Throttle:
    def __init__(self, delay):
        self.delay = delay
        self.domains = {}
    def wait(self, url):
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)
        
        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now() - 
                last_accessed).seconds
            if sleep_secs > 0:
                #domain has been accessed recently
                #so need to sleep
                time.sleep(sleep_secs)
            #update the last accessed time
            self.domains[domain] = datetime.datetime.now()
