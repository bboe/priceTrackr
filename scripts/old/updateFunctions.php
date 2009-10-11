<?php
if(!(defined('START') && START)) die('Not A Valid Entry Point');

/*
 * This function updates the item in the database
 * and adds the tracking data.
 */
function addTracker(&$db,&$info,&$old=null) {
	$curr = getActualCost($info);
	if (is_null($old)) {
		if ($db->query('update item set dateUpdated = now(), currPrice = ?, flag = 0 where id = ?',array($curr,$info['id']))
		&& $db->query('insert into tracker values(?,now(),?,?,?,?,?)',array($info['id'],$info['orig'],$info['savings'],$info['cost'],$info['aRebate'],$info['shipping'])))
		return true;
		else return false;
	}
	else {
		if ($db->query('update item set dateUpdated = now(), currPrice = ?, priceChange = ?, flag = 0 where id = ?',array($curr,$curr-$old,$info['id']))
		&& $db->query('insert into tracker values(?,now(),?,?,?,?,?)',array($info['id'],$info['orig'],$info['savings'],$info['cost'],$info['aRebate'],$info['shipping'])))
		return true;
		else return false;
	}
}

/*
 * This function calculates the out the door cost.
 */
function getActualCost(&$price) {
	if ($price['aRebate'] != 0) $toReturn = $price['aRebate'];
	else $toReturn = $price['cost'];
	return $toReturn + $price['shipping'];
}

/*
 * This function returns true if the old
 * data is different from the new data.
 */
function doUpdate(&$a,&$b) {
	if ($a['orig'] != $b['orig'] || $a['cost'] != $b['cost'] || $a['aRebate'] != $b['aRebate'] || $a['shipping'] != $b['shipping']) return true;
	return false;
}

/*
 * This function normalizes odd characters.
 */
function replaceChars($text) {
	return htmlentities(html_entity_decode(strip_tags($text)));
}
?>