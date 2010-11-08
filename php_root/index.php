<?php
require_once('Cache/Lite.php');
// Set a id for this cache
$id = 'index';

// Set a few options
$options = array(
'cacheDir' => '/tmp/',
'lifeTime' => 60*60*24
);

// Create a Cache_Lite object
$Cache_Lite = new Cache_Lite($options);

// Test if thereis a valide cache for this id
if ($data = $Cache_Lite->get($id)) {
	print $data;
} else { // No valid cache found (you have to make the page)
	ob_start();
	define('START', true);
	$title = 'Home';
	require_once 'includes/header.php';
?>

<h1>Track your newegg products' price history!</h1>
<p>priceTrackr regularly crawls newegg to get updated prices for many of your
favorite newegg items. Use priceTrackr Look up the price history for an item
you are interested in purchasing on newegg. priceTrackr will help to inform you
if <em>now</em is a good time to purchase the item, or conversely, priceTrackr can show you that the item is currently at the highest price it's been.</p>
<p>See the examples below to get familiar with priceTrackr:</p>

<ul>
  <li><a href="/i/N82E16819115214/">N82E16819115214: Intel Core i7-860</a></li>
  <li><a href="/i/N82E16820227461/">N82E16820227461: OCZSSD2-1AGT60G</a></li>
  <li><a href="/i/N82E16814150447/">N82E16814150447: XFX HD-577A-ZNFC</a></li>
</ul>

<h2>What is priceTrackr?</h2>

<p>priceTrackr is a service which tracks nearly 100% of Newegg's items over
  time and presents each item's price on a timeline with a line for each of
  the following:</p>
<dl>
  <dt>Original price</dt>
  <dd>- The base price of the item.</dd>
  <dt>Instant savings price</dt>
  <dd>- The original price of the item with instant savings subtracted.</dd>
  <dt>Rebate savings price</dt>
  <dd>- The original price of the item with both the instant savings and
    rebate savings subtracted.</dd>
  <dt>Shipping price</dt>
  <dd>- The original price of the item, plus the cost to ship that item to zip
    code 93117 (Goleta, CA).</dd>
</dl>

<h3>How do I use this site?</h3>
<p>At present the only way to navigate this site is through search. Ideally you
  will know exactly what you're searching for after having navigated through
  Newegg to find it. You can search for anything within the title of the item,
  or by entering the Newegg product id directly into the search field you can
  go directly to the priceTrackr page for that item.</p>

<p>Finding the Newegg product id is as simple as copying part of the Newegg url
  when looking at a particular item. If you are on the product page for
  "Crucial 6GB (3 x 2GB) 240-Pin DDR3 SDRAM DDR3 1066 (PC3 8500) Triple
  Channel Kit Desktop Memory", then the url in the browser will be:</p>
<p style="margin-left:50px">
  http://www.newegg.com/Product/Product.asp?Item=<span class="min"
							>N82E16820148246</span>
</p>
<p>That last part colored in blue is the Newegg product id. Copying and
  pasting <span class="min">N82E16820148246</span> into the search box will
  take you directly to the product's page. Give it a try.</p>

<h3>priceTrackr News</h3>
<p>2009-10-15 - priceTrackr is back after two years of inactivity.</p>
<?php
require_once 'includes/footer.php';
$data = ob_get_flush();
$Cache_Lite->save($data);
}
?>
