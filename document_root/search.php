<?php
ob_start();
define('START', true);
$title = 'Search';
require_once 'includes/header.php';
?>

<h1>Search Results</h1>

<?php
$start = microtime(true);
if (isset($_GET['q'])) {
  $q = trim($_GET['q']);
  $len = strlen($q);
  if ($len == 0) print '<p class="error">No search terms entered.</p>';
  else if ($len < 3) print '<p class="error">Search string too short.</p>';
  else if ($len > 100) print '<p class="error">Search string too long.</p>';
  else {
	  $result = $db->prepare_execute('select id,small_name,current_price, match(id,model_num,small_name,name) against (? in boolean mode) as score from item where match(id,model_num,small_name,name) against (? in boolean mode) and flag >= 0 order by score desc',array($q,$q),array('text','text'),true,false);
	  $time = microtime(true)-$start;
	  print '<p class="searchTime">'. $time . ' seconds</p>';
	  print '<p class="query">Query:<i>'.$q.'</i></p>';
	  $size = sizeof($result);
	  if ($size == 0) {
	    print '<p>No results found. Please contact us if you believe priceTrackr is missing something.</p>';
	  }
	  else if ($size == 1) {
	    header('Location: /i/'.$result[0]['id'].'/');
	    exit();
	  }
	  else {
	    print '<div class="results"><ol>';
	    foreach ($result as $value) {
	      print '<li><a href="/i/'.$value['id'].'/">'.$value['small_name'].'</a> - <span class="price">'.intToDollar($value['current_price']).'</span></li>'."\n";
	    }
	    print '</ol></div>';
	  }
  }
 }
ob_end_flush();
?>
<?php require_once 'includes/footer.php';?>
