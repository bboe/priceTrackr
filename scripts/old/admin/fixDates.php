<?php
define('START', true);
require_once '../includes/pearDB.php';
require_once 'updateFunctions.php';

$db = new pearDB();

$result = $db->query('select id from item order by id');

$count = 0;
foreach ($result as $value) {
	$dates = $db->query('select date,cost,aRebate,shipping from tracker where itemID = ? order by date',$value['id']);
	if (empty($dates)) {
		print "bad: {$value['id']}<br/>\n";
		continue;
	}
	$firstDate = $dates[0]['date'];
	$last = end($dates);
	$lastDate = $last['date'];
	if (sizeof($dates) > 1) {
		$last = array_pop($dates);
		$prev = array_pop($dates);
		
		$lastCost = getActualCost($last);
		$prevCost = getActualCost($prev);
		
		$change = $lastCost-$prevCost;

		$db->query('update item set dateAdded = ?, dateUpdated = ?, priceChange = ? where id = ?',array($firstDate,$lastDate,$change,$value['id']));
	}
}
?>