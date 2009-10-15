#!/usr/bin/env python
import cPickle, os, re, sys, time

class PageParser(object):
    regx = {}
    regx['title'] = re.compile('<title>Newegg.com - ([^<]+)</title>'), 1
    regx['model'] = re.compile(''.join(['<td class="name">\s?(kits_)?Model',
                                        '</td>\s*<td class="desc"',
                                        '>([^<]+(<br>)?[^<]*)</td>'])), 2
    regx['cart'] = re.compile('title="Sale Price">See price in cart</a>'), 0
    regx['deactivated'] = re.compile('Deactivated Item'), 0
    regx['original'] = re.compile(''.join(['<dd class="original">Original ',
                                           'Price: \$([^<]+)</dd>'])), 1
    regx['save'] = re.compile(''.join(['<dd class="rebate">You Save: \$',
                                       '([^<]+)</dd>'])), 1
    regx['price'] = re.compile('<h3 class="zmp">\s*\$([^<]+)\s*</h3>'), 1
    regx['rebate'] = re.compile(''.join(['<strong>\$[^<]+</strong> after ',
                                         '\$([^ ]+) Mail-In Rebate'])), 1
    regx['map_rebate'] = re.compile('Before \$([^ ]+) Mail-In Rebate'), 1
    regx['shipping'] = re.compile(''.join(['<dd class="shipping">Free ',
                                           'Shipping\*\s*</dd>'])), 0

    def __init__(self, date_dir):
        self.mapping_dir = os.path.join(date_dir, 'mapping')

    @staticmethod
    def __re_search(body, regex, group):
        match = regex.search(body)
        if match:
            return match.group(group).strip()
        else:
            return None

    def parse_mapping_page(self, id, body):
        info = {}
        info['original'] = self.__re_search(body, *self.regx['original'])
        # ORIGINAL TEST
        # if not info['original'] and 'Original Price' in body:
        #     print 'Missing Original: %s' % id
        #     return None
        if info['original']:
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
        if not info['rebate']:
            info['rebate'] = self.__re_search(body, *self.regx['map_rebate'])
            # REBATE TEST
            # if not info['rebate'] and 'Mail-In Rebate' in body:
            #     print 'Missing Rebate: %s' % id
            #     return None
        return info

    def parse_item_page(self, id, body):
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
        if self.__re_search(body, *self.regx['shipping']):
            info['free_shipping'] = True
        # FREE SHIPPING TEST
        # elif 'Free Shipping*' in body:
        #     print id
        if self.__re_search(body, *self.regx['cart']):
            body = open(os.path.join(self.mapping_dir, '%s.html' % id)).read()
            info.update(self.parse_mapping_page(id, body))
            return info
        info['original'] = self.__re_search(body, *self.regx['original'])
        # ORIGINAL TEST
        # if not info['original'] and 'Original Price' in body:
        #     print 'Missing Original: %s' % id
        #     return None
        if info['original']:
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
        items[id] = pp.parse_item_page(id, body)

    output = open('%s.pkl' % date_dir.strip('/'), 'w')
    cPickle.dump(items, output, cPickle.HIGHEST_PROTOCOL)
    output.close()
    sys.exit(1)

    
    invalids = 0
    deactivated = 0
    free_shipping = 0
    rebates = 0
    saves = 0
    for item in items.values():
        if item is None:
            invalids += 1
            continue
        if 'deactivated' in item:
            deactivated += 1
            continue
        if 'free_shipping' in item:
            free_shipping += 1
        if item['rebate']:
            rebates += 1
        if 'save' in item and item['save']:
            saves += 1

    
    print 'Invalid: %d' % invalids
    print 'Deactivated: %d' % deactivated
    print 'Free shipping: %d' % free_shipping
    print 'Rebates: %d' % rebates
    print 'Saves: %d' % saves
