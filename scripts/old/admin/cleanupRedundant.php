<?php
define('START', true);
require_once '../includes/pearDB.php';

$db = new pearDB();

$result = $db->query('select id from item order by id');

$count = 0;
foreach ($result as $value) {
	$prices = $db->query('select date,orig,cost,aRebate,shipping from tracker where itemID = ? order by date',$value['id']);
	if (empty($prices)) continue;
	$orig = -1;
	$cost = -1;
	$aRebate = -1;
	$shipping = -1;
	foreach ($prices as $item) {
		if ($orig == $item['orig'] && $cost == $item['cost'] && $aRebate == $item['aRebate'] && $shipping == $item['shipping']) {
			$count++;
			print "Delete {$value['id']}<br/>\n";
			$db->query('delete from tracker where itemID = ? and date = ?',array($value['id'],$item['date']));
		}
		else {
			$orig = $item['orig'];
			$cost = $item['cost'];
			$aRebate = $item['aRebate'];
			$shipping = $item['shipping'];
		}
	}
}
print "Deleted $count rows";





?>