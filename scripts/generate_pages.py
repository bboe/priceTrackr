#!/usr/bin/env python
import datetime, math, os, sys
import MySQLdb
import sitemap_gen


def generate_sitemap(newegg_ids, directory):
    sitemap = 'sitemap.xml.gz'
    lastmod = datetime.date.today().__str__()
    sm = sitemap_gen.Sitemap(True)
    sm._base_url = 'http://test.pricetrackr.com/'
    sm._filegen = sitemap_gen.FilePathGenerator()
    sm._filegen.Preload(sitemap)
    sm._wildurl1 = sm._filegen.GenerateWildURL(sm._base_url)
    sm._wildurl2 = sm._filegen.GenerateURL(sitemap_gen.SITEINDEX_SUFFIX,
                                           sm._base_url)
    urls = ['/i/%s/' % x for x in newegg_ids]
    for url in urls:
        sm._inputs.append(sitemap_gen.InputURL({'href':url,
                                                'lastmod':lastmod,
                                                'changefreq':'daily'}))
    sm.Generate()
    os.rename(sitemap, os.path.join(directory, sitemap))

def generate_graph_pages(db, ids, directory):
    end_xml_data = """  <license>K1XUXQVMDNCL.NS5T4Q79KLYCK07EK</license>
  <chart_type>Line</chart_type>
  <chart_value prefix="$" decimals="2" separator="," position="cursor" size="14" color="000000" background_color="FFD991" alpha="90" />
  <chart_pref line_thickness="2" point_shape="none" />
  <chart_transition type="slide_down" delay="0" duration="1" order="series" />
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
        db.execute('select newegg_id from item where id = %s', id)
        newegg_id = cursor.fetchone()['newegg_id']
        db.execute(''.join(['SELECT date_added as date, original',
                            ', price, rebate, shipping from item_',
                            'history where id = %s order by date']),
                           id)
        rows = cursor.fetchall()

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

def generate_item_pages(db, ids, directory):
    title_template = """<!DOCTYPE html
PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
<title>%s &raquo; priceTrackr</title>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
<link rel="shortcut icon" href="/favicon.ico" />
<link rel="stylesheet" type="text/css" href="/layout.css" />
<script type="text/javascript" src="/javascript.js"></script>
</head>
<body>
<div id="container">
<div id="header">
<table style="width:99%%">
<!-- How can I do this without a table? -->
<tr valign="bottom">
<td><h1>priceTrackr</h1></td>
<td style="text-align:right;padding-bottom:5px"><form method="get" action="/search/">
    <div>
      <input type="text" name="q" size="20" maxlength="100" />
      <input type="submit" value="search" style="vertical-align:middle" />
    </div>
</form></td>
</tr>
</table>
</div>
<div id="menu">
  <ul id="nav">
    <li><a href="/">Home</a></li>
    <li><a href="/faq/">FAQ</a></li>
    <li><a href="/about/">About</a></li>
  </ul>
</div>
"""
    body_template = """<div id="content">
<div class="itemName"><h4><a href="http://www.newegg.com/Product/Product.asp?Item=%s" onClick="javascript:pageTracker._trackPageview('/outgoing/newegg.com/%s');">%s</a></h4>
<p>Model: %s</p></div>
<div class="itemAdd">
<script type="text/javascript"><!--
google_ad_client = "pub-0638295794514727";google_ad_slot = "9316902769";google_ad_width = 468;google_ad_height = 60;
//-->
</script>
<script type="text/javascript" src="http://pagead2.googlesyndication.com/pagead/show_ads.js"></script>
</div>
<OBJECT classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000"
codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,0,0" 
WIDTH="700" 
HEIGHT="350" 
id="charts">
  <PARAM NAME="movie" VALUE="/charts.swf?library_path=/charts_library&xml_source=/g/%s" />
  <PARAM NAME="quality" VALUE="high" />
  <PARAM NAME="bgcolor" VALUE="#666666" />
  <param name="allowScriptAccess" value="sameDomain" />
  
  <EMBED src="/charts.swf?library_path=/charts_library&xml_source=/g/%s"
 quality="high" 
 bgcolor="#C8E9FF" 
 WIDTH="700" 
 HEIGHT="350" 
 NAME="charts" 
 allowScriptAccess="sameDomain" 
 swLiveConnect="true" 
 TYPE="application/x-shockwave-flash" 
 PLUGINSPAGE="http://www.macromedia.com/go/getflashplayer">

  </EMBED>
</OBJECT>
"""
    stats_template = """<h3>Statistics</h3>
<table class="stats">
  <tr>
    <th><h3>Prices</h3></th>
    <th><h3>Current</h3></th>
    <th><h3>Minimum</h3></th>
    <th><h3>Maximum</h3></th>
  </tr>
  <tr>
    <td>original</td>
    <td>$%.2f</td>
    <td><span class="min">$%.2f</span> on %s</td>
    <td><span class="max">$%.2f</span> on %s</td>
  </tr>
  <tr>
    <td>+ savings</td><td>$%.2f</td>
    <td><span class="min">$%.2f</span> on %s</td>
    <td><span class="max">$%.2f</span> on %s</td>
  </tr>
  <tr>
    <td>+ rebate</td><td>$%.2f</td>
    <td><span class="min">$%.2f</span> on %s</td>
    <td><span class="max">$%.2f</span> on %s</td>
  </tr>
  <tr>
    <td>shipping*</td>
    <td>%s</td>
    %s
  </tr>
</table>
<p>* Shipping is calculated to zip code 93117. Minimum shipping is the lowest nonzero shipping cost.</p>
</div>
<div id="footer">
<div class="copyright">&copy; 2009 priceTrackr.  All Rights Reserved</div>
</div>
</div>
<script type="text/javascript" src="http://pagead2.googlesyndication.com/pagead/show_ads.js"></script>
<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%%3E%%3C/script%%3E"));
</script>
<script type="text/javascript">
try {
var pageTracker = _gat._getTracker("UA-510348-5");
pageTracker._setDomainName(".pricetrackr.com");
pageTracker._trackPageview();
} catch(err) {}</script>
</body>
</html>"""

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

        output = title_template % current['title']
        output +=  body_template % (newegg_id, newegg_id, current['title'],
                                    current['model'], newegg_id, newegg_id)
        if min['shipping'][1]:
            shipping = """<td><span class="min">$%.2f</span> on %s*</td>
    <td><span class="max">$%.2f</span> on %s</td>""" % \
                (min['shipping'][0] / 100., min['shipping'][1],
                 max['shipping'][0] / 100., min['shipping'][1])
        else:
            shipping = "<td colspan=2><strong>Always Free Shipping</strong></td>"

        output += stats_template % (current['original'] / 100.,
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
                                    current['shipping'] / 100.,
                                    shipping)

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

    generate_sitemap(newegg_ids, '../nginx_root/')
    print "Sitemap complete"
    generate_graph_pages(cursor, ids, '../nginx_root/graphs')
    print "Graph pages complete"
    generate_item_pages(cursor, ids, '../nginx_root/items')
    print "Item pages complete"
