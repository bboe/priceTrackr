<?php
if(!(defined('START') && START)) exit('Not A Valid Entry Point');
require_once('includes/myDB.php');
require_once("includes/functions.php");
if (!isset($db)) $db = new myDB();

?>
<!DOCTYPE html
PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<title><?php require_once 'title.php'?> &raquo; priceTrackr</title>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
<link rel="shortcut icon" href="/favicon.ico" />
<link rel="stylesheet" type="text/css" href="/layout.css" />
<script type="text/javascript" src="/javascript.js"></script>
</head>
<body onload="document.getElementById('q').focus()">
<div id="container">
<div id="header">
<table style="width:99%">
<!-- How can I do this without a table? -->
<tr valign="bottom">
<td><h1>priceTrackr</h1></td>
<td style="text-align:right;padding-bottom:5px"><form method="get" action="/search/">
    <div>
      <input type="text" name="q" id="q" size="20" maxlength="100" />
      <input type="submit" value="search" style="vertical-align:middle" />
    </div>
</form></td>
</tr>
</table>
</div>
<?php
$home_class = $faq_class = $contact_class = $about_class = '';
switch ($_SERVER['SCRIPT_NAME']) {
 case '/index.php': $home_class = ' class="active"'; break;
 case '/faq.php': $faq_class = ' class="active"'; break;
 case '/about.php': $about_class = ' class="active"'; break;
}
?>
<div id="menu">
  <ul id="nav">
    <li><a href="/"<?php echo $home_class; ?>>Home</a></li>
    <li><a href="/faq/"<?php echo $faq_class; ?>>FAQ</a></li>
    <li><a href="/about/"<?php echo $about_class; ?>>About</a></li>
  </ul>
</div>
<div id="content">
