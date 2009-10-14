<?php
require_once('Cache/Lite.php');
// Set a id for this cache
$id = 'index';

// Set a few options
$options = array(
'cacheDir' => '/tmp/',
'lifeTime' => 300
);

// Create a Cache_Lite object
$Cache_Lite = new Cache_Lite($options);

// Test if thereis a valide cache for this id
if ($data = $Cache_Lite->get($id)) {
	print $data;
	print "\n".'<!--priceTrackr :)-->';

} else { // No valid cache found (you have to make the page)
	ob_start();
	define('START', true);
	$title = 'Home';
	require_once 'includes/header.php';
?>

<h1>Welcome to priceTrackr</h1>
<p>priceTrackr will give you the price history of specific items with the following factors included:</p>
<ul>
<li>Original Price</li>
<li>Store discount</li>
<li>Rebate discount</li>
<li>Shipping price</li>
</ul>
<p>Using all of these we calculate the out the door price on items on a day by day basis.
</p>
<p>At this time it is only possible to find items through the search.  A browse by category section will be added soon.</p>
<p>If you can't find an item that you would like tracked please <a href="/add.php">add it</a>.</p>
<h2>priceTrackr News</h2>
<p>2009-10-15 - priceTrackr is back!</p>
<p>2007-01-21 - So priceTrackr probably wont be coming back up as I cannot afford a dedicated server and the tracking scripts "utilize too many resources" which is complete BS. As the whole purpose of this website was to aid in making purchases I offer the following link. <a href="http://labs.anandtech.com/">labs.anandtech.com</a>.</p>
<p>2007-01-06 - As some of you may have noticed priceTrackr was down for roughly a day due to my update scripts running and as I was told utilizing too much of the server's resources. Anyways this means my update scripts are not currently running, though I should have a work around for this current situation soon.
<h2>Latest Updates</h2>

<?php
recentAdded();

require_once 'includes/footer.php';
$data = ob_get_flush();
$Cache_Lite->save($data);
}

function recentAdded() {
	global $db;
	$result = $db->query('SELECT small_name,id,current_price from item,tracker where tracker.item_id = id order by date desc limit 10');
	$count = 0;
	print '<div class="results"><ol>';
	foreach ($result as $value) {
		print '<li><a href="/i/'.$value['id'].'/">'.$value['small_name'].'</a> - <span class="price">'.intToDollar($value['current_price']).'</span></li>';
		$count++;
	}
	print '</ol></div>';
}
?>
