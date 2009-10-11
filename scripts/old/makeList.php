#!/usr/bin/php
<?php

// Copyright 2006 Bryce Boe

ini_set('include_path',ini_get('include_path').':/usr/local/lib/php/:../includes/:');
define('START', true);
require_once 'pearDB.php';
require_once 'parseXML.php';

foreach ($argv as $arg) {
	if ($arg == '-u') {
		define('UPDATE',true);
	}
}
if (!defined('UPDATE')) define('UPDATE',false);

$db = new pearDB();

$db->query('update item set deleted = 1, flag = 127 where flag > 120');

if (UPDATE) {
	$result = $db->query('select id from item where deleted = 0 and flag > -1 and flag <= 120 order by dateUpdated');
	foreach ($result as $value) print $value['id']."\n";
}

if (!UPDATE) {
	$deals = getDeals();
	foreach ($deals as $value) {
		$db->query('insert into item (id,dateAdded,flag) values(?,now(),-1)',$value,true);
	}
	$result = $db->query('select id from item where flag = -1');
	foreach ($result as $value) print $value['id']."\n";
}
$db->unpearDB();
?>