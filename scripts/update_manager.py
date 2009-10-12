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

    def __init__(self):
        time = datetime.datetime.isoformat(datetime.datetime.now())
        self.working_dir = './%s_pages' % time
        self.error_dir = './%s_errors' % time

    def handle_error(id, rr):
        if not os.path.exists(self.error_dir):
            os.mkdir(error_dir)
        path = os.path.join(self.error_dir, id)
        if os.path.exists(path):
            print 'Already errored: %s' % id
            return False
        output = open(path, 'w')
        cPickle.dump(rr, output, cpickle.HIGHEST_PROTOCOL)
        output.close()
        return True
    
    def save_page(self, id, rr):
        if not os.path.exists(self.work_dir):
            os.mkdir(work_dir)
        print id
        path = os.path.join(self.working_dir, '%s.html' % id)
        output = open(path, 'w')
        output.write(rr.responseBody)
        output.close()

    def process(self, rr, queue):
        id = self.ID_RE.match(rr.requestURL).group(1)
        if rr.responseStatus != 200:
            if self.handle_error(id, rr):
                queue.put(rr.responseURL)
            return
        self.save_page(id, rr)
        

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--count', action='store_true', default=False,
                      help='only display count of items from sitemap')
    options, args = parser.parse_args()

    crawler = NewEggCrawler()
    if options.count:
        print len(crawler.urls)
        sys.exit(0)

    crawler.do_crawl(5)
