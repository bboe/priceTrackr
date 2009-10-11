#!/usr/bin/python
# Copyright 2006 Bryce Boe

import socket
import urllib2
import re
import sys

CONNECT_FAILED	= -1
INVALID_TITLE	= -2
NO_NAME		= -3
NO_COST_PRICE	= -4

socket.setdefaulttimeout(5)

class RedirectHandler(urllib2.HTTPRedirectHandler):
	def http_error_301(self,req,fp,code,msg,headers):
		sys.stderr.write('301: '+ req.get_full_url() + '\n')
		raise Exception
	def http_error_302(self,req,fp,code,msg,headers):
		sys.stderr.write('302: '+ req.get_full_url() + '\n')
		raise Exception
	def http_error_303(self,req,fp,code,msg,headers):
		sys.stderr.write('303: '+ req.get_full_url() + '\n')
		raise Exception
	def http_error_307(self,req,fp,code,msg,headers):
		sys.stderr.write('307: '+ req.get_full_url() + '\n')
		raise Exception

def openUrl( url, numRetrys = 0):
	request = urllib2.Request(url)
	currRetrys = 0;
	while (True):
		try:
			opener = urllib2.build_opener(RedirectHandler())
			sock = opener.open(request)
			toReturn = sock.read()
			sock.close()
		except urllib2.URLError:
			if (currRetrys < numRetrys):
				currRetrys += 1
				continue
			else:
				return False
		except socket.timeout:
			if (currRetrys < numRetrys):
				currRetrys += 1
				continue
			else:
				return False
		except Exception:
			return False
		return toReturn
		
def toInt(x):
	return str(x).replace('.','').replace(',','')

rSmallName = re.compile('<title>Newegg.com - (.* - (Retail|OEM))</title>',re.DOTALL)
rName = re.compile('<h1>\s*(.*- (Retail|OEM))\s*</h1>',re.DOTALL)
rOrig = re.compile('<dd class="original">Original Price: \$([.,\d]*)</dd>')
rSavings = re.compile('<dd class="rebate">You Save: \$([.,\d]*)</dd>')
rCost = re.compile('<dd class="final">\s*<h3 class="zmp">\$([.,\d]*)</h3>\s*</dd>')
rARebate = re.compile('<strong>\$([.,\d]*)</strong> after \$.* Mail-In Rebate')
rShipping = re.compile('<span class="noteSavings">.*\$([.,\d]*).*</span>')
rModel = re.compile('<TD class="qspecTitle">Model</TD>\s*<TD class="qspecDesc">(.*)</TD>')
rOrig2 = re.compile('<dd class="original">Original Price: \$([.,\d]*)</dd>')
rSavings2 = re.compile('<dd class="rebate">You Save: \$([.,\d]*)</dd>')
rCost2 = re.compile('<dd class="final">\s*<h3 class="zmp">\$([.,\d]*)</h3>\s*</dd>')
rARebate2 = re.compile('<strong>\$([.,\d]*)</strong>')

def parse(id,update=False,debug=False):
	web = openUrl('http://www.newegg.com/Product/Product.aspx?Item='+id,5)
	if not web:
		return False,id,CONNECT_FAILED
	orig = savings = cost = aRebate = shipping = 0
	name = smallName = model = ''

	# Check for title
	m = rSmallName.search(web)
	if not m:
		return False,id,INVALID_TITLE
	offset = m.end()
	
	# If new, get name
	if not update:
		smallName = m.group(1).replace('\n',' ').replace('\r','')
		m = rName.search(web,offset)
		if not m:
			return False,id,NO_NAME
		name = m.group(1).replace('\n',' ').replace('\r','')
		offset = m.end()
	
	# Get Original Price (optional)
	m = rOrig.search(web,offset)
	if m:
		orig = m.group(1)
		offset = m.end()
	
	# Get Instant Savings (optional)
	m = rSavings.search(web,offset)
	if m:
		savings = m.group(1)
		offset = m.end()

	# Get Cost (Required, but can be special)
	m = rCost.search(web,offset)
	if m:
		cost = m.group(1)
		offset = m.end()
	
	# Get afterRebate (Optional)
	m = rARebate.search(web,offset)
	if m:
		aRebate = m.group(1)
		offset = m.end()
	
	# Get shipping (Optional)
	m = rShipping.search(web,offset)
	if m:
		shipping = m.group(1)
		offset = m.end()

	# Get model number (Mostly required)
	if not update:
		m = rModel.search(web,offset)
		if m:
			model = m.group(1)
	if debug:
		print 'Name:',name
		print 'SmallName:',smallName
		print 'Model:',model
		print 'Orig:',orig
		print 'Save:',savings
		print 'Cost:',cost
		print 'Arebate:',aRebate
		print 'Shipping:',shipping

	# Handle case where one must visit other page
	if not cost:
		web = openUrl('http://www.newegg.com/Product/MappingPrice.aspx?Item='+id,5)
		if not web:
			return False,id,CONNECT_FAILED
		offset = 0
		
		# Get Orig
		m = rOrig2.search(web,offset)
		if m:
			orig = m.group(1)
			offset = m.end()

		# Get Savings
		m = rSavings2.search(web,offset)
		if m:
			savings = m.group(1)
			offset = m.end()

		# Get Cost
		m = rCost2.search(web,offset)
		if not m:
			return False,id,NO_COST_PRICE
		cost = m.group(1)
		offset = m.end()

		# Get aRebate
		m = rARebate2.search(web,offset)
		if m:
			aRebate = m.group(1)

		if debug:
			print 'Orig2:',orig
			print 'Save2:',savings
			print 'Cost2:',cost
			print 'Arebate2:',aRebate

	# Update Orig if necessary
	if not orig:
		orig = cost
	
	if not update:
		return True,id,name,smallName,model,toInt(orig),toInt(savings),toInt(cost),toInt(aRebate),toInt(shipping)
	else:
		return True,id,toInt(orig),toInt(savings),toInt(cost),toInt(aRebate),toInt(shipping)


if __name__ == '__main__':
	import sys

	if sys.argv[1]:
		print parse(sys.argv[1],update=False,debug=True)
		sys.exit()

	print openUrl('http://www.newegg.com/Product/Product.aspx?Item=N82E16834220107') # -1 error
	print openUrl('http://www.newegg.com/Product/Product.aspx?Item=N82E16828104627') # -4 error
