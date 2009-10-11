<?php
define('START', true);
$title = 'Add Item';
require_once 'includes/header.php';

if (isset($_POST['id'])) {
	$id = strtoupper(trim($_POST['id']));
	$valid = true;
	// If just hit submit
	if (!isset($_POST['valid']) || !$_POST['valid']) {
		if (!(strlen($id) == 15)) {
			$valid = false;
			$mesg = "Invaild newegg product ID.";
		}
	}
	if ($valid) {
	  $result = $db->prepare_execute('select deleted from item where id = ?',$id,'text',true,false);
	  if (sizeof($result) == 0) {
	    $result = $db->prepare_execute('insert into item (id,date_added,flag) values(?,now(),-1)',$id,'text',false,true);
	    if ($result) {
	      $mesg = 'Sucessfully added item: <a href="/i/'.$id.'/">'.$id.'</a><br />Details will be filled in during the next update.';
	    }
	    else {
	      $mesg = 'Item could not be added. Please try again later.';
	      sendMail('bbzbryce@gmail.com','priceTrackr::Add error','Failed on item: '.$id);
	    }
	  }
	  elseif ($result[0]['deleted']) {
	    $db->prepare_execute('update item set deleted = 0, flag = -1 where id = ?',$id,'text',false,false);
	    $mesg = 'Item has been readded: <a href="/i/'.$id.'/">'.$id.'</a><br />New information will be gathered shortly.';
	    sendMail('bbzbryce@gmail.com','priceTrackr::Item readd','Readded item: '.$id);
	  }
	  else $mesg = 'Item has already been added: <a href="/i/'.$id.'/">'.$id.'</a>';
	}
 }
?>
<h1>Add item</h1>
<?php if (isset($mesg)) print "<p style=\"color:red\">$mesg</p>\n"; ?>
<form name="add" action="add.php" method="post">
    <p>
      <label for="id">item #:</label>
      <input name="id" size="20" id="id" type="text" />
      <input name="submit" type="submit" value="submit" />
      <input name="valid" value="0" type="hidden" />
    </p>
</form>

<h2>Where do I get the item number?</h2>
<p>Visit <a href="http://www.newegg.com" target="_blank">newegg</a> and find a product.  The item number
can then be easily found in two places.</p>
<h3>The URL</h3>
<p>The blue part of the url is the item number:</p>
<p>http://www.newegg.com/Product/Product.asp?Item=<span class="min">N82E16819116001</span></p>
<h3>In the Bread Crumb</h3>
<p>Just under the search area where the white part of the page begins is the bread crumb.
The item number is shown in blue:</p>
<p>> Categories > Processors / CPUs > Processors > intel > Item #: <span class="min">N82E16819116001</span></p>

<?php require_once 'includes/footer.php'; ?>