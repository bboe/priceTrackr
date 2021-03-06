#!/usr/bin/env python
import crawle, cPickle, gzip, os, re, socket, sys, tarfile, threading, time
from optparse import OptionParser
from StringIO import StringIO
from page_parser import PageParser

class NewEggCrawler(object):
    SITEMAP_INDEX = 'http://www.newegg.com/Siteindex_USA.xml'
    LOC_RE = re.compile('<loc>([^<]+)</loc>')
    ITEM_ID_RE = re.compile(''.join(['http://www.newegg.com/Product/',
                                     'Product.aspx\?Item=([A-Z0-9]+)']))

    def __init__(self, output_tar, error_tar, save):
        self.item_ids = []
        self.get_product_ids()
        self.handler = NewEggCrawlHandler(output_tar, error_tar, save)
        self.queue = crawle.URLQueue()

    def get_sitemaps(self):
        rr = crawle.quick_request(self.SITEMAP_INDEX, redirects=1)
        if rr.response_status != 200:
            print 'Could not get index: %d' % rr.response_status
            sys.exit(1)
        data = rr.response_body
        return [x for x in self.LOC_RE.findall(data) if 'product' in x]

    def get_product_ids(self):
        sitemaps = self.get_sitemaps()
        for sitemap in sitemaps:
            rr = crawle.quick_request(sitemap, redirects=1)
            if rr.response_status != 200:
                print 'Error fetching sitemap: %d' % rr.response_status
                print rr.request_url, rr.response_url
                sys.exit(1)
            body = gzip.GzipFile(fileobj=StringIO(rr.response_body)).read()
            self.item_ids.extend(self.ITEM_ID_RE.findall(body))

    def do_crawl(self, limit=None, start=0, threads=1):
        if limit:
            self.item_ids = self.item_ids[:limit + start]
        for item_id in self.item_ids[start:]:
            self.queue.put((item_id, 0))
        controller = crawle.Controller(handler=self.handler, queue=self.queue,
                                       num_threads=threads)
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

    ITEM = 0
    CART = 1
    MAPPING = 2

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
        info = tarfile.TarInfo('error/%s-%s' % rr.request_url)
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
        info = tarfile.TarInfo('pages/%s-%s' % rr.request_url)
        info.size = len(temp_file.buf)
        info.mtime = time.time()
        self.lock.acquire()
        self.output_tar.members = []
        self.output_tar.addfile(info, temp_file)
        self.lock.release()
        temp_file.close()

    def pre_process(self, rr):
        if not isinstance(rr.request_url, tuple):
            print 'Something slid by: %s' % rr.response_url
        item_id, r_type = rr.request_url
        if r_type == self.ITEM:
            rr.response_url = ''.join([self.ITEM_URL_PREFIX, item_id])
        elif r_type == self.CART:
            rr.response_url = self.CART_URL
            c_id = ''.join(['NV%5FNEWEGGCOOKIE=#4{"Sites":{"USA":{"Values":{"',
                            self.transform_id(item_id), '":"1"}}}}'])
            rr.request_headers = {'Cookie':';'.join([self.ZIP_COOKIE, c_id])}
        elif r_type == self.MAPPING:
            rr.response_url = ''.join([self.MAP_URL_PREFIX, item_id])
        else:
            raise Exception('Unknown type')
        rr.redirects = 0

    def process(self, rr, queue):
        if rr.response_status == None:
            try:
                if isinstance(rr.error, socket.error):
                    queue.put(rr.request_url)
                elif isinstance(rr.error, crawle.CrawleRedirectsExceeded):
                    pass
                else:
                    self.handle_error(rr)
            except:
                self.handle_error(rr)
            return
        elif rr.response_status != 200:
            self.handle_error(rr)
            return
        item_id, r_type = rr.request_url
        if r_type == self.ITEM:
            info = self.parser.parse_item_page_info(item_id, rr.response_body)
            if not info:
                return
            if 'deactivated' not in info and 'price' not in info:
                queue.put((item_id, self.CART))
        elif r_type == self.CART:
            info = self.parser.parse_cart_page(item_id, rr.response_body)
            if not info:
                queue.put((item_id, self.MAPPING))
                return
        elif r_type == self.MAPPING:
            info = self.parser.parse_mapping_page(item_id, rr.response_body)
        else:
            raise Exception('Unknown Type')
        self.lock.acquire()
        if r_type == self.ITEM:
            self.items[item_id] = info
        else:
            self.items[item_id].update(info)
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

    try:
        if options.count:
            sys.exit(0)
        else:
            crawler.do_crawl(limit=options.limit, start=options.start,
                             threads=options.threads)
    finally:
        if output_tar:
            output_tar.close()
            error_tar.close()
            if len(output_tar.members) == 0:
                os.remove('%s.tar.gz' % output_prefix)
            if len(error_tar.members) == 0:
                os.remove('%s_error.tar.gz' % output_prefix)

    if options.no_save:
        import pprint
        pprint.pprint(crawler.handler.items)
        sys.exit(1)


    print 'Creating pickle file'
    output = open('%s.pkl' % output_prefix, 'w')
    cPickle.dump(crawler.handler.items, output, cPickle.HIGHEST_PROTOCOL)
    output.close()

