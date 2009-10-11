<?php
ob_start();
define('START', true);
$title = 'Contact Form';
require_once 'includes/header.php';

if (!isset($_GET['type'])) {
	header('Location: /');
	exit();
}
$type = $_GET['type'];
$types = array('general','support','marketing');
if (!in_array($type,$types)) header('Location: /');

$from = '';
$message = '';
$subject = '';

if (isset($_POST) && sizeof($_POST) > 0) {
	set_magic_quotes_runtime(FALSE);
	if (get_magic_quotes_gpc()) {
		$_POST = stripslashes_array($_POST);
	}
	$mesg = '';
	if (isset($_POST['submit']) && $_POST['submit'] == "submit") {
		$valid = true;
		if (!false) {
			$from = trim($_POST['from']);
			$subject = trim($_POST['subject']);
			$message = trim($_POST['message']);
			if ($from == '') {
				$valid = false;
				$mesg .= '<p class="mesg">Error: No from address</p>';
			}
			if (!validateEmail($from)) {
				$valid = false;
				$mesg .= '<p class="mesg">Error: Invalid email address</p>';
			}
			if ($subject == '') {
				$valid = false;
				$mesg .= '<p class="mesg">Error: No subject</p>';
			}
			if ($message == '') {
				$valid = false;
				$mesg .= '<p class="mesg">Error: No message</p>';
			}
		}
		if ($valid) {
			$to = $type . '@pricetrackr.com';
			$to = 'bbzbryce@gmail.com';
			sendPearMail($to,$subject,$message,$from);
			header('Location: /thankyou.php');
			exit();
		}
	}
	else {
		header('Location: /');
		exit();
	}
}
ob_end_flush();
$Type = ucfirst($type);
?>

<h1><?=$Type?> Contact Form</h1>

<?php if (isset($mesg)) print $mesg; ?>

<form name="contact" action="/c/<?=$type?>" method="post">
  <p>
    <label for="from">your email:</label>
    <br />
    <input name="from" id="from" size="50" value="<?=$from?>" type="text" />
  </p>
  <p>
    <label for="subject">subject:</label>
    <br />
    <input name="subject" id="subject" size="50" value="<?=$subject?>" type="text" />
  </p>
  <p>
    <label for="message">message:</label>
    <br />
    <textarea name="message" id="message" cols="50" rows="10"><?=$message?></textarea>
  </p>
  <p>
    <input name="submit" type="submit" value="submit" />
    <input name="valid" value="0" type="hidden" />
  </p>
</form>



<? require_once 'includes/footer.php'; ?>