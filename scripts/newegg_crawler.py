#!/usr/bin/env python
import crawle, cPickle, time, gzip, os, re, sys, threading
from optparse import OptionParser
from StringIO import StringIO

class PageParser(object):
    regx = {}
    # Item Info
    regx['title'] = re.compile('<title>Newegg.com - ([^<]+)</title>'), 1
    regx['model'] = re.compile(''.join(['<td class="name">\s?(kits_)?Model',
                                        '</td>\s*<td class="desc"',
                                        '>([^<]+(<br>)?[^<]*)</td>'])), 2
    regx['combo'] = re.compile('<div id="pclaComboDeals">'), 0

    # Item Flags
    regx['cart'] = re.compile('title="Sale Price">See price in cart</a>'), 0
    regx['deactivated'] = re.compile('Deactivated Item'), 0
    regx['free_shipping'] = re.compile(''.join(['<dd class="shipping">Free ',
                                                'Shipping\*?\s*</dd>'])), 0

    # Item / Mapping Price Info
    regx['original'] = re.compile(''.join(['<dd class="original">Original ',
                                           'Price: \$([^<]+)</dd>'])), 1
    regx['save'] = re.compile(''.join(['<dd class="rebate">You Save: \$',
                                       '([^<]+)</dd>'])), 1
    regx['price'] = re.compile('<h3 class="zmp">\s*\$([^<]+)\s*</h3>'), 1
    regx['rebate'] = re.compile('\$([^ ]+) Mail-(i|I)n Rebate'), 1

    # Cart Page Specific
    regx['cart_unavailable'] = re.compile('removed from shopping cart due'), 0
    regx['cart_original'] = re.compile('<dd class="cartOrig">\$([^<]+)</dd'), 1
    regx['cart_save'] = re.compile(''.join(['<td class="cartSavings">\s*-\$',
                                            '([0-9.,]+)&nbsp;Instant<br>'])), 1
    regx['cart_price'] = re.compile('<dd>\$([^<]+)</dd>'), 1
    regx['cart_shipping'] = re.compile(''.join(['<td>Shipping:</td>\s*<td>',
                                                '<strong>\$([^<]+)</strong>',
                                                '</td>'])), 1    
    
    @staticmethod
    def __re_search(body, regex, group):
        match = regex.search(body)
        if match:
            return match.group(group).strip()
        else:
            return None
    @staticmethod
    def __re_search_item_pos(body, regex, group):
        match = regex.search(body)
        if match:
            return match.group(group).strip(), match.start(group)
        else:
            return None

    def parse_mapping_page(self, id, body):
        """Return price tracking information"""
        info = {}
        info['original'] = self.__re_search(body, *self.regx['original'])
        info['save'] = self.__re_search(body, *self.regx['save'])
        info['price'] = self.__re_search(body, *self.regx['price'])
        info['rebate'] = self.__re_search(body, *self.regx['rebate'])
        return info

    def parse_cart_page(self, id, body):
        """Return price tracking information or None if unavailable"""
        info = {}
        if self.__re_search(body, *self.regx['cart_unavailable']):
            return None

        info['price'], p = self.__re_search_item_pos(body,
                                                     *self.regx['cart_price'])
        b2 = body[:p]
        info['original'] = self.__re_search(b2, *self.regx['cart_original'])
        info['save'] = self.__re_search(b2, *self.regx['cart_save'])
        info['rebate'] = self.__re_search(body, *self.regx['rebate'])
        info['shipping'] = self.__re_search(body, *self.regx['cart_shipping'])
        return info

    def parse_item_page_price(self, id, body):
        """Return price tracking information, only used if free shipping"""
        info = {}
        end = self.__re_search_pos(body, *self.regx['combo'])
        if end:
            body = body[:end]
        info['original'] = self.__re_search(body, *self.regx['original'])
        info['save'] = self.__re_search(body, *self.regx['save'])
        info['price'] = self.__re_search(body, *self.regx['price'])
        info['rebate'] = self.__re_search(body, *self.regx['rebate'])
        return info

    def parse_item_page_info(self, id, body):
        """Return basic information, and prace tracking information if free
        shipping and not cart"""
        info = {}
        info['title'] = self.__re_search(body, *self.regx['title'])
        if info['title'] == 'Suggested Products':
            return None
        info['model'] = self.__re_search(body, *self.regx['model'])
        if self.__re_search(body, *self.regx['deactivated']):
            info['deactivated'] = True
            return info
        free_shipping = self.__re_search(body, *self.regx['free_shipping'])
        cart = self.__re_search(body, *self.regx['cart'])
        if free_shipping and not cart:
            info.update(self.parse_item_page_price(id, body))
        return info

class NewEggCrawler(object):
    SITEMAP_URL_PREFIX = 'http://www.newegg.com/Sitemap/USA/'
    SITEMAPS = ['newegg_sitemap_product01.xml.gz',
                'newegg_sitemap_product02.xml.gz']
    ITEM_ID_RE = re.compile(''.join(['http://www.newegg.com/Product/',
                                     'Product.aspx\?Item=([A-Z0-9]+)']))

    def __init__(self, output_prefix):
        self.item_ids = []
        self.get_product_ids()
        self.handler = NewEggCrawlHandler(output_prefix)
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
    
    def __init__(self, output_prefix):
        self.working_dir = './%s' % output_prefix
        self.error_dir = './%s_errors' % output_prefix
        self.parser = PageParser()
        self.lock = threading.Lock()
        self.items = {}

    def handle_error(self, rr):
        if not os.path.exists(self.error_dir):
            os.mkdir(self.error_dir)
        path = os.path.join(self.error_dir, '%s_%s' % rr.requestURL)
        if os.path.exists(path):
            print 'Already errored: %s - %s' % rr.requestURL
            return False
        output = open(path, 'w')
        cPickle.dump(rr, output, cPickle.HIGHEST_PROTOCOL)
        output.close()
        return True
    
    def save_page(self, rr):
        if not os.path.exists(self.working_dir):
            os.mkdir(self.working_dir)
        path = os.path.join(self.working_dir, '%s_%s.html' % rr.requestURL)
        output = open(path, 'w')
        output.write(rr.responseBody)
        output.close()

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
        if rr.responseStatus == None and rr.responseMsg == 'Socket Error':
            queue.put(rr.requestURL)
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
      
    crawler = NewEggCrawler(output_prefix)
    if options.item != None:
        crawler.item_ids = options.item

    print 'Found %d items' % len(crawler.item_ids)
    if options.count:
        sys.exit(0)

    crawler.do_crawl(limit=options.limit, start=options.start,
                     threads=options.threads)

    if options.item != None:
        print crawler.handler.items
        sys.exit(1)

    output = open('%s.pkl' % output_prefix, 'w')
    cPickle.dump(crawler.handler.items, output, cPickle.HIGHEST_PROTOCOL)
    output.close()
