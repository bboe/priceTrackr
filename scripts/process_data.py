#!/usr/bin/env python
import cPickle, os, re, string, sys, time
import MySQLdb

class ItemHistoryHelper(object):
    ID_RE = re.compile('N82E168(\d+)((IN)|R|(SF))?')
    RF = 1

    @staticmethod
    def reverse_id(id):
        root = 'N82E168'
        if id >> 28 == 0:
            return '%s%08d' % (root, id & (2 ** 28 - 1))
        elif id & 1 << 28:
            return '%s%08dR' % (root, id & (2 ** 28 - 1))
        elif id & 1 << 29:
            return '%s%08dSF' % (root, id & (2 ** 28 - 1))
        elif id & 1 << 30:
            return '%s%06dIN' % (root, id & (2 ** 28 - 1))
            
    @staticmethod
    def convert_price(price):
        trans = string.maketrans('', '')
        return int(price.translate(trans, '.,'))

    def __init__(self, id, item):
        self.id = id
        if 'title' not in item:
            raise Exception('Incomplete Item')
        self.title = item['title']
        if item['model'] != None:
            self.model = item['model']
        else:
            self.model = ''
        if 'price' not in item:
            raise Exception('Incomplete Item')
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

    def verify_text(self):
        if len(self.title) > 512:
            print 'Title too long: %s' % self.id
        if len(self.model) > 256:
            print 'Model too long: %s' % self.id
        match = self.ID_RE.match(self.id)
        if not match or int(match.group(1)) > 2**28-1:
            print 'Unknown ID: %s' % self.id, self.id[15:]
        #else: print match.groups()

    def to_num(self):
        # R = openbox, SF = downloadable software, IN = InstallerNet
        match = self.ID_RE.match(self.id)
        base = int(match.group(1))
        if match.group(2) == None:
            return base
        elif match.group(2) == 'R':
            return base | 1 << 28
        elif match.group(2) == 'SF':
            return base | 1 << 29
        elif match.group(2) == 'IN':
            return base | 1 << 30
        else:
            print 'Not matched', self.id
            return base

    def verify_savings(self):
        if self.original - self.save != self.price:
            print 'Savings Mismatch: %s' % self.id

    def add_item(self, db, date):
        db.execute(''.join(['insert into item (id, newegg_id, date_added, ',
                            'title, model) VALUES (%s, %s, %s, %s, %s)']),
                   (self.to_num(), self.id, date, self.title, self.model))

    def update_history(self, db, date):
      try:
        db.execute(''.join(['insert into item_history (id, date_added, ',
                            'original, price, rebate, shipping) VALUES',
                            '(%s, %s, %s, %s, %s, %s)']),
                   (self.to_num(), date, self.original, self.price,
                    self.rebate, self.shipping))
      except MySQLdb.IntegrityError, e:
          print e


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

    file = os.path.basename(file)
    date = file.strip('.pkl').replace('.', ':').replace('_', ' ')

    conn = MySQLdb.connect(user='pt_user', passwd='pritshiz',
                           db='priceTrackr')
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    count = cursor.execute('SELECT newegg_id from item')
    rows = cursor.fetchall()
    ids = dict([(x['newegg_id'], True) for x in rows])
    print '---'

    for id, item in items.items():
        if 'deactivated' in item:
            continue
        try:
            i = ItemHistoryHelper(id, item)
        except Exception, e:
            if e.args == ('Incomplete Item',): continue
            else: raise
        if i.title == None:
            print 'No title: %s' % id
            continue
        i.verify_savings()
        i.verify_text()
        if id not in ids:
            i.add_item(cursor, date)
        i.update_history(cursor, date)
