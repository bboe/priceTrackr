<?php
if (!isset($_GET['feed'])) {
	header('Location: /');
	exit();
}
$feed = $_GET['feed'];
$feeds = array('dailyDrops');
if (!in_array($feed,$feeds)) {
	header('Location: /');
	exit();
}

header('Content-type: text/xml');

require_once('Cache/Lite.php');
$id = 'rss-'.$feed;

$options = array(
'cacheDir' => '/tmp/',
'lifeTime' => 3600
);

$Cache_Lite = new Cache_Lite($options);

if ($data = $Cache_Lite->get($id)) {
	print $data;
	print "\n".'<!--priceTrackr :)-->';

} else { // No valid cache found (you have to make the page)
	define('START', true);
	require_once 'includes/error.php';
	require_once 'includes/myDB.php';
	require_once 'includes/functions.php';
	$db = new myDB();
	$result = $db->query('SELECT id,small_name,name,current_price,price_change,unix_timestamp(date_updated) as timestamp from item where price_change < -900 and date_sub(now(),interval 1 day) < date_updated order by date_updated desc limit 100');
	$db->free();
	ob_start();
	print '<?xml version="1.0" encoding="iso-8859-1" ?>'."\n";
?>
<rss version="2.0">

	<channel>
		<title>priceTrackr Daily Drops</title>
		<link>http://www.pricetrackr.com/daily/</link>
		<description>Official priceTrackr RSS Feed. Lists items with a significant drop in prices. The prices shown include shipping, rebates, and savings.</description>
		<language>en-us</language>
		<lastBuildDate><?php echo date('D, d M Y H:i:s T'); ?></lastBuildDate>
		<ttl>60</ttl>
		
<?php

foreach ($result as $value) {
	print "\t\t\t".'<item>'."\n";
	print "\t\t\t\t".'<title>'. intToDollar($value['current_price']) . ' (-'.intToDollar($value['price_change']).') - ' . tFix($value['small_name']).'</title>'."\n";
	print "\t\t\t\t".'<link>http://www.pricetrackr.com/i/'.$value['id'].'/</link>'."\n";
	print "\t\t\t\t".'<description>&lt;p&gt;&lt;b&gt;'.tFix($value['name']).'&lt;/b&gt;&lt;/p&gt;';
	print "\t\t\t\t".'&lt;p&gt;Current Price: ' . intToDollar($value['current_price']) . '&lt;/p&gt;';
	print "\t\t\t\t".'&lt;p&gt;Price Drop: &lt;b&gt;' . intToDollar($value['price_change']) . '&lt;/b&gt;&lt;/p&gt;';
	print "\t\t\t\t".'&lt;p&gt;Percent Drop: ' . dropPercent($value['current_price'],$value['price_change']) . '&lt;/p&gt;';
	print "\t\t\t\t".'</description>'."\n";
	print "\t\t\t\t".'<pubDate>'.date('D, d M Y H:i:s T',$value['timestamp']).'</pubDate>'."\n";
	print "\t\t\t\t".'<guid>http://www.pricetrackr.com/i/'.$value['id'].'/;'.$value['timestamp'].'</guid>'."\n";
	print "\t\t\t".'</item>'."\n";
}
?>
		<copyright>Copyright (c) 2006 priceTrackr. All Rights Reserved.</copyright>
	</channel>
	
</rss>
<?php
$data = ob_get_flush();
$Cache_Lite->save($data);
}

function tFix($text) {
	$text = html_entity_decode($text);
	return str_replace('&','&#x26;',$text);
}
?>