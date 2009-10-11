<?php
require_once('Cache/Lite.php');

if(!isset($_GET['item'])) {
	header('Location: /');
	exit();
}

// Set a id for this cache
$cacheID = 'graph-'.$_GET['item'];

// Set a few options
$options = array(
'cacheDir' => '/tmp/',
'lifeTime' => 1800
);

// Create a Cache_Lite object
$Cache_Lite = new Cache_Lite($options);

// Test if thereis a valide cache for this id
if ($data = $Cache_Lite->get($cacheID)) {
	print $data;
} else { // No valid cache found (you have to make the page)
	ob_start();
	define('START', true);
	require_once 'myDB.php';
	require_once 'chart/charts.php';

	$id = $_GET['item'];

	$db = new myDB();

	$oneMonth = date('Y-m-d',strtotime('-1 month'));
	$result = $db->prepare_execute('select date(date_added) as date from item where id = ?',$id,'text',true,false);
	$dateAdded = $result[0]['date'];

	if ($oneMonth < $dateAdded) {
		$result =& oneMonthQuery($db,$id);
		$skip = 5;
	}
	else {
		$result =& allTimeQuery($db,$id);
		$skip = ceil((time() - strtotime($dateAdded))/86400/12);
	}
	$db->free();

	/*
	* Begin Chart Definition
	*/
	$chart = buildData($result);
	$chart['license'] = 'K1XUXQVMDNCL.NS5T4Q79KLYCK07EK';
	$chart['chart_type'] = 'Line';
	$chart['chart_value'] = array('prefix'=>'$','decimals'=>2,'separator'=>',','position'=>'cursor','size'=>14,'color'=>'000000','background_color'=>'FFD991','alpha'=>90);
	$chart['chart_pref'] = array('line_thickness'=>2,'point_shape'=>'none');
	$chart['chart_transition'] = array('type'=>'scale','delay'=>0,'duration'=>1,'order'=>'series');
	$chart['legend_rect'] = array ('x'=>5,'y'=>5,'width'=>490);
	$chart['legend_transition'] = array('type'=>'slide_right','delay'=>0,'duration'=>1);
	$chart['axis_category'] = array('skip'=>$skip);
	$chart['axis_value']['steps'] = 5;
	$chart['axis_value']['prefix'] = '$';
	$chart['series_color'] = array('FFCF75','AA5C4E','4E85AA');
	$chart['series_explode'] = array(250,175,100);

	SendChartData ( $chart );

	$data = ob_get_flush();
	$Cache_Lite->save($data);

}

function allTimeQuery(&$db,$id) {
  $result = $db->prepare_execute('select date(date) as date,orig,cost,after_rebate,shipping from tracker where item_id = ? order by date',$id,'text',true,false);
  return $result;
}

function oneMonthQuery(&$db,$id) {
  $result = $db->prepare_execute('select date(date) as date,orig,cost,after_rebate,shipping from tracker where item_id = ? and date > date_sub(now(),interval 1 month) order by date',$id,'text',true,false);
  $result2 = $db->prepare_execute('select orig,cost,after_rebate,shipping from tracker where itemID = ? and date < date_sub(now(),interval 1 month) order by date desc limit 1',$id,'text',true,false);
	$result['begin'] = date('Y-m-d',strtotime('-1 month'));
	if (sizeof($result2)) {
		$result['orig'] = $result2[0]['orig'];
		$result['cost'] = $result2[0]['cost'];
		$result['after_rebate'] = $result2[0]['after_rebate'];
		$result['shipping'] = $result2[0]['shipping'];
	}
	return $result;
}

function buildData($info) {
	define('ONE_DAY',60*60*24);

	// Set the start and end points
	if (isset($info['begin'])) {
		$currDate = strtotime($info['begin']);
		unset($info['begin']);
	}
	else $currDate = strtotime($info[0]['date']);
	$endDate = time();

	// Get starting prices
	if (isset($info['orig'])) {
		$cPrice = ($info['orig']+$info['shipping'])/100.;
		$cSavings = ($info['cost']+$info['shipping'])/100.;
		if ($info['after_rebate'] != 0) $cRebate = ($info['after_rebate']+$info['shipping'])/100.;
		else $cRebate = $cSavings;
		$max = $cPrice;
		$min = $cRebate;
		unset($info['orig']);
		unset($info['cost']);
		unset($info['after_rebate']);
		unset($info['shipping']);
	}
	else {
		$cPrice = $cSavings = $cRebate = null;
		$max = 0;
		$min = 0x7FFF;
	}

	$index = 0;

	// Create chart titles
	$toReturn['chart_data'][0][0] = '';
	$toReturn['chart_data'][1][0] = 'cost + shipping';
	$toReturn['chart_data'][2][0] = '+ savings';
	$toReturn['chart_data'][3][0] = '+ rebates';
	
	

	// Iterate through each day
	while($currDate <= $endDate) {
		// Set the date for the item
		$toReturn['chart_data'][0][] = date('m/d',$currDate);

		// This will make sure we have the last price tracked durring the day.
		// This might be better with an average over the day.
		while (isset($info[$index]) && strtotime($info[$index]['date']) < ($currDate + ONE_DAY)) {
			$temp = $info[$index];
			$cPrice = ($temp['orig']+$temp['shipping'])/100.;
			$cSavings = ($temp['cost']+$temp['shipping'])/100.;
			if ($temp['after_rebate'] != 0) $cRebate = ($temp['after_rebate']+$temp['shipping'])/100.;
			else $cRebate = $cSavings;

			$index++;
		}
		
		// Update the min and max if necessary
		if (!is_null($cRebate) && $cRebate < $min) $min = $cRebate;
		if ($cPrice > $max) $max = $cPrice;

		// Add the prices to the chart
		$toReturn['chart_data'][1][] = $cPrice;
		$toReturn['chart_data'][2][] = $cSavings;
		$toReturn['chart_data'][3][] = $cRebate;

		// Increment to the next day
		$currDate += ONE_DAY;
	}

	// Setup min and max values
	$toReturn['axis_value']['min'] = $min*.95;
	$toReturn['axis_value']['max'] = $max*1.05;

	return $toReturn;
}
?>