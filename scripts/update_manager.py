#!/usr/bin/env python
import crawle, cPickle, datetime, gzip, os, re, sys
from optparse import OptionParser
from StringIO import StringIO

class NewEggCrawler(object):
    URL_RE = re.compile(''.join(['http://www.newegg.com/Product/',
                                 'Product.aspx\?Item=[A-Z0-9]+']))
    SITEMAP_PREFIX = 'http://www.newegg.com//Sitemap/USA/'
    SITEMAPS = ['newegg_sitemap_product01.xml.gz',
                'newegg_sitemap_product02.xml.gz']

    def __init__(self):
        self.urls = []
        self.get_product_ids()
        self.handler = NewEggCrawlHandler()
        self.queue = crawle.URLQueue()

    def get_product_ids(self):
        for sitemap in [''.join([self.SITEMAP_PREFIX, x]) for x
                        in self.SITEMAPS]:
            cc = crawle.HTTPConnectionControl(crawle.Handler())
            rr = crawle.RequestResponse(sitemap, redirects=None)
            cc.request(rr)
            if rr.responseStatus != 200:
                print 'Error'
                break
            body = gzip.GzipFile(fileobj=StringIO(rr.responseBody)).read()
            self.urls.extend(self.URL_RE.findall(body))

    def do_crawl(self, threads):
        for url in self.urls:
            self.queue.put(url)
        controller = crawle.Controller(handler=self.handler, queue=self.queue,
                                       numThreads=threads)
        controller.start()
        try:
            controller.join()
        except KeyboardInterrupt:
            controller.stop()

class NewEggCrawlHandler(crawle.Handler):
    ID_RE = re.compile(''.join(['http://www.newegg.com/Product/',
                                'Product.aspx\?Item=([A-Z0-9]+)']))
    MAP_URL = 'http://www.newegg.com/Product/MappingPrice.aspx?Item='
    CART_URL = 'http://secure.newegg.com/Shopping/ShoppingCart.aspx'

    ZIP_COOKIE = ''.join(['NV%5FORDERCOOKIE=#4%7b%22Sites%22%3a%7b%22USA%22',
                          '%3a%7b%22Values%22%3a%7b',
                          '%22NVS%255FCUSTOMER%255FSHIPPING%255FMETHOD1%22',
                          '%3a%22038%22%2c',
                          '%22NVS%255FCUSTOMER%255FZIP%255FCODE%22%3a',
                          '%2293117%22%7d%7d%7d%7d'])

    def __init__(self):
        time = datetime.datetime.isoformat(datetime.datetime.now())
        self.working_dir = './%s_pages' % time
        self.error_dir = './%s_errors' % time

    def handle_error(self, id, rr):
        if not os.path.exists(self.error_dir):
            os.mkdir(self.error_dir)
        path = os.path.join(self.error_dir, id)
        if os.path.exists(path):
            print 'Already errored: %s' % id
            return False
        output = open(path, 'w')
        cPickle.dump(rr, output, cPickle.HIGHEST_PROTOCOL)
        output.close()
        return True
    
    def save_page(self, id, rr):
        if not os.path.exists(self.working_dir):
            os.mkdir(self.working_dir)
        path = os.path.join(self.working_dir, '%s.html' % id)
        output = open(path, 'w')
        output.write(rr.responseBody)
        output.close()

    def mapping_preProcess(self, rr):
        match = self.ID_RE.match(rr.requestURL)
        if match:
            id = match.group(1)
            rr.responseURL = ''.join([self.MAP_URL, id])
        else:
            print rr.requestURL
            rr.responseURL = None

    def cart_preProcess(self, rr):
        match = self.ID_RE.match(rr.requestURL)
        if match:
            id = match.group(1)
            rr.responseURL = self.CART_URL
            c_id = ''.join(['NV%5FNEWEGGCOOKIE=#4{"Sites":{"USA":{"Values":{"',
                            self.transform_id(id), '":"1"}}}}'])
            rr.requestHeaders = {'Cookie':';'.join([self.ZIP_COOKIE, c_id])}
        else:
            print rr.requestURL
            rr.responseURL = None

    @staticmethod
    def transform_id(id):
        return '%s-%s-%s' % (id[7:9], id[9:12], id[12:])

    def process(self, rr, queue):
        match = self.ID_RE.match(rr.requestURL)
        if match:
            id = match.group(1)
        else:
            print rr.requestURL
            return
        if rr.responseStatus != 200:
            if self.handle_error(id, rr):
                queue.put(rr.responseURL)
            return
        self.save_page(id, rr)
        

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--count', action='store_true', default=False,
                      help='only display count of items from sitemap')
    parser.add_option('--mapping', action='store_true', default=False,
                      help='crawl mapping pages')
    parser.add_option('--cart', action='store_true', default=False,
                      help='crawl cart pages')
    options, args = parser.parse_args()
      
    crawler = NewEggCrawler()
    if options.count:
        print len(crawler.urls)
        sys.exit(0)
    if options.mapping:
        print 'Crawling mapping pages'
        crawler.handler.preProcess = crawler.handler.mapping_preProcess
    elif options.cart:
        print 'Crawling cart pages'
        crawler.handler.preProcess = crawler.handler.cart_preProcess
    else:
        print 'Crawling item pages'

    crawler.do_crawl(10)
