<?php
define('START', true);
require_once 'includes/header.php';

$result = $db->query('select title, newegg_id from item where date_deleted is NULL order by title limit 100');
print '<ol>';
foreach ($result as $value) {
  print '<li><a href="/i/'.$value['newegg_id'].'/">'.$value['title'].'</a></li>';
}
print '</ol>';

require_once 'includes/footer.php';
?>
