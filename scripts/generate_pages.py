#!/usr/bin/env python
import datetime, math, os, re, sys
import MySQLdb
import sitemap_gen

BASE_PATH = '/home/bryce/svn/priceTrackr/nginx_root/'

SITE_HEADER = """<!DOCTYPE html
PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<title>%s &raquo; priceTrackr</title>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
<link rel="shortcut icon" href="/favicon.ico" />
<link rel="alternate" type="application/rss+xml" title="RSS" href="/daily.xml" />
<link rel="stylesheet" type="text/css" href="/layout.css" />
<script type="text/javascript" src="/javascript.js"></script>
</head>
<body onload="document.getElementById('q').focus()">
<div id="container">
<div id="header">
<table style="width:99%%">
<!-- How can I do this without a table? -->
<tr valign="bottom">
<td><h1>priceTrackr</h1></td>
<td style="text-align:right;padding-bottom:5px"><form method="get" action="/search/">
    <div>
      <input type="text" name="q" id="q" size="20" maxlength="100" />
      <input type="submit" value="search" style="vertical-align:middle" />
    </div>
</form></td>
</tr>
</table>
</div>
<div id="menu">
  <ul id="nav">
    <li><a href="/">Home</a></li>
    <li><a href="/daily/"%s>Daily Drops</a></li>
    <li><a href="/faq/">FAQ</a></li>
    <li><a href="/about/">About</a></li>
  </ul>
</div>
<div id="content">
"""

SITE_FOOTER = """</div>
<div id="footer">
<div class="copyright">&copy; 2010 priceTrackr.  All Rights Reserved</div>
</div>
</div>
<script type="text/javascript" src="http://pagead2.googlesyndication.com/pagead/show_ads.js"></script>
<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
try {
var pageTracker = _gat._getTracker("UA-510348-5");
pageTracker._setDomainName(".pricetrackr.com");
pageTracker._trackPageview();
} catch(err) {}</script>
</body>
</html>
"""

ITEM_ADD = """<div class="itemAdd">
<script type="text/javascript"><!--
google_ad_client = "pub-0638295794514727";google_ad_slot = "9316902769";google_ad_width = 468;google_ad_height = 60;
//-->
</script>
<script type="text/javascript" src="http://pagead2.googlesyndication.com/pagead/show_ads.js"></script>
</div>
"""

RSS_TEMPLATE = """<?xml version="1.0"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>priceTrackr Daily Drops</title>
    <link>http://www.pricetrackr.com/daily/</link>
    <atom:link href="http://www.pricetrackr.com/daily.xml" rel="self" type="application/rss+xml" />
    <description>Daily list of items which have dropped the most according to
      priceTrackr's score function. The score function is computed as
      the drop percent multiplied by the drop value.</description>
    <language>en-us</language>
    <lastBuildDate>%s</lastBuildDate>
%s
  </channel>
</rss>
"""

DATE_822 = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S PST')


def strip_tags(data):
    return re.compile(r'<.*?>').sub('', data)


def generate_sitemap(newegg_ids, directory):
    sitemap_prefix = 'pt_sitemap'
    lastmod = datetime.date.today().__str__()
    sm = sitemap_gen.Sitemap(True)
    sm._base_url = 'http://www.pricetrackr.com/'
    sm._filegen = sitemap_gen.FilePathGenerator()
    sm._filegen.Preload('%s.xml.gz' % sitemap_prefix)
    sm._wildurl1 = sm._filegen.GenerateWildURL(sm._base_url)
    sm._wildurl2 = sm._filegen.GenerateURL(sitemap_gen.SITEINDEX_SUFFIX,
                                           sm._base_url)
    urls = ['/i/%s/' % x for x in newegg_ids]
    for url in urls:
        sm._inputs.append(sitemap_gen.InputURL({'href':url,
                                                'lastmod':lastmod,
                                                'changefreq':'daily'}))

    today = datetime.date.today().__str__()
    sm._inputs.append(sitemap_gen.InputURL({'href':'/',
                                            'changefreq':'weekly'}))
    sm._inputs.append(sitemap_gen.InputURL({'href':'/daily/', 'lastmod':today,
                                            'changefreq':'daily'}))
    sm._inputs.append(sitemap_gen.InputURL({'href':'/faq/',
                                            'changefreq':'weekly'}))
    sm._inputs.append(sitemap_gen.InputURL({'href':'/about/',
                                            'changefreq':'weekly'}))
    
    
    sm.Generate()
    os.system('mv %s* %s/' % (sitemap_prefix, directory))

def generate_daily_drops(db, drops, directory):
    output_html = 'daily.html'
    output_rss = 'daily.xml'
    
    html = SITE_HEADER % ('Daily Drops', ' class="active"')
    html += '<h1>Daily Drops</h1>\n\n'
    xml = ''

    i = 0
    for score, id, drop, percent, total in sorted(drops, reverse=True)[:50]:
        i += 1
        db.execute('SELECT title, newegg_id from item where item.id = %s', id)
        row = cursor.fetchone()
        title = row['title'].replace('& ', '&amp; ')
        line = ' '.join(['Drop Value: <strong>$%.2f</strong>',
                         'Drop Percent: <strong>%.0f%%</strong>',
                         'Current Cost: <strong>$%.2f</strong>']) \
                         % (drop / 100., percent * 100., total / 100.)
        html += '<p><a href="/i/%s/">%s</a><br/>%s</p>\n' % (row['newegg_id'],
                                                             title, line)
        xml += '    <item>\n      <title>%s</title>\n' % title
        xml += '      <link>http://www.pricetrackr.com/i/%s/</link>\n' \
            % row['newegg_id']
        xml += '      <description>%s</description>\n' % strip_tags(line)
        xml += '      <guid isPermaLink="false">%s%s</guid>\n' % (id, DATE_822)
        xml += '      <pubDate>%s</pubDate>\n    </item>' % DATE_822
        
        if i % 10 == 0:
            html += ITEM_ADD

    out_file = open(os.path.join(directory, output_rss), 'w')
    out_file.write(RSS_TEMPLATE % (DATE_822, xml))
    out_file.close()

    html += SITE_FOOTER
    out_file = open(os.path.join(directory, output_html), 'w')
    out_file.write(html)
    out_file.close()    

def generate_graph_pages(db, ids, directory):
    """Returns list of (drop_score, id, drop, drop_percent, current_total)"""
    drops = []
    today = datetime.date.today()
    #today = datetime.date(2009, 10, 21)
    yesterday = today - datetime.timedelta(days=1)    

    end_xml_data = """  <license>K1XUXQVMDNCL.NS5T4Q79KLYCK07EK</license>
  <chart_type>Line</chart_type>
  <chart_value prefix="$" decimals="2" separator="," position="cursor" size="14" color="000000" background_color="FFD991" alpha="90" />
  <chart_pref line_thickness="2" point_shape="none" />
  <chart_transition type="slide_down" delay="0" duration=".5" order="series" />
  <legend_label size="14" />
  <legend_rect width="680" x="10"/>
  <legend_transition type="slide_right" />
  <axis_category size="14" />
  <series_color>
    <value>FFCF75</value>
    <value>4E85AA</value>
    <value>FFA191</value>
    <value>AA5C4E</value>
  </series_color>
  <series_explode>
    <value>350</value>
    <value>250</value>
    <value>150</value>
    <value>100</value>
  </series_explode>
</chart>
"""
    try:
        os.mkdir(directory)
    except OSError:
        pass
    for id in ids:
        yesterday_cost = today_cost = None
        db.execute('select newegg_id from item where id = %s', id)
        newegg_id = cursor.fetchone()['newegg_id']
        db.execute(''.join(['SELECT date_added as date, original',
                            ', price, rebate, shipping from item_',
                            'history where id = %s order by date']),
                           id)
        rows = cursor.fetchall()
        if len(rows) == 0:
            print 'No tracker data: %d' % id
            continue

        data = []
        max_axis = 0
        min_axis = 0x7FFFFFF

        cur_date = rows[0]['date'].date()
        delta_days = (rows[-1]['date'].date() - cur_date).days
        if delta_days < 5:
            label_delta = 1
        else:
            label_delta = delta_days / 5
        i = 0
        while cur_date <= rows[-1]['date'].date():
            while rows[i]['date'].date() < cur_date:
                i += 1
            row = rows[i]
            
            # Calculate drop score
            if row['date'].date() == yesterday:
                yesterday_cost = row['rebate'] + row['shipping']
            elif row['date'].date() == today:
                if yesterday_cost:
                    today_cost = row['rebate'] + row['shipping']
                    drop = yesterday_cost - today_cost
                    if drop > 0:
                        drop_percent = drop * 1.0 / yesterday_cost
                        drop_score = drop_percent * drop
                        drops.append((drop_score, id, drop, drop_percent,
                                      today_cost))

#             if cur_date.day == 1:  # list only months
            if len(data) % label_delta == 0: # list every label_delta dates
                print_date = cur_date
            else:
                print_date = ''

            if row['date'].date() != cur_date:
                data.append([print_date, None, None, None, None])
                cur_date += datetime.timedelta(days=1)
                continue
            else:
                cur_date += datetime.timedelta(days=1)

            tmp = [print_date]
            tmp.extend([x / 100. for x in [row['original'], row['price'],
                                           row['rebate'],
                                           row['original'] + row['shipping']]])

            data.append(tmp)
            if tmp[3] < min_axis: min_axis = tmp[3]
            if tmp[4] > max_axis: max_axis = tmp[4]

        if min_axis == max_axis:
            extra = 5
        else:
            delta = max_axis - min_axis
            extra = (delta / .9) - delta

        output = ''.join(['<chart>\n  <axis_value min="%d" max="%d" size="14"',
                          ' steps="%d" prefix="$" />\n  <chart_data>\n']) % \
                          (math.floor(min_axis - extra),
                           math.ceil(max_axis + extra), 5)

        for i, column in enumerate([None, 'original', '+ savings', '+ rebates',
                                    'original + shipping']):
            if column:
                title = '<string>%s</string>' % column
            else:
                title = '<null/>'
            output += '    <row>\n      %s\n' % title
            for row in data:
                if i == 0:
                    output += '      <string>%s</string>\n' % row[i].__str__()[2:]
                elif row[i]:
                    output += '      <number>%.2f</number>\n' % row[i]
                else:
                    output += '      <null/>\n'
            output += '    </row>\n'
        output += '  </chart_data>\n%s' % end_xml_data
        file = open(os.path.join(directory, '%s.html' % newegg_id), 'w')
        file.write(output)
        file.close()
    return drops

def generate_item_pages(db, ids, directory):
    body_template = """<div class="itemName"><h4><a href="http://www.newegg.com/Product/Product.asp?Item=%s" onclick="javascript:pageTracker._trackPageview('/outgoing/newegg.com/%s');">%s</a></h4>
<p>Model: %s</p></div>
<div class="itemAdd">
<script type="text/javascript"><!--
google_ad_client = "pub-0638295794514727";google_ad_slot = "9316902769";google_ad_width = 468;google_ad_height = 60;
//-->
</script>
<script type="text/javascript" src="http://pagead2.googlesyndication.com/pagead/show_ads.js"></script>
</div>
<object
   type="application/x-shockwave-flash"
   data="/charts.swf?library_path=/charts_library&amp;xml_source=/g/%s"
   width="700" height="350">
  <param
     name="movie"
     value="/charts.swf?library_path=/charts_library&amp;xml_source=/g/%s" />
  <param name="quality" value="high" />
  <param name="bgcolor" value="#C8E9FF" />
  <param name="wmode" value="transparent" />
  <param name="allowScriptAccess" value="sameDomain" />
</object>
"""
    stats_template = """<h3>Statistics</h3>
<table class="stats">
  <tr>
    <th><h3>Prices</h3></th>
    <th><h3>as of %s</h3></th>
    <th><h3 class="min">Minimum</h3></th>
    <th><h3 class="max">Maximum</h3></th>
  </tr>
  <tr style="background:#FFCF75">
    <td>original</td>
    <td>$%.2f</td>
    <td>$%.2f on %s</td>
    <td>$%.2f on %s</td>
  </tr>
  <tr style="background:#4E85AA;color:#C8E9FF">
    <td>+ savings</td><td>$%.2f</td>
    <td>$%.2f on %s</td>
    <td>$%.2f on %s</td>
  </tr>
  <tr style="background:#FFA191">
    <td>+ rebates</td><td>$%.2f</td>
    <td>$%.2f on %s</td>
    <td>$%.2f on %s</td>
  </tr>
  <tr style="background:#AA5C4E;color:#C8E9FF">
    <td>shipping*</td>
    <td>%s</td>
    %s
  </tr>
</table>
<p>* Shipping is calculated to zip code 93117. Minimum shipping is the lowest nonzero shipping cost.</p>
"""

    try:
        os.mkdir(directory)
    except OSError:
        pass
    for id in ids:
        db.execute(''.join(['SELECT title, model, item_history.date_added ',
                            'as update_date, item_history.original, ',
                            'item_history.price, item_history.rebate, ',
                            'item_history.shipping, newegg_id from item, ',
                            'item_history where item_history.id = item.id ',
                            'and item.id = %s order by update_date']), id)
        rows = cursor.fetchall()
        current = rows[-1]
        current_date = current['update_date'].date()
        newegg_id = current['newegg_id']

        keys = ['original', 'price', 'rebate', 'shipping']
        max = {}
        min = {}
        for key in keys:
            max[key] = 0, None
            min[key] = 0x7FFFFFFF, None
        for row in rows:
            for key in keys:
                if row[key] > max[key][0]:
                    max[key] = row[key], row['update_date'].date()
                if key != 'shipping' and row[key] < min[key][0]:
                    min[key] = row[key], row['update_date'].date()
                elif key == 'shipping' and row[key] < min[key][0] and \
                        row[key] != 0:
                    min[key] = row[key], row['update_date'].date()

        output = SITE_HEADER % (current['title'], '')
        output +=  body_template % (newegg_id, newegg_id, current['title'],
                                    current['model'], newegg_id, newegg_id)
        if min['shipping'][1]:
            shipping = """<td>$%.2f on %s*</td>
    <td>$%.2f on %s</td>""" % \
                (min['shipping'][0] / 100., min['shipping'][1],
                 max['shipping'][0] / 100., min['shipping'][1])
        else:
            shipping = "<td colspan=2><strong>Always Free Shipping</strong></td>"

        if current['shipping'] != 0:
            current_shipping = '$%.2f' % (current['shipping'] / 100.)
        else:
            current_shipping = '<strong>FREE!</strong>'

        output += stats_template % (current_date, current['original'] / 100.,
                                    min['original'][0] / 100.,
                                    min['original'][1],
                                    max['original'][0] / 100.,
                                    max['original'][1],
                                    current['price'] / 100.,
                                    min['price'][0] / 100.,
                                    min['price'][1],
                                    max['price'][0] / 100.,
                                    max['price'][1],
                                    current['rebate'] / 100.,
                                    min['rebate'][0] / 100.,
                                    min['rebate'][1],
                                    max['rebate'][0] / 100.,
                                    max['rebate'][1],
                                    current_shipping,
                                    shipping)
        output += SITE_FOOTER
        file = open(os.path.join(directory, '%s.html' % newegg_id), 'w')
        file.write(output)
        file.close()
    

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
    conn = MySQLdb.connect(user='pt_user', passwd='pritshiz', db='priceTrackr')
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    
    if len(sys.argv) == 2:
        filter = ' where newegg_id = %s'
        filter_id = sys.argv[1]
    else:
        filter = ''
        filter_id = None

    count = cursor.execute('SELECT id, newegg_id from item%s' % filter, filter_id)
    rows = cursor.fetchall()
    ids = [x['id'] for x in rows]
    newegg_ids = [x['newegg_id'] for x in rows]
    print 'Found %d items' % len(ids)

    if not filter_id:
        generate_sitemap(newegg_ids, BASE_PATH)
        print "Sitemap complete"
    drops = generate_graph_pages(cursor, ids,
                                 os.path.join(BASE_PATH, 'graphs'))
    print "Graph pages complete"
    generate_daily_drops(cursor, drops, BASE_PATH)
    generate_item_pages(cursor, ids, os.path.join(BASE_PATH, 'items'))
    print "Item pages complete"
