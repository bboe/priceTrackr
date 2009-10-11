<?php
define('START', true);
require_once '../includes/pearDB.php';

$db = new pearDB();

$result = $db->query('select id from item order by id');

foreach ($result as $value) {
	$cost = $db->query('select cost,aRebate,shipping from tracker where itemID = ? order by date desc limit 1',$value['id']);
	if (empty($cost)) {
		print "bad: {$value['id']}<br/>\n";
		continue;
	}
	$cost = $cost[0];
	if ($cost['aRebate'] != 0) $curr = $cost['aRebate'];
	else $curr = $cost['cost'];
	$curr += $cost['shipping'];
	$db->query('update item set currPrice = ? where id = ?',array($curr,$value['id']));
}
?>