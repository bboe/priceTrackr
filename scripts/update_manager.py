#!/usr/bin/env python
import crawle, gzip, re
from StringIO import StringIO

def get_product_ids(sitemap):
    url_re = re.compile(''.join(['http://www.newegg.com/Product/Product',
                                 '.aspx\?Item=([A-Z0-9]+)']))
    return url_re.findall(gzip.GzipFile(fileobj=StringIO(sitemap)).read())

if __name__ == '__main__':
    sm = ['http://www.newegg.com//Sitemap/USA/newegg_sitemap_product01.xml.gz',
          'http://www.newegg.com//Sitemap/USA/newegg_sitemap_product02.xml.gz']
    urls = []
    for sitemap in sm:
        cc = crawle.HTTPConnectionControl(crawle.Handler())
        rr = crawle.RequestResponse(sitemap, maxRedirects=None)
        cc.request(rr)
        if rr.responseStatus != 200:
            print 'Error'
            break
        urls.extend(get_product_ids(rr.responseBody))
    print len(urls)

    # FEED URLS TO QUEUE
