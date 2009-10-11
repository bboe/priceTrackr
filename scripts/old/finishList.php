#!/usr/bin/php
<?php

// Copyright 2006 Bryce Boe

ini_set('include_path',ini_get('include_path').':/usr/local/lib/php/:../includes/:');
error_reporting(E_ALL);

define('START', true);
require_once 'pearDB.php';
require_once 'parseXML.php';
require_once 'updateFunctions.php';

foreach ($argv as $arg) {
	if ($arg == '-u') {
		define('UPDATE',true);
	}
}
if (!defined('UPDATE')) define('UPDATE',false);

$db = new pearDB();

$count = 0;

while(!feof(STDIN)) {
	$line = fgets(STDIN);
	$a = explode("\t",$line);

	if (sizeof($a) == 1) continue;
	$id = $a[1];
	if ($a[0] == 'False') {
		switch ($a[2]) {
			case -1:	// Network Error
			fwrite(STDERR,'Network Error: '.$id."\n");
			break;
			case -2:	// Title Error
			fwrite(STDERR,'Title Error: '.$id."\n");
			if (UPDATE) {	// Increment flag if item is not new and error
				$db->query('update item set dateUpdated = now(), flag = flag+1 where id = ?',$id);
			}
			else {	// Delete item if it's new and error
				$db->query('update item set dateUpdated = now(), flag = 127, deleted = 1 where id = ?',$id);
			}
			break;
			case -3:	// Name Error
			fwrite(STDERR,'Name Error: '.$id."\n");
			break;
			case -4:	// Cost Error
			fwrite(STDERR,'Cost Error: '.$id."\n");
			break;
		}
	}
	else {
		if (UPDATE) { // Old Item
			$currInfo['id'] = $a[1];
			$currInfo['orig'] = $a[2];
			$currInfo['savings'] = $a[3];
			$currInfo['cost'] = $a[4];
			$currInfo['aRebate'] = $a[5];
			$currInfo['shipping'] = $a[6];

			$prevInfo = $db->query('select orig,cost,aRebate,shipping from tracker where tracker.itemID = ? order by date desc limit 1',$id);
			$prevInfo = $prevInfo[0];

			if (doUpdate($currInfo,$prevInfo)) {
				$prevCost = getActualCost($prevInfo);
				if (addTracker($db,$currInfo,$prevCost)) {
					print 'http://www.newegg.com/Product/Product.asp?Item=' . $id . "\n";
				}
			}
		}
		else { // New Item
			$name = replaceChars($a[2]);
			$shortName = replaceChars($a[3]);
			$model = replaceChars($a[4]);
			$currInfo['id'] = $a[1];
			$currInfo['orig'] = $a[5];
			$currInfo['savings'] = $a[6];
			$currInfo['cost'] = $a[7];
			$currInfo['aRebate'] = $a[8];
			$currInfo['shipping'] = $a[9];

			$db->query('update item set smallName = ?, name = ?, modelNum = ?, flag = 0 where id = ?',array($shortName,$name,$model,$id));
			if (addTracker($db,$currInfo))
				print 'Added http://www.newegg.com/Product/Product.asp?Item=' . $id . "\n";
		}
	}
}
$db->unpearDB();
?>