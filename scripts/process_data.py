#!/usr/bin/env python
import cPickle, os, sys

class ItemHistoryHelper(object):
    @staticmethod
    def convert_price(price):
        return int(price.translate(None, '.,'))

    def __init__(self, id, item):
        self.id = id
        self.cost = self.convert_price(item['price'])
        if item['original'] != None:
            self.original = self.convert_price(item['original'])
            try:
                if self.original - self.convert_price(item['save']) != self.cost:
                    print '%s cost mismatch' % id
                    print self.original, self.cost, item['save']
            except:
               pass#print id
        else:
            self.original = self.cost
        #self.shipping = self.convert_price(item['shipping'])

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

    for id, item in items.items():
        if 'deactivated' in item: continue
        ItemHistoryHelper(id, item)
