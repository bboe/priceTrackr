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
  <li><a href="#1">Why are there holes for some dates in the charts?</a></li>
  <li><a href="#2">How should the charts be interpreted?</a></li>
</ol>

<div class="faq">
  <h4><a name="0"></a>Why create priceTrackr?</h4>
  <div class="answer">
    <p>priceTrackr was created so that one can make a more informed decision before purchasing items on newegg.</p>
  </div>
</div>

<div class="faq">
  <h4><a name="1"></a>Why are there holes for some dates in the charts?</h4>
  <div class="answer">
    <p>Holes can appear in a chart for a few reasons. A crawl of Newegg
      may not have occurred on that date, an error may have occurred while
      crawling a specific item, or an item was placed in a deactivated state on
      Newegg. Except for in the case of a deactivated item, it should be pretty
      easy to extrapolate what the prices on the missing dates were.</p>
  </div>
</div>

<div class="faq">
  <h4><a name="2"></a>How should the charts be interpreted?</h4>
  <div class="answer">
    <p>Each chart has four lines.  The first line, "original", is the price one
      of the item in the absence of savings, rebates and shipping. The second
      line, "+ savings", is the price after Newegg's instant savings on the
      item. This is the cost to purchase the item, when not considering the
      cost of shipping. The third line, "+ rebates", is the previous price with
      any rebates also added on. The final line, "original + shipping", allows
      one to track the variance in shipping over time with respect to the
      original price.</p>
    <p>The best way to look at the specific pieces is to compare them to the
      other lines. When "+ savings" differs from the original, then at that
      point in time there was savings on the item. Likewise when "+ rebates"
      differs from "+ savings" there was rebates on the item.</p>
    <p>The reason for comparing the shipping to the original price, rather than
      to tack on after the rebates price is that the original price varries
      much less than the rebates price, therefore it is simpler to monitor
      variations in the shipping price as is.</p>
  </div>
</div>
<?php
require_once 'includes/footer.php';
$data = ob_get_flush();
$Cache_Lite->save($data);
}
?>
