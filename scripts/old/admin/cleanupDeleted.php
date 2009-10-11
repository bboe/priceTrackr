<?php
define('START', true);
require_once '../includes/pearDB.php';

$db = new pearDB();

$result = $db->query('select id from item where deleted = 1 order by id');

$count = 0;
foreach ($result as $value) {
	$db->query('delete from tracker where itemID = ?',$value['id']);
	$db->query('delete from item where id = ?',$value['id']);
	$count++;
}
print "Deleted $count items";





?>