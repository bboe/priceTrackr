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
if (false && $data = $Cache_Lite->get($id)) {
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
		print '<div class="itemName"><h4><a href="'.$url.$_GET['item'].'" onClick="javascript:urchinTracker(\'/outgoing/newegg.com/'.$_GET['item'].'\');">'.$result[0]['title'].'</a></h4>
		<p>Model Number: '.$result[0]['model'].'</p></div>';

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
		   if (!($result[0]['update_date'] == date('Y-m-d'))) {?>
		<OBJECT classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000"
			codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,0,0" 
			WIDTH="400" 
			HEIGHT="250" 
			id="charts">
		  <PARAM NAME="movie" VALUE="/static_content/charts.swf?library_path=/static_content/charts_library&xml_source=/g/<?=$_GET['item']?>" />
		  <PARAM NAME="quality" VALUE="high" />
		  <PARAM NAME="bgcolor" VALUE="#666666" />
		  <param name="allowScriptAccess" value="sameDomain" />
		  
		  <EMBED src="/static_content/charts.swf?library_path=/static_content/charts_library&xml_source=/g/<?=$_GET['item']?>"
			 quality="high" 
			 bgcolor="#C8E9FF" 
			 WIDTH="500" 
			 HEIGHT="250" 
			 NAME="charts" 
			 allowScriptAccess="sameDomain" 
			 swLiveConnect="true" 
			 TYPE="application/x-shockwave-flash" 
			 PLUGINSPAGE="http://www.macromedia.com/go/getflashplayer">
		  </EMBED>
		</OBJECT>
                <?php
		}
		else print '<p class="mesg">This item was added within the last 24 hours and therefore no chart will be displayed.</p>';

		$value = end($result);
		$original = $value['original'];
		$price = $value['price'];
		$rebate = $value['rebate'];
		$shipping = $value['shipping'];

		$max_original = $max_price = $max_rebate = $max_shipping = 0;
		$min_original = $min_price = $min_rebate = $min_shipping = 0x7FFFFF;

		$date_min_shipping = NULL;
		
		foreach ($result as $value) {
		  if ($value['original'] > $max_original) {
		    $max_original = $value['original'];
		    $date_max_original = $value['update_date'];
		  }
		  if ($value['price'] > $max_price) {
		    $max_price = $value['price'];
		    $date_max_price = $value['update_date'];
		  }
		  if ($value['rebate'] > $max_rebate) {
		    $max_rebate = $value['rebate'];
		    $date_max_rebate = $value['update_date'];
		  }
		  if ($value['shipping'] > $max_shipping) {
		    $max_shipping = $value['shipping'];
		    $date_max_shipping = $value['update_date'];
		  }

		  if ($value['original'] < $min_original) {
		    $min_original = $value['original'];
		    $date_min_original = $value['update_date'];
		  }
		  if ($value['price'] < $min_price) {
		    $min_price = $value['price'];
		    $date_min_price = $value['update_date'];
		  }
		  if ($value['rebate'] < $min_rebate) {
		    $min_rebate = $value['rebate'];
		    $date_min_rebate = $value['update_date'];
		  }
		  if ($value['shipping'] < $min_shipping && $value['shipping'] != 0) {
		    $min_shipping = $value['shipping'];
		    $date_min_shipping = $value['update_date'];
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
		print '<td>original</td>';
		print '<td>' . intToDollar($original).'</td>';
		print '<td><span class="min">' . intToDollar($min_original) . '</span> on ' . $date_min_original .'</td>';
		print '<td><span class="max">' . intToDollar($max_original) . '</span> on ' . $date_max_original .'</td>';
		print '</tr>';
		print '<tr>';
		print '<td>+ savings</td>';
		print '<td>' . intToDollar($price).'</td>';
		print '<td><span class="min">' . intToDollar($min_price) . '</span> on ' . $date_min_price .'</td>';
		print '<td><span class="max">' . intToDollar($max_price) . '</span> on ' . $date_max_price .'</td>';
		print '</tr>';
		print '<tr>';
		print '<td>+ rebate</td>';
		print '<td>' . intToDollar($rebate).'</td>';
		print '<td><span class="min">' . intToDollar($min_rebate) . '</span> on ' . $date_min_rebate .'</td>';
		print '<td><span class="max">' . intToDollar($max_rebate) . '</span> on ' . $date_max_rebate .'</td>';
		print '</tr>';
		print '<tr>';
		print '<td>shipping*</td>';
		print '<td>' . intToDollar($shipping).'</td>';
		if ($date_min_shipping == NULL) {
		  print '<td colspan=2><strong>Always Free Shipping</strong></td>';
		}
		else {
		  print '<td><span class="min">' . intToDollar($min_shipping) . '</span> on ' . $date_min_shipping .'*</td>';
		  print '<td><span class="max">' . intToDollar($max_shipping) . '</span> on ' . $date_max_shipping .'</td>';
		}
		print '</tr>';
		print '</table>';
		print '<p>* Shipping is calculated to zip code 93117. Minimum shipping is the lowest nonzero shipping cost.</p>';
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
