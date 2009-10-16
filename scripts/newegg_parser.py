#!/usr/bin/env python
import cPickle, os, re, sys, time

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
    
    def __init__(self, date_dir):
        self.mapping_dir = os.path.join(date_dir, 'mapping')
        self.cart_dir = os.path.join(date_dir, 'cart')

    @staticmethod
    def __re_search(body, regex, group):
        match = regex.search(body)
        if match:
            return match.group(group).strip()
        else:
            return None
    @staticmethod
    def __re_search_pos(body, regex, group):
        match = regex.search(body)
        if match:
            return match.start(group)
        else:
            return None


    def parse_mapping_page(self, id, body):
        info = {}
        info['original'] = self.__re_search(body, *self.regx['original'])
        # ORIGINAL TEST
        # if not info['original'] and 'Original Price' in body:
        #     print 'Missing Original: %s' % id
        #     return None
        info['save'] = self.__re_search(body, *self.regx['save'])
        # SAVE TEST
        # if not info['save'] and 'You Save' in body:
        #     print 'Missing Saving: %s' % id
        #     return None
        info['price'] = self.__re_search(body, *self.regx['price'])
        # PRICE TEST
        # if not info['price']:
        #     print 'Missing Price: %s' % id
        #     return None
        info['rebate'] = self.__re_search(body, *self.regx['rebate'])
        # REBATE TEST
        # if not info['rebate'] and 'Mail-In Rebate' in body:
        #     print 'Missing Rebate: %s' % id
        #     return None
        return info

    def parse_cart_page(self, id, body, free_shipping):
        info = {}
        if self.__re_search(body, *self.regx['cart_unavailable']):
            body = open(os.path.join(self.mapping_dir, '%s.html' % id)).read()
            mapping = self.parse_mapping_page(id, body)
            if mapping:
                info.update(mapping)
            return info
        
        info['original'] = self.__re_search(body, *self.regx['cart_original'])
        # ORIGINAL TEST
        # if not info['original'] and 'cartOrig' in body:
        #     print 'Missing Original: %s' % id
        #     return None
        info['save'] = self.__re_search(body, *self.regx['cart_save'])
        # SAVE TEST
        # if not info['save'] and 'Instant' in body:
        #     print 'Missing Saving: %s' % id
        #     return None
        info['rebate'] = self.__re_search(body, *self.regx['rebate'])
        # REBATE TEST
        # if not info['rebate'] and 'Mail-In Rebate' in body:
        #     print 'Missing Rebate: %s' % id
        #     return None
        info['price'] = self.__re_search(body, *self.regx['cart_price'])
        # PRICE TEST
        # if not info['price']:
        #     print 'Missing Price: %s' % id
        #     return None
        info['shipping'] = self.__re_search(body, *self.regx['cart_shipping'])
        # SHIPPING TEST
        # if not info['shipping']:
        #     print 'Missing Shipping: %s' % id
        #     return None
        # if  info['shipping'] == '0.00' and not free_shipping:
        #     print 'Inconsistent Shipping: %s' % id
        #     return None
        return info

    def parse_item_page_price(self, id, body):
        info = {}
        end = self.__re_search_pos(body, *self.regx['combo'])
        if end:
            body = body[:end]
        info['original'] = self.__re_search(body, *self.regx['original'])
        # ORIGINAL TEST
        # if not info['original'] and 'Original Price' in body:
        #     print 'Missing Original: %s' % id
        #     return None
        info['save'] = self.__re_search(body, *self.regx['save'])
        # SAVE TEST
        # if not info['save'] and 'You Save' in body:
        #     print 'Missing Saving: %s' % id
        #     return None
        info['price'] = self.__re_search(body, *self.regx['price'])
        # PRICE TEST
        # if not info['price']:
        #     print 'Missing Price: %s' % id
        #     return None
        info['rebate'] = self.__re_search(body, *self.regx['rebate'])
        # REBATE TEST
        # if not info['rebate'] and 'Mail-In Rebate' in body:
        #     print 'Missing Rebate: %s' % id
        #     return None
        return info


    def parse_item_page_info(self, id, body):
        info = {}
        info['title'] = self.__re_search(body, *self.regx['title'])
        if info['title'] == 'Suggested Products':
            return None
        info['model'] = self.__re_search(body, *self.regx['model'])
        # MODEL TEST
        # if not info['model'] and 'Model' in body and \
        #         '<td colspan="2" class="title">Model</td>' not in body:
        #     print 'Missing Model: %s' % id, info['title']
        if self.__re_search(body, *self.regx['deactivated']):
            # VERIFY DEACTIVATION
            # if self.__re_search(body, *self.regx['price']):
            #     print 'Deactivation Error: %s' % id
            #     return None
            info['deactivated'] = True
            return info
        if self.__re_search(body, *self.regx['free_shipping']):
            info['free_shipping'] = True
        # FREE SHIPPING TEST
        # elif '">Free Shipping' in body:
        #     print 'Failed free shipping: %s' % id
        if self.__re_search(body, *self.regx['cart']):
            body = open(os.path.join(self.cart_dir, '%s.html' % id)).read()
            cart = self.parse_cart_page(id, body, 'free_shipping' in info)
            if cart:
                info.update(cart)
            
            # Verify cart and mapping match
            # body = open(os.path.join(self.mapping_dir, '%s.html' % id)).read()
            # mapping = self.parse_mapping_page(id, body)
            # for key in mapping:
            #     if cart and mapping[key] != cart[key]:
            #         print 'difference in %s %s: %s %s' % (id, key,
            #                                               mapping[key],
            #                                               cart[key])
        else:
            main = self.parse_item_page_price(id, body)
            if main:
                info.update(main)

            # Verify main and mapping match
            # body = open(os.path.join(self.mapping_dir, '%s.html' % id)).read()
            # mapping = self.parse_mapping_page(id, body)
            # for key in mapping:
            #     if main and mapping[key] != main[key]:
            #         print 'Difference in %s [%s] map:%s %s' % (id, key,
            #                                                    mapping[key],
            #                                                    main[key])

        return info

        
if __name__ == '__main__':
    date_dir = sys.argv[1]
    items_dir = os.path.join(date_dir, 'items')
    pages = os.listdir(items_dir)
    pp = PageParser(date_dir)
    items = {}

    for page in pages:
        id = page.split('.')[0]
        page = os.path.join(items_dir, page)
        body = open(page).read()
        items[id] = pp.parse_item_page_info(id, body)

    output = open('%s.pkl' % date_dir.strip('/'), 'w')
    cPickle.dump(items, output, cPickle.HIGHEST_PROTOCOL)
    output.close()
