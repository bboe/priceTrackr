<?php
require_once('Cache/Lite.php');
// Set a id for this cache
$id = 'contact';

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
	print "\n".'<!--priceTrackr :)-->';

} else { // No valid cache found (you have to make the page)
	ob_start();
	define('START', true);
	$title = 'Contact';
	require_once 'includes/header.php';
?>

<h1>Contact</h1>
<h2>General</h2>
<p>Is there something you would like to see on priceTrackr?  A new feature perhaps?
Please send us your ideas so that we can make priceTrackr better for you.</p>
<p><a href="/c/general">priceTrackr General Contact</a></p>
<h2>Support</h2>
<p>Are you having trouble with priceTrackr? Does some data not appear to be correct?
Please contact us with this information so we can correct any problems and to ensure
that our users are able to get the data the need.</p>
<p><a href="/c/support">priceTrackr Support Contact</a></p>
<h2>Marketing</h2>
<p>Interested in advertising for priceTrackr?  Please contact us with your proposal so that
we may consider your offer.</p>
<p><a href="/c/marketing">priceTrackr Marketing Contact</a></p>

<?php
require_once 'includes/footer.php';
$data = ob_get_flush();
$Cache_Lite->save($data);
}
?>