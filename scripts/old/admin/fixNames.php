<?php
define('START', true);
require_once '../includes/pearDB.php';

if (isset($argv) && $argv[1] == '-u') $update = true;
else $update = false;

$db = new pearDB();

$result = $db->query('select id from item where smallName = ""');
print '<br/>Updating names, model num<br/>'."\n";
foreach ($result as $value) {
	set_time_limit(60);
	$info = process($value['id'],true);
	if (!isset($info['name'])) continue;
	$db->query('update item set smallName = ?, name = ?, modelNum = ?, flag = 0 where id = ?',array(replaceChars($info['smallName']),replaceChars($info['name']),replaceChars($info['model']),$value['id']));
}

$db->unpearDB();

print '<p>done</p>';

?>