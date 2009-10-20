<?php
require_once('Cache/Lite.php');
// Set a id for this cache
$id = 'recent';

// Set a few options
$options = array(
'cacheDir' => '/tmp/',
'lifeTime' => 1
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
	define('BIG_ADS', true);
	$title = 'Daily Drops';
	require_once 'includes/header.php';
?>

<h1>Daily Drops</h1>

<?php
   //dailyDrops();
require_once 'includes/footer.php';
$data = ob_get_flush();
$Cache_Lite->save($data);
}

function dailyDrops() {
	global $db;
	$result = $db->query('SELECT small_name,id,current_price,price_change from item where price_change < -900 and date_Sub(now(),interval 1 day) < date_updated order by price_change limit 50');
	if (count($result) == 0) {
		print '<p class="mesg">Sorry there have been no significant drops within the last 24 hours.</p>';
		print '<h3>Last 30 changes</h3>';
		$result = $db->query('SELECT date_updated,small_name,id,current_price,price_change from item where price_change != 0 order by date_updated desc limit 30');
		print '<div class="results"><ol>';
		foreach ($result as $value) {
			print '<li><a href="/i/'.$value['id'].'/">'.$value['small_name'].'</a><br />';
			print 'Date: '.substr($value['date_updated'],0,-9).' ';
			if ($value['price_change'] > 0) print 'Increase: <span class="max">';
			else print 'Drop: <span class="min">';
			print intToDollar($value['price_change']).'</span> ';
			print 'Cost: <span class="price">'.intToDollar($value['current_price']).'</span>';
			print '</li>';
		}
		print '</ol></div>';
	}
	
	else {
		print '<div class="results"><ol>';
		foreach ($result as $value) {
			print '<li><a href="/i/'.$value['id'].'/">'.$value['small_name'].'</a><br />';
			print 'Drop: <span class="price">'.intToDollar($value['price_change']).'</span> ';
			print 'Cost: <span class="price">'.intToDollar($value['current_price']).'</span></li>';
		}
		print '</ol></div>';
	}
}
?>