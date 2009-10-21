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
if (false && $data = $Cache_Lite->get($cacheID)) {
	print $data;
} else { // No valid cache found (you have to make the page)
	ob_start();
	define('START', true);
	define('ERROR_SET', true);
	require_once('includes/functions.php');
	require_once 'includes/myDB.php';

	$id = id_to_num($_GET['item']);
	$db = new myDB();

	$result = allTimeQuery($db, $id);
	$skip = 0;
	$db->free();

	/*
	* Begin Chart Definition
	*/
	$chart = buildData($result);
	$chart['license'] = 'K1XUXQVMDNCL.NS5T4Q79KLYCK07EK';
	$chart['chart_type'] = 'Line';
	$chart['chart_value'] = array('prefix'=>'$','decimals'=>2,'separator'=>',','position'=>'cursor','size'=>14,'color'=>'000000','background_color'=>'FFD991','alpha'=>90);
	$chart['chart_pref'] = array('line_thickness'=>2,'point_shape'=>'none');
	$chart['chart_transition'] = array('type'=>'slide_down','delay'=>0,'duration'=>1,'order'=>'series');
	$chart['legend_rect'] = array ('x'=>5,'y'=>5,'width'=>490);
	$chart['legend_transition'] = array('type'=>'slide_right','delay'=>0,'duration'=>1);
	$chart['axis_category'] = array('skip'=>$skip);
	$chart['axis_value']['steps'] = 5;
	$chart['axis_value']['prefix'] = '$';
	$chart['series_color'] = array('FFCF75','AA5C4E','4E85AA');
	$chart['series_explode'] = array(250,175,100);

	SendChartData($chart);

	$data = ob_get_flush();
	$Cache_Lite->save($data);
}

function allTimeQuery($db,$id) {
  $result = $db->prepare_execute('select date(date_added) as date, original, price, rebate, shipping from item_history where id = ? order by date', $id, 'text', true, false);
  return $result;
}

function buildData($info) {
  define('ONE_DAY',60*60*24);
  $chart_data[0][0] = NULL;
   
  $chart_data[0][0] = NULL;
  $chart_data[1][0] = 'original';
  $chart_data[2][0] = '+ savings';
  $chart_data[3][0] = '+ rebates';
  $chart_data[4][0] = 'original + shipping';

  $max_axis = 0;
  $min_axis = 0x7FFFFFFF;

  $index = 0;
  $curr_date = strtotime($info[0]['date']);
  $end_date = time();  
  while($curr_date <= $end_date) {
    $chart_data[0][] = date('m/d',$curr_date);

    // This will make sure we have the last price tracked durring the day.
    while (isset($info[$index]) && strtotime($info[$index]['date']) < ($curr_date + ONE_DAY)) {
      $temp = $info[$index];
      $original = $temp['original'] / 100.;
      $price = $temp['price'] / 100.;
      $rebate = $temp['rebate'] / 100.;
      $shipping = $original + $temp['shipping'] / 100.;
      $index++;
    }
		
    if ($original > $max_axis) $max_axis = $original;
    if ($shipping < $min_axis) $min_axis = $shipping;

    // Add the prices to the chart
    $chart_data[1][] = $original;
    $chart_data[2][] = $price;
    $chart_data[3][] = $rebate;
    $chart_data[4][] = $shipping;

    // Increment to the next day
    $curr_date += ONE_DAY;
  }

  // Setup min and max values
  $toReturn['axis_value']['min'] = $min_axis * .99;
  $toReturn['axis_value']['max'] = $max_axis * 1.01;
  $toReturn['chart_data'] = $chart_data;

  return $toReturn;
}
?>