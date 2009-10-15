#!/usr/bin/env python

import crawle, os, re, urllib

url = 'http://secure.newegg.com/Shopping/ShoppingCart.aspx'
shipping_re = re.compile('<td>Shipping:</td>\s*<td><strong>\$([^<]+)</strong></td>')

def transform_id(ids):
    return '%s-%s-%s' % (ids[:2], ids[2:5], ids[5:])

cookies = []
cookies.append(''.join(['NV%5FNEWEGGCOOKIE=#4{"Sites":{"USA":{"Values":{"',
                        transform_id("12802059R"), '":"1"}}}}']))
cookies.append('NV%5FORDERCOOKIE=#4%7b%22Sites%22%3a%7b%22USA%22%3a%7b%22Values%22%3a%7b%22NVS%255FCUSTOMER%255FSHIPPING%255FMETHOD1%22%3a%22038%22%2c%22NVS%255FCUSTOMER%255FZIP%255FCODE%22%3a%2293117%22%7d%7d%7d%7d')

headers = {'Cookie':';'.join(cookies)}

cc = crawle.HTTPConnectionControl(crawle.Handler())
rr = crawle.RequestResponse(url, headers=headers)
cc.request(rr)
match = shipping_re.search(rr.responseBody)
if not match:
    print 'Failure'
else:
    print 'Shipping Price: %s' % match.group(1)
