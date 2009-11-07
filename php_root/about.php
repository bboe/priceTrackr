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

<h2>Original History (2006-2007)</h2>
<p>The idea for priceTrackr was originally conceived by Bryce Boe July 22,
  2006 while procrastinating the writing of a paper. Bryce had recently
  purchased parts for a new desktop system and thought it would have been nice
  to have a service which allows one to make more informed decisions about the
  items they're purchasing. Having a little money in pocket the domain name
  "thepricetracker.com" was registered.</p>

<p>After a few more days of procrastination a newegg crawler was written and
  the first data was collected for 20 items at 10:37 PM PST on July 31st from
  Bryce's home computer. The first data set did not include savings,rebates or
  shipping prices and the crawler was adapted to collect this information.
  Regular data collection began August 4, 2006.</p>

<p>Upon discussing the idea with some friends, a suggestion was made to
  register "pricetrackr.com" to mimic sites like flickr. Thus on August 7,
  2006 the domain was registered and the name was changed to "priceTrackr". The
  next day a <em>very cheap</em> shared web host was purchased to host
  Bryce's various websites.</p>

<p>A few weeks passed by before Bryce thought priceTrackr was ready to go. The
  night of August 27, 2006 Bryce
  <a href="http://www.bryceboe.com/2006/08/27/official-pricetrackr-launch/">
    blogged about priceTrackr</a>, though this blog posting had hardly any
  impact as very few people visited Bryce's blog at the time.</p>

<p>On September 5, 2006 Bryce thought it was time to let the world know about
  priceTrackr. Utilizing digg he
  <a href="http://www.digg.com/tech_deals/Newegg_priceTrackr">linked</a> to his
  blog posting with great skepticsm. To his surprise priceTrackr reached digg's
  front page on September 6, 2006 and very shortly there after Bryce's
  webserver became a victim of the digg effect. A more detailed recollection
  of this event can be read <a href="http://www.bryceboe.com/2006/09/07/a-day-with-digg-pricetrackr-was-dugg/">here</a>.</p>

<p>Within a few days caching was enabled and the digg effect subsided allowing
  priceTrackr to resume normal operation, which it did for nearly four months.
  On January 5, 2007 priceTrackr's hosting company explicitly stated that the
  update scripts (crawler) was not to run anymore, thus ending priceTrackr for
  the foreseable future.</p>

<h2>Creator</h2>
<p>priceTrackr is the sole idea of Bryce Boe who is currently a Computer
  Science student at the University of California in Santa Barbara. Bryce has
  purchased the majority of his computer equipment through newegg as their
  selection and speed of delivery cannot be matched.  Bryce hopes that through
  priceTrackr others may benefit by seeing trends in newegg's pricing and thus
  purchase items when they deem most appropriate.</p>

<p>To learn more about the creator of priceTrackr please visit
  <a href="http://www.bryceboe.com">BryceBoe.com.</a></p>
<?php
require_once 'includes/footer.php';
$data = ob_get_flush();
$Cache_Lite->save($data);
}
?>
