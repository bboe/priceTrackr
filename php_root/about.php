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
<h1>About priceTrackr</h1>
<h2>Original History (2006-2007)</h2>
<p>The idea for priceTrackr was originally conceived by Bryce Boe on July 22,
  2006 while procrastinating the writing of a paper. Bryce had recently
  purchased parts for a new desktop system and thought it would have been nice
  to have a service which allows one to make more informed decisions about the
  items they're purchasing. Having a little money in pocket the domain name
  "thepricetracker.com" was registered.</p>

<p>After a few more days of procrastination, a Newegg crawler was written and
  the first data was collected for 20 items at 10:37 PM PST on July 31st from
  Bryce's home computer. The first data set did not include savings, rebates or
  shipping prices and the crawler was adapted to collect this information.
  Regular data collection began August 4, 2006.</p>

<p>Upon discussing the idea with some friends, a suggestion was made to
  register "pricetrackr.com" to mimic sites like flickr. Thus on August 7,
  2006 the domain was registered and the name was changed to "priceTrackr". The
  next day a <em>very cheap</em>, shared web host was purchased to host
  Bryce's various websites.</p>

<p>A few weeks passed by before Bryce thought priceTrackr was ready to go. The
  night of August 27, 2006 he
  <a href="http://www.bryceboe.com/2006/08/27/official-pricetrackr-launch/">
    blogged about priceTrackr</a>, though this blog posting had hardly any
  impact as very few people visited his blog at the time.</p>

<p>On September 5, 2006 Bryce thought it was time to let the world know about
  priceTrackr. Utilizing digg he
  <a href="http://www.digg.com/tech_deals/Newegg_priceTrackr">linked</a> to his
  blog posting with great skepticism. To his surprise priceTrackr reached
  digg's front page on September 6, 2006 and very shortly there after Bryce's
  web server became a victim of the digg effect. A more detailed recollection
  of this event can be read <a href="http://www.bryceboe.com/2006/09/07/a-day-with-digg-pricetrackr-was-dugg/">here</a>.</p>

<p>Within a few days caching was enabled and the digg effect subsided allowing
  priceTrackr to resume normal operation, which it did for nearly four months.
  On January 5, 2007 priceTrackr's hosting company explicitly stated that the
  update scripts (crawler) was not to run anymore, thus ending priceTrackr for
  the foreseeable future.</p>

<h2>Relevant History (2008)</h2>
<p>Though priceTrackr was lying dormant online for nostalgic purposes, not all
  of its code went unused. The Newegg crawler, written in the python
  programming language, was used as the basis for a highly distributed web
  crawler, CRAWL-E. CRAWL-E was in the data collection parts of a few research
  projects with more to come.</p>

<h2>Current History (2009+)</h2>
<p>After years of priceTrackr wanting to get priceTrackr back up and running,
  but having neither reason nor the resources to do so, Bryce finally received
  the resources and some time for making it happen. priceTrackr's Newegg
  crawler was updated to use the CRAWL-E framework and began crawling November
  15, 2009. This time around priceTrackr doesn't just crawl a few items from
  Newegg, but rather nearly 100% of Newegg's items.</p>

<p>priceTrackr was reintroduced into the wild on November XX, 2009...</p>

<h2>Contact</h2>
<p>If you have any questions or comments regarding priceTrackr please email
  them to contact __at__ pricetrackr __dot__ com. Additionally feel free to
  post comments on Bryce's relevant blog entries.</p>
<?php
require_once 'includes/footer.php';
$data = ob_get_flush();
$Cache_Lite->save($data);
}
?>
