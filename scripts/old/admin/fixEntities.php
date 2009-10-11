<?php
define('START', true);
require_once '../includes/pearDB.php';

$db = new pearDB();

$result = $db->query('select id,smallName from item where smallName like ?','%&%');

$count = 0;
foreach ($result as $value) {
	$db->query('update item set smallName = ? where id = ?',array(replaceChars($value['smallName']),$value['id']));
	print "{$value['smallName']}<br/>\n";
	$count++;
}
print "Updated $count rows";

$result = $db->query('select id,name from item where name like ?','%&%');

$count = 0;
foreach ($result as $value) {
	$db->query('update item set name = ? where id = ?',array(replaceChars($value['name']),$value['id']));
	print "{$value['name']}<br/>\n";
	$count++;
}
print "Updated $count rows";

$result = $db->query('select id,modelNum from item where modelNum like ?','%&%');

$count = 0;
foreach ($result as $value) {
	$db->query('update item set modelNum = ? where id = ?',array(replaceChars($value['modelNum']),$value['id']));
	print "{$value['modelNum']}<br/>\n";
	$count++;
}
print "Updated $count rows";


function replaceChars($text) {
	return htmlentities(html_entity_decode(html_entity_decode($text)));
}


?>