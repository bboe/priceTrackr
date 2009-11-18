#!/usr/bin/env python
import crawle, cPickle, gzip, os, re, sys, tarfile, threading, time
from optparse import OptionParser
from StringIO import StringIO
from page_parser import PageParser

class NewEggCrawler(object):
    SITEMAP_URL_PREFIX = 'http://www.newegg.com/Sitemap/USA/'
    SITEMAPS = ['newegg_sitemap_product01.xml.gz',
                'newegg_sitemap_product02.xml.gz']
    ITEM_ID_RE = re.compile(''.join(['http://www.newegg.com/Product/',
                                     'Product.aspx\?Item=([A-Z0-9]+)']))

    def __init__(self, output_tar, error_tar, save):
        self.item_ids = []
        self.get_product_ids()
        self.handler = NewEggCrawlHandler(output_tar, error_tar, save)
        self.queue = crawle.URLQueue()

    def get_product_ids(self):
        for sitemap in [''.join([self.SITEMAP_URL_PREFIX, x]) for x
                        in self.SITEMAPS]:
            cc = crawle.HTTPConnectionControl(crawle.Handler())
            rr = crawle.RequestResponse(sitemap, redirects=None)
            cc.request(rr)
            if rr.responseStatus != 200:
                print 'Error'
                break
            body = gzip.GzipFile(fileobj=StringIO(rr.responseBody)).read()
            self.item_ids.extend(self.ITEM_ID_RE.findall(body))

    def do_crawl(self, limit=None, start=0, threads=1):
        if limit:
            self.item_ids = self.item_ids[:limit + start]
        for item_id in self.item_ids[start:]:
            self.queue.put((item_id, 0))
        controller = crawle.Controller(handler=self.handler, queue=self.queue,
                                       numThreads=threads)
        controller.start()
        try:
            controller.join()
        except KeyboardInterrupt:
            controller.stop()

class NewEggCrawlHandler(crawle.Handler):
    ITEM_URL_PREFIX = 'http://www.newegg.com/Product/Product.aspx\?Item='
    CART_URL = 'http://secure.newegg.com/Shopping/ShoppingCart.aspx'
    MAP_URL_PREFIX = 'http://www.newegg.com/Product/MappingPrice.aspx?Item='
    ZIP_COOKIE = ''.join(['NV%5FORDERCOOKIE=#4%7b%22Sites%22%3a%7b%22USA%22',
                          '%3a%7b%22Values%22%3a%7b',
                          '%22NVS%255FCUSTOMER%255FSHIPPING%255FMETHOD1%22',
                          '%3a%22038%22%2c',
                          '%22NVS%255FCUSTOMER%255FZIP%255FCODE%22%3a',
                          '%2293117%22%7d%7d%7d%7d'])

    @staticmethod
    def transform_id(id):
        return '%s-%s-%s' % (id[7:9], id[9:12], id[12:])
    
    def __init__(self, output_tar, error_tar, save):
        self.save = save
        self.output_tar = output_tar
        self.error_tar = error_tar
        self.parser = PageParser()
        self.lock = threading.Lock()
        self.items = {}

    def handle_error(self, rr):
        if not self.save: return
        temp_file = StringIO()
        cPickle.dump(rr, temp_file, cPickle.HIGHEST_PROTOCOL)
        temp_file.seek(0)
        info = tarfile.TarInfo('error/%s-%s' % rr.requestURL)
        info.size = len(temp_file.buf)
        info.mtime = time.time()
        self.lock.acquire()
        self.error_tar.members = []
        self.error_tar.addfile(info, temp_file)
        self.lock.release()
        temp_file.close()
    
    def save_page(self, rr):
        if not self.save: return
        temp_file = StringIO()
        cPickle.dump(rr, temp_file, cPickle.HIGHEST_PROTOCOL)
        temp_file.seek(0)
        info = tarfile.TarInfo('pages/%s-%s' % rr.requestURL)
        info.size = len(temp_file.buf)
        info.mtime = time.time()
        self.lock.acquire()
        self.output_tar.members = []
        self.output_tar.addfile(info, temp_file)
        self.lock.release()
        temp_file.close()

    def preProcess(self, rr):
        if not isinstance(rr.requestURL, tuple):
            print 'Something slid by: %s' % rr.responseURL
            raise
        id, type = rr.requestURL
        if type == 0: # ITEM
            rr.responseURL = ''.join([self.ITEM_URL_PREFIX, id])
        elif type == 1: # CART
            rr.responseURL = self.CART_URL
            c_id = ''.join(['NV%5FNEWEGGCOOKIE=#4{"Sites":{"USA":{"Values":{"',
                            self.transform_id(id), '":"1"}}}}'])
            rr.requestHeaders = {'Cookie':';'.join([self.ZIP_COOKIE, c_id])}
        elif type == 2: # MAPPING
            rr.responseURL = ''.join([self.MAP_URL_PREFIX, id])
        else:
            raise 'Unknown Type'

    def process(self, rr, queue):
        if rr.responseStatus == None:
            try:
                if rr.errorMsg == 'Socket Error':
                    queue.put(rr.requestURL)
                elif rr.errorMsg == 'Redirect count exceeded':
                    pass
                else:
                    self.handle_error(rr)
            except:
                self.handle_error(rr)
            return
        elif rr.responseStatus != 200:
            self.handle_error(rr)
            return
        id, type = rr.requestURL
        if type == 0: # ITEM
            info = self.parser.parse_item_page_info(id, rr.responseBody)
            if not info:
                return
            if 'deactivated' not in info and 'price' not in info:
                queue.put((id, 1))
        elif type == 1: # CART
            info = self.parser.parse_cart_page(id, rr.responseBody)
            if not info:
                queue.put((id, 2))
                return
        elif type == 2: # MAPPING
            info = self.parser.parse_mapping_page(id, rr.responseBody)
        else:
            raise 'Unknown Type'
        self.lock.acquire()
        if type == 0:
            self.items[id] = info
        else:
            self.items[id].update(info)
        self.lock.release()
        self.save_page(rr)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--count', action='store_true', default=False,
                      help='only display count of items from sitemap')
    parser.add_option('--no-save', action='store_true', default=False,
                      dest='no_save',
                      help='don\'t save items and output to screen')
    parser.add_option('--threads', default=1, type="int",
                      help='number of crawl threads (default: %default)')
    parser.add_option('--limit', default=None, type="int",
                      help='limit of items to crawl (default: %default)')
    parser.add_option('--start', default=0, type="int",
                      help='item pos to start crawl (default: %default)')
    parser.add_option('--item', action='append',
                     help='single item to crawl - can list multiple times')
    options, args = parser.parse_args()

    output_prefix = time.strftime('%Y-%m-%d_%H.%M.%S', time.localtime())
    if options.no_save:
        output_tar = error_tar = None
    else:
        output_tar = tarfile.open('%s.tar.gz' % output_prefix, 'w:gz')
        error_tar = tarfile.open('%s_error.tar.gz' % output_prefix, 'w:gz')
      
    crawler = NewEggCrawler(output_tar, error_tar, not options.no_save)
    if options.item != None:
        crawler.item_ids = options.item

    print 'Found %d items' % len(crawler.item_ids)
    if options.count:
        sys.exit(0)

    crawler.do_crawl(limit=options.limit, start=options.start,
                     threads=options.threads)

    if options.no_save:
        import pprint
        pprint.pprint(crawler.handler.items)
        sys.exit(1)


    print 'Creating pickle file'
    output = open('%s.pkl' % output_prefix, 'w')
    cPickle.dump(crawler.handler.items, output, cPickle.HIGHEST_PROTOCOL)
    output.close()

    output_tar.close()
    error_tar.close()
    if len(error_tar.members) == 0:
        os.remove('%s_error.tar.gz' % output_prefix)
