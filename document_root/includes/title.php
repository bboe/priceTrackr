<?php
if(!(defined('START') && START)) exit('Not A Valid Entry Point');

if (isset($_GET['item']) && $_GET['item'] != '') {
	$id = $_GET['item'];
	$result = $db->prepare_execute('select small_name,name,model_num,date(tracker.date) as s_date,tracker.orig,tracker.savings,tracker.cost,tracker.after_rebate,tracker.shipping from item,tracker where tracker.item_id = id and id = ? order by date',$id,'text',true,false);
	if (isset($result[0])) print $result[0]['small_name'];
	else {
	  $result = $db->prepare_execute('select name from item where id = ?',$id,'text',true,false);
		if (isset($result[0])) print 'New Item';
		else {
			print 'Invalid Item';
			unset($_GET);	
		}
		
	}
}
elseif (isset($title)) print $title;
else print '';
?>