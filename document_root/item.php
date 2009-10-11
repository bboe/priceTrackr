<?php
require_once('Cache/Lite.php');

// Set a id for this cache
if (isset($_GET['item']) && $_GET['item'] != '') {
	$id = 'item-'.$_GET['item'];
}
else $id = 'item';

// Set a few options
$options = array(
'cacheDir' => '/tmp/',
'lifeTime' => 3600
);

// Create a Cache_Lite object
$Cache_Lite = new Cache_Lite($options);

// Test if there is a valide cache for this id
if ($data = $Cache_Lite->get($id)) {
	print $data;
	print "\n".'<!--priceTrackr :)-->';
} else { // No valid cache found (you have to make the page)
	ob_start();
	define('START', true);
	$title = 'Item';
	require_once 'includes/header.php';
	
	// $result comes from includes/title.php	

	if (isset($_GET['item']) && $_GET['item'] != '' && sizeof($result[0]) != 1) {
		
		$url = 'http://www.newegg.com/Product/Product.asp?Item=';
		$colors = array('#CCC','#999');
		print '<div class="itemName"><h4><a href="'.$url.$id.'" onClick="javascript:urchinTracker(\'/outgoing/newegg.com/'.$id.'\');">'.$result[0]['name'].'</a></h4>
		<p>Model Number: '.$result[0]['model_num'].'</p></div>';

		?>
		<div class="itemAdd">
		<script type="text/javascript"><!--
		google_ad_client = "pub-0638295794514727";
		google_ad_width = 468;
		google_ad_height = 60;
		google_ad_format = "468x60_as";
		google_ad_type = "text_image";
		google_ad_channel ="0017611932";
		google_color_border = "C8E9FF";
		google_color_bg = "C8E9FF";
		google_color_link = "0000FF";
		google_color_text = "000000";
		google_color_url = "FF0000";
		//--></script>
		<script type="text/javascript"
		src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
		</script>
		</div>
		
		<?php		
		// Check to make sure the item wasn't added today		
		if (!($result[0]['s_date'] == date('Y-m-d'))) {
			require_once 'includes/chart/charts.php';
			echo InsertChart ('/static_content/scripts/charts.swf', '/static_content/charts_library', '/includes/graph.php?item='.$_GET['item'],500,250,'C8E9FF',true);
		}
		else print '<p class="mesg">This item was added within the last 24 hours and therefore no chart will be displayed.</p>';

		$value = end($result);
		$currO = $value['orig']+$value['shipping'];
		$currS = $value['cost']+$value['shipping'];
		if ($value['after_rebate'] != 0) $currR = $value['after_rebate']+$value['shipping'];
		else $currR = $currS;

		$maxO = $maxS = $maxR = 0;
		$minO = $minS = $minR = 0x7FFFFF;

		foreach ($result as $value) {
			$cPrice = $value['orig']+$value['shipping'];
			$cSavings = $value['cost']+$value['shipping'];
			if ($value['after_rebate'] != 0) $cRebate = $value['after_rebate']+$value['shipping'];
			else $cRebate = $cSavings;

			if ($cPrice > $maxO) {
				$maxO = $cPrice;
				$dateMaxO = $value['s_date'];
			}
			if ($cSavings > $maxS) {
				$maxS = $cSavings;
				$dateMaxS = $value['s_date'];
			}
			if ($cRebate > $maxR) {
				$maxR = $cRebate;
				$dateMaxR = $value['s_date'];
			}

			if ($cPrice < $minO) {
				$minO = $cPrice;
				$dateMinO = $value['s_date'];
			}
			if ($cSavings < $minS) {
				$minS = $cSavings;
				$dateMinS = $value['s_date'];
			}
			if ($cRebate < $minR) {
				$minR = $cRebate;
				$dateMinR = $value['s_date'];
			}
		}

		print '<h3>Statistics</h3>';
		print '<table class="stats">';
		print '<tr>';
		print '<th><h3>Prices</h3></th>';
		print '<th><h3>Current</h3></th>';
		print '<th><h3>Minimum</h3></th>';
		print '<th><h3>Maximum</h3></th>';
		print '</tr>';
		print '<tr>';
		print '<td>cost + shipping</td>';
		print '<td>' . intToDollar($currO).'</td>';
		print '<td><span class="min">' . intToDollar($minO) . '</span> on ' . $dateMinO .'</td>';
		print '<td><span class="max">' . intToDollar($maxO) . '</span> on ' . $dateMaxO .'</td>';
		print '</tr>';
		print '<tr>';
		print '<td>+ savings</td>';
		print '<td>' . intToDollar($currS).'</td>';
		print '<td><span class="min">' . intToDollar($minS) . '</span> on ' . $dateMinS .'</td>';
		print '<td><span class="max">' . intToDollar($maxS) . '</span> on ' . $dateMaxS .'</td>';
		print '</tr>';
		print '<tr>';
		print '<td>+ rebate</td>';
		print '<td>' . intToDollar($currR).'</td>';
		print '<td><span class="min">' . intToDollar($minR) . '</span> on ' . $dateMinR .'</td>';
		print '<td><span class="max">' . intToDollar($maxR) . '</span> on ' . $dateMaxR .'</td>';
		print '</tr>';
		print '</table>';
		require_once 'includes/title.php';

	}
	elseif (isset($_GET['item']) && $_GET['item']) {
		print 'This item has recently been added and currently has no data. Data will be added for this item within a day.';
	}
	else print 'Invalid item';
	require_once 'includes/footer.php';
	$data = ob_get_flush();
	$Cache_Lite->save($data);
}
?>
