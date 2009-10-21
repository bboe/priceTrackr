<?php
if(!(defined('START') && START)) die('Not A Valid Entry Point');

define('ERROR_SET', true);
define('ERROR_EMAIL', false);

$errorlevel = E_ALL;
error_reporting($errorlevel);

// Function to handle all errors
function php_error_handler ($errno, $errstr, $errfile, $errline) {
  if (error_reporting() & $errno) {		
    $errortype = array (
			E_WARNING      => "Warning",
			E_NOTICE       => "Notice",
			E_USER_ERROR   => "User Error",
			E_USER_WARNING => "User Warning",
			E_USER_NOTICE  => "User Notice",
			E_STRICT       => "Runtime Notice"
			);
    if (ERROR_EMAIL) {
      $email = "bbzbryce@gmail.com";
      $mesg = "$errortype[$errno]: In $errfile, line: $errline\n$errstr\n\n";
      $mesg .= "Server Info\n";
      $mesg .= var_export($_SERVER,true);
      if (isset($_COOKIE)) {
	$mesg .= "\nCookie Information\n";
	$mesg .= var_export($_COOKIE,true);
      }
      if (isset($_SESSION)) {
	$mesg .= "\nSession Information\n";
	$mesg .= var_export($_SESSION,true);
      }
      error_log($mesg,1,$email,'From: ADMIN <errorLog@pricetrackr.com>');
      header('Location: /error/');
      exit(1);
    }
    
    // Only occurs when ERROR_EMAIL is false or not set
    die ("<b>$errortype[$errno]</b> In <b>$errfile</b>, line: <b>$errline</b>\n<br>$errstr");
  }
}

if (ERROR_SET) set_error_handler('php_error_handler', $errorlevel);
?>
