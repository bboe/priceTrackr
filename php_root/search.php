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
  if ($len == 0) print '<p class="mesg">No search terms entered.</p>';
  else if ($len > 100) print '<p class="mesg">Search string too long.</p>';
  else {
    $terms = '';
    foreach (split(' ', $q) as $i) {
      if (strlen($i) < 2) $terms .= " '$i'";
    }
    if ($terms != '') print '<p class="mesg">The following terms have been ignored:'. $terms . '</p>';
    $result = $db->prepare_execute('select newegg_id, title, match(title, model) against (? in boolean mode) as score from item where match(title, model) against (? in boolean mode) order by score desc limit 30', array($q, $q), array('text', 'text'), true, false);
    $time = microtime(true)-$start;
    print '<p class="searchTime">'. $time . ' seconds</p>';
    print '<p class="query">Query:<i>'.$q.'</i></p>';
    $size = sizeof($result);
    if ($size == 0) {
      print '<p>No results found. Please <a href="/contact/">contact us</a> if you believe priceTrackr is missing something.</p>';
    }
    else if ($size == 1) {
      header('Location: /i/'.$result[0]['newegg_id'].'/');
      exit();
    }
    else {
      print '<div class="results"><ol>';
      foreach ($result as $value) {
	print '<li><a href="/i/'.$value['newegg_id'].'/">'.$value['title'].'</a></span></li>'."\n";
      }
      print '</ol></div>';
    }
  }
 }
ob_end_flush();
?>
<?php require_once 'includes/footer.php';?>
