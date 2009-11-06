#!/usr/bin/env python
import math, os, sys
import MySQLdb

def generate_graph_pages(db, ids, directory):
    end_xml_data = """  <license>K1XUXQVMDNCL.NS5T4Q79KLYCK07EK</license>
  <chart_type>Line</chart_type>
  <chart_value prefix="$" decimals="2" separator="," position="cursor" size="14" color="000000" background_color="FFD991" alpha="90" />
  <chart_pref line_thickness="2" point_shape="none" />
  <chart_transition type="slide_down" delay="0" duration="1" order="series" />
  <legend_rect x="5" y="5" width="490" />
  <legend_transition type="slide_right" />
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
            if tmp[3] < min_axis: min_axis = tmp[3]
            if tmp[4] > max_axis: max_axis = tmp[4]

        output = ''.join(['<chart>\n  <axis_value min="%d" max="%d" ',
                          'steps="%d" prefix="$" />\n  <chart_data>\n']) % \
                          (math.floor(min_axis * .95),
                           math.ceil(max_axis * 1.05), 5)

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
                else:
                    output += '      <number>%.2f</number>\n' % row[i]
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
      <input type="text" name="q" id="searchInput" value="search..." size="20" maxlength="100" onfocus="searchInputClick();" onblur="searchInputBlur();" />
      <input type="image" alt="Submit" src="/images/search.png" style="vertical-align:middle" />
    </div>
</form></td>
</tr>
</table>
</div>
<div id="menu">
  <ul id="nav">
    <li><a href="/">Home</a></li>
    <li><a href="/faq/">FAQ</a></li>
    <li><a href="/contact/">Contact</a></li>
    <li><a href="/about/">About</a></li>
  </ul>
</div>
"""
    body_template = """<div id="content">
<div class="itemName"><h4><a href="http://www.newegg.com/Product/Product.asp?Item=%s" onClick="javascript:pageTracker._trackPageview('/outgoing/newegg.com/%s');">%s</a></h4>
<p>Model: %s</p></div>
<div class="itemAdd">
<script type="text/javascript"><!--
google_ad_client = "pub-0638295794514727";
/* 468x60, created 11/6/09 */
google_ad_slot = "9316902769";
google_ad_width = 468;
google_ad_height = 60;
//-->
</script>
<script type="text/javascript"
src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
</script>
</div>
<OBJECT classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000"
codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,0,0" 
WIDTH="400" 
HEIGHT="250" 
id="charts">
  <PARAM NAME="movie" VALUE="/charts.swf?library_path=/charts_library&xml_source=/g/%s" />
  <PARAM NAME="quality" VALUE="high" />
  <PARAM NAME="bgcolor" VALUE="#666666" />
  <param name="allowScriptAccess" value="sameDomain" />
  
  <EMBED src="/charts.swf?library_path=/charts_library&xml_source=/g/%s"
 quality="high" 
 bgcolor="#C8E9FF" 
 WIDTH="500" 
 HEIGHT="250" 
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
<p>* Shipping is calculated to zip code 93117. Minimum shipping is the lowest nonzero shipping cost.</p></div>
<div id="adds">
<h2>Advertisements</h2>
<br/>
<br/>
<script type="text/javascript"><!--
google_ad_client="pub-0638295794514727";google_ad_width=120;google_ad_height=240;google_ad_format="120x240_as";google_ad_type="text_image";google_ad_channel="6355930926";google_color_border="336699";google_color_bg="FFFFFF";google_color_link="0000FF";google_color_text="000000";google_color_url="008000";
//--></script>
<script type="text/javascript"
  src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
</script>
</div>

<div id="footer">
<div class="copyright">&copy; 2009 priceTrackr.  All Rights Reserved</div>
</div>
</div>
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

    count = cursor.execute('SELECT id from item')
    rows = cursor.fetchall()
    ids = [x['id'] for x in rows]

    generate_graph_pages(cursor, ids, '../nginx_root/graphs')
    print "Graph pages complete"
    generate_item_pages(cursor, ids, '../nginx_root/items')
    print "Item pages complete"
