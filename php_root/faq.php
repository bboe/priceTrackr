<?php
require_once('Cache/Lite.php');
// Set a id for this cache
$id = 'faq';

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
	$title = 'FAQ';
	require_once 'includes/header.php';
?>

<h1>Frequently Asked Questions</h1>

<ol>
  <li><a href="#0">Why create priceTrackr?</a></li>
  <li><a href="#1">How should the graphs be interpreted?</a></li>
</ol>

<div class="faq">
  <h4><a name="0"></a>Why create priceTrackr?</h4>
  <div class="answer">
    <p>priceTrackr was created so that one can make a more informed decision before purchasing items on newegg.</p>
  </div>
</div>

<div class="faq">
  <h4><a name="1"></a>How should the graphs be interpreted?</h4>
  <div class="answer">
    <p>Each graph has three sections.  The first section is the price + shipping which is the price one would pay in the absence of savings or rebates.</p>
    <p>The second section is + savings which includes the instant savings from the company.  This essentially is what you must pay to get the item.</p>
    <p>The final section is + rebate which adds in the rebate to the savings price.  This, in a sense, is the overall cost of the item once the rebate check is received.</p>
  </div>
</div>
<?php
require_once 'includes/footer.php';
$data = ob_get_flush();
$Cache_Lite->save($data);
}
?>
