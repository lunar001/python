#!/usr/bin/python

import downpage
import os
import sys
import re
import lxml.html
import time

FIELDS = ('area', 'population', 'iso', 'country', 'capital', 'continent', 
    'tld', 'currency_code', 'currency_name', 'phone', 'postal_code_format',
    'postal_code_regex', 'languages', 'neighbours')
def re_scraper(html):
    results = {}
    for field in FIELDS:
        results[field] = re.search('<tr id="places_%s__row">.*?<td class="w2p_fw">(.*?)</td>' % field, html).groups()[0]
    return results
 
def lxml_scraper(html):
    tree = lxml.html.fromstring(html)
    results = {}
    for field in FIELDS:
        results[field] = tree.cssselect('table > tr#places_%s__row"> td.w2p_fw' % field)[0].text_content()
    return results

def get_time():
    NUM_ITERATIONS = 1000
    html = downpage.download('http://example.webscraping.com/places/view/United-Kingdom-239')
    for name, scraper in [('Regular expressions', re_scraper),
        ('Lxml', lxml_scraper)]:
        start = time.time()
        for i in range(NUM_ITERATIONS):
            if scraper == re_scraper:
                re.purge()
            results = scraper(html)
            assert(results['area'] == '244,820 square kilometres')
        end = time.time()
        print '%s: %.2f seconds' % (name, end - start)





if __name__ == '__main__':
    get_time()


