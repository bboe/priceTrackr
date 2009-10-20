<?php
if(!(defined('START') && START)) exit('Not A Valid Entry Point');

if (isset($_GET['item']) && $_GET['item'] != '') {
  $id = id_to_num($_GET['item']);
  print $id;
  if (!$id) {
    print 'Invalid Item';
    unset($_GET);
    break;
  }
  $result = $db->prepare_execute('select title, model, date(item_history.date_added) as update_date, item_history.original, item_history.price, item_history.rebate, item_history.shipping from item, item_history where item_history.id = item.id and item.id = ? order by update_date', $id, 'text', true, false);
  if (isset($result[0])) print $result[0]['title'];
  else {
    print 'Invalid Item';
    unset($_GET);	
  }
}
elseif (isset($title)) print $title;
else print '';
?>