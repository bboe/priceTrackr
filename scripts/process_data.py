#!/usr/bin/env python
import cPickle, os, sys

class ItemHistoryHelper(object):
    @staticmethod
    def convert_price(price):
        return int(price.translate(None, '.,'))

    def __init__(self, id, item):
        self.id = id
        self.price = self.convert_price(item['price'])
        if item['original'] != None:
            self.original = self.convert_price(item['original'])
            self.save = self.convert_price(item['save'])
        else:
            self.original = self.price
            self.save = 0
        if item['rebate'] != None:
            self.rebate = self.price - self.convert_price(item['rebate'])
        else:
            self.rebate = self.price
        if 'shipping' not in item:
            self.shipping = 0
        else:
            self.shipping = self.convert_price(item['shipping'])

    def verify_savings(self):
        if self.original - self.save != self.price:
            print 'Savings Mismatch: %s' % self.id

if __name__ == '__main__':
    def usage(msg=None):
        if msg:
            sys.stderr.write('%s\n' % msg)
        sys.stderr.write('Usage: %s pickle_file\n' % sys.argv[0])
        sys.exit(1)

    if len(sys.argv) != 2: usage()
    file = sys.argv[1]
    if not os.path.exists(file):
        usage('File %s does not exist' % file)

    try:
        items = cPickle.load(open(file))
    except cPickle.UnpicklingError:
        usage('Invalid pickle file')
    except Exception, e:
        raise

    deactivated = 0
    savings = 0
    rebates = 0

    for id, item in items.items():
        if 'deactivated' in item:
            deactivated += 1
            continue
        i = ItemHistoryHelper(id, item)
        i.verify_savings()
        if i.save: savings += 1
        if i.rebate != i.price: rebates += 1

    print 'Deactivated: %d' % deactivated
    print 'Savings: %d' % savings
    print 'Rebates: %d' % rebates
