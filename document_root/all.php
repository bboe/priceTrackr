<?php
define('START', true);
require_once 'includes/header.php';

$result = $db->query('select name,id from item where deleted = 0 order by name');
$id = -1;
$total = -1;
print '<ol>';
foreach ($result as $value) {
	if ($id != $value['id']) {
		if ($id != -1) print '</ol>'."\n";
		print '<li><a href="/i/'.$value['id'].'/">'.$value['name'].'</a></li>';
	}
}
print '</ol>';

require_once 'includes/footer.php';
?>
