<?php
if(!(defined('START') && START)) exit('Not A Valid Entry Point');
require_once('includes/error.php');
require_once('includes/myDB.php');
require_once("includes/functions.php");
if (!isset($db)) $db = new myDB();

?>

<!DOCTYPE html
PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
<title>priceTrackr - <?php require_once 'title.php'?></title>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
<link rel="stylesheet" type="text/css" href="/style/layout.css" />
<script type="text/javascript" src="/scripts/niftycube.js"></script>
<script type="text/javascript">
function searchInputClick() {
	input = document.getElementById('searchInput')
	if (input.value == 'search...') input.value = ''
}

function searchInputBlur() {
	input = document.getElementById('searchInput')
	if (input.value == '') input.value = 'search...'
}
</script>
<script type="text/javascript">
window.onload=function() {
Nifty("div#container");
Nifty("div#adds,div#content","same-height");
Nifty("div#header,div#footer,div#content h1","transparent");
Nifty("ul#nav a","transparent bottom");
}
</script>
</head>
<body>
<div id="container">
<div id="header">
<table style="width:99%">
<!-- How can I do this without a table? -->
<tr valign="bottom">
<td><h1>priceTrackr</h1></td>
<td style="text-align:right;padding-bottom:5px"><form method="get" action="/search/">
	<div>
	<input type="text" name="q" id="searchInput" value="search..." size="20" maxlength="100" onfocus="searchInputClick();" onblur="searchInputBlur();" />
	<input type="image" alt="Submit" src="/images/search.png" style="vertical-align:middle" />
	</div>
</form></td>
</tr>
</table>
</div>
<?php require_once("includes/nav.php"); ?>
<div id="content">
