<?php
require_once('Cache/Lite.php');
// Set a id for this cache
$id = 'about';

// Set a few options
$options = array(
'cacheDir' => '/tmp/',
'lifeTime' => 3600
);

// Create a Cache_Lite object
$Cache_Lite = new Cache_Lite($options);

// Test if thereis a valide cache for this id
if ($data = $Cache_Lite->get($id)) {
	print $data;
} else { // No valid cache found (you have to make the page)
	ob_start();
	define('START', true);
	$title = 'About';
	require_once 'includes/header.php';
?>

<h1>About</h1>
<p>priceTrackr unofficially began 10:37 PM PST July 31, 2006 when priceTrackr first collected data from newegg.
The original data set contained 20 items compared to over 350 items currently tracked.  priceTrackr was
created to give consumers the product pricing history so that they can better determine when the
appropriate time to purchase an item is.</p>
<h2>History</h2>
<p>The idea of priceTrackr came about July 22, 2006 while procrastinating the writing of a paper, and
after recently purchasing parts for a new desktop system. 
priceTrackr first collected data, for 20 items, 10:37 PM PST July 31st on a home computer.
The first set of data did not include savings, rebates or shipping and priceTrackr was quickly adapted to do so.
priceTrackr was originally named thepricetracker until it was suggested that priceTrackr would be better.
</p>
<p>The initial launch of priceTrackr was delayed nearly a month after the original launch date as it was
not deemed ready for the public. priceTrackr officially opened to the public Monday August 28, 2006.</p>
<h2>Creator</h2>
<p>priceTrackr is the sole idea of Bryce Boe who is currently a Computer Science student at the University
of California in Santa Barbara. Bryce has purchased the majority of his computer equipment through newegg
as their selection and speed of delivery cannot be matched.  Bryce hopes that through priceTrackr others
may benefit by seeing trends in newegg's pricing and thus purchase items when they deem most appropriate.</p>
<p>To learn more about the creator of priceTrackr please visit <a href="http://www.bryceboe.com">BryceBoe.com.</a></p>

<?php
require_once 'includes/footer.php';
$data = ob_get_flush();
$Cache_Lite->save($data);
}
?>