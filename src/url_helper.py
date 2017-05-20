
from urlparse import urlparse, parse_qs
import urllib2

import random
from bs4 import BeautifulSoup
def parse_url_qs(url):
    return parse_qs(urlparse(url).query)
def url_without_query_string(url):
    """ remove query string in url"""
    o = urlparse(url)
    return o.scheme + "://" + o.netloc + o.path

def random_headers(headers_list):
    headers = {'User-Agent': random.choice(headers_list)}
    return headers
def get_headers_list():
    # fake useragent
    from fake_useragent import UserAgent
    ua = UserAgent()
    headers_list = [ua.chrome, ua.google, ua['google chrome'], ua.firefox, ua.ff,'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0']
    return headers_list


def req_html(proj_id, url, headers_list, timeout=10):
    """request for html by url with randome headers
    return:
        if request success: html and error=None 
        if request encounter error: html=None and error
    """
    headers = random_headers(headers_list)
    req = urllib2.Request(url, headers=headers)
    html = None
    error = None
    # catch url request error
    try:
        response = urllib2.urlopen(req,timeout=10)
        html = response.read()
    except urllib2.HTTPError, e:
        error = 'HTTPError = ' + str(e.code)
    except urllib2.URLError, e:
        error = 'URLError = ' + str(e.reason)
    except Exception as e:
        error = e
        
    if error is not None:
        error = (proj_id, url, error)
    return html, error