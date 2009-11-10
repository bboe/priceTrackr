#!/usr/bin/env python
import cPickle, os, re, sys

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

        body = body[body.find(id):]
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
        end = self.__re_search_item_pos(body, *self.regx['combo'])
        if end:
            body = body[:end[1]]
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

if __name__ == '__main__':
    def usage(msg=None):
        if msg:
            sys.stderr.write('%s\n' % msg)
        sys.stderr.write('Usage: %s folder\n' % sys.argv[0])
        sys.exit(1)

    if len(sys.argv) != 2: usage()
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        usage('File %s does not exist' % directory)

    parser = PageParser()

    count = 0
        
    items = {}
    for fname in [x for x in os.listdir(directory) if '_0' in x]:
        count += 1
        if count % 1000 == 0:
            print count
        id = fname.strip('_0.html')
        body = open(os.path.join(directory, fname)).read()
        info = parser.parse_item_page_info(id, body)
        if not info:
            continue
        if 'deactivated' not in info and 'price' not in info:
            try:
                body = open(os.path.join(directory, '%s_1.html' % id)).read()
            except IOError: continue
            info = parser.parse_cart_page(id, body)
            if not info:
                body = open(os.path.join(directory, '%s_2.html' % id)).read()
                info = parser.parse_mapping_page(id, body)
        items[id] = info

    output = open('%s.pkl' % directory.rstrip('/'), 'w')
    cPickle.dump(items, output, cPickle.HIGHEST_PROTOCOL)
    output.close()
