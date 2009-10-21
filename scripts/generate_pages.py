#!/usr/bin/env python
import math, os, sys, datetime
import MySQLdb



    # def add_item(self, db, date):
    #     db.execute(''.join(['insert into item (id, newegg_id, date_added, ',
    #                         'title, model) VALUES (%s, %s, %s, %s, %s)']),
    #                (self.to_num(), self.id, date, self.title, self.model))

    # def update_history(self, db, date):
    #     db.execute(''.join(['insert into item_history (id, date_added, ',
    #                         'original, price, rebate, shipping) VALUES',
    #                         '(%s, %s, %s, %s, %s, %s)']),
    #                (self.to_num(), date, self.original, self.price,
    #                 self.rebate, self.shipping))

def generate_graph_pages(db, ids):
    end_xml_data = """  <license>K1XUXQVMDNCL.NS5T4Q79KLYCK07EK</license>
  <chart_type>Line</chart_type>
  <chart_value prefix="$" decimals="2" separator="," position="cursor" size="14" color="000000" background_color="FFD991" alpha="90" />
  <chart_pref line_thickness="2" point_shape="none" />
  <chart_transition type="slide_down" delay="0" duration="1" order="series" />
  <legend_rect x="5" y="5" width="490" />
  <legend_transition type="slide_right" delay="0" duration="1" />
  <axis_category skip="0" />
  <series_color>
    <value>FFCF75</value>
    <value>AA5C4E</value>
    <value>4E85AA</value>
  </series_color>
  <series_explode>
    <value>250</value>
    <value>175</value>
    <value>100</value>
  </series_explode>
</chart>
"""
    os.mkdir('graphs')
    for id in ids:
        db.execute(''.join(['SELECT date_added as date, original',
                            ', price, rebate, shipping from item_',
                            'history where id = %s order by date']),
                           id)
        rows = cursor.fetchall()
        data = []

        max_axis = 0
        min_axis = 0x7FFFFFF
        
        prev_date = None
        for row in rows:
            tmp = [row['date'].date()]
            tmp.extend([x / 100. for x in [row['original'], row['price'],
                                           row['rebate'],
                                           row['original'] + row['shipping']]])

            if row['date'].date() != prev_date:
                data.append(tmp)
                prev_date = row['date'].date()
            else:
                data[-1] = tmp
            if tmp[1] > max_axis: max_axis = tmp[1]
            if tmp[4] < min_axis: min_axis = tmp[4]

        output = ''.join(['<chart>\n  <axis_value min="%d" max="%d" ',
                          'steps="%d" prefix="$" />\n  <chart_data>\n']) % \
                          (math.floor(min_axis * .99),
                           math.ceil(max_axis * 1.01), 5)

        for i, column in enumerate([None, 'original', '+ savings', '+ rebates',
                                    'original + shipping']):
            if column:
                title = '<string>%s</string>' % column
            else:
                title = '<null/>'
            output += '    <row>\n      %s\n' % title
            for row in data:
                if i == 0:
                    output += '      <string>%s</string>\n' % row[i]
                else:
                    output += '      <number>%.2f</number>\n' % row[i]
            output += '    </row>\n'
        output += '  </chart_data>\n%s' % end_xml_data
        file = open(os.path.join('graphs', '%s.html' % reverse_id(id)), 'w')
        file.write(output)
        file.close()

def generate_item_pages(db, ids):
    pass
    

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
    
if __name__ == '__main__':
    conn = MySQLdb.connect(user='root', db='priceTrackr')
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

    count = cursor.execute('SELECT id from item')
    rows = cursor.fetchall()
    ids = [x['id'] for x in rows]

    generate_graph_pages(cursor, ids)
    generate_item_pages(cursor, ids)
