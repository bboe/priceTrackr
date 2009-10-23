<?php
ob_start();
define('START', true);
require_once 'includes/header.php';

$from = '';
$message = '';
$subject = '';

if (isset($_POST) && sizeof($_POST) > 0) {
  set_magic_quotes_runtime(FALSE);
  if (get_magic_quotes_gpc()) {
    $_POST = stripslashes_array($_POST);
  }
  $msg = '';
  if (isset($_POST['submit']) && $_POST['submit'] == "submit") {
    $valid = true;
    if (!false) {
      $from = trim($_POST['from']);
      $subject = trim($_POST['subject']);
      $message = trim($_POST['message']);
      if ($from == '') {
	$valid = false;
	$msg .= '<p class="mesg">Error: No from address</p>';
      }
      else if (!validateEmail($from)) {
	$valid = false;
	$msg .= '<p class="mesg">Error: Invalid email address</p>';
      }
      if ($subject == '') {
	$valid = false;
	$msg .= '<p class="mesg">Error: No subject</p>';
      }
      if ($message == '') {
	$valid = false;
	$msg .= '<p class="mesg">Error: No message</p>';
      }
    }
    if ($valid) {
      $to = 'admin@pricetrackr.com';
      sendPearMail($to, $subject, $message, $from);
      $msg .= '<p class="mesg">Your message has been sent. Thank you.</p>';
    }
  }
  else {
    header('Location: /');
    exit();
  }
 }
ob_end_flush();
?>

<h1>Contact</h1>

<?php if (isset($msg)) print $msg; ?>

<form name="contact" action="/contact/" method="post">
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