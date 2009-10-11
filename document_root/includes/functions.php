<?php
if(!(defined('START') && START)) exit('Not A Valid Entry Point');

function create_guid($size = 32) {
	$guid = "";
	mt_srand();
	for($i = 0; $i < $size; $i++) {
		$temp = mt_rand(0,2);
		if ($temp == 0) $guid .= chr(mt_rand(48,57));
		else if ($temp == 1) $guid .= chr(mt_rand(65,90));
		else $guid .= chr(mt_rand(97,122));
	}
	return $guid;
}

function createHash($article,$refid) {
	return md5($article.'sdlkjapp'.$refid);
}

function intToDollar($int) {
	$int = abs($int);
	if (strlen($int) == 1) return '&nbsp;';
	return '$'.substr($int,0,-2).'.'.substr($int,-2);
}

function dropPercent($curr,$drop) {
	$drop = abs($drop);
	return number_format($drop*100/($curr+$drop),2).'%';
}

function stripslashes_array($data) {
   if (is_array($data)){
       foreach ($data as $key => $value){
           $data[$key] = stripslashes_array($value);
       }
       return $data;
   }else{
       return stripslashes($data);
   }
}

function validateEmail($email) {
	if (!eregi('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,3})$', $email)) {
		return false;
	}
	return true;
}

function sendMail($to,$subject,$body,$from=null,$html=false) {
	if ($html) {
		$body = '<html><body>'.$body.'</body></html>';
		$headers['MIME-Version'] = '1.0';
		$headers['Content-Type'] = "text/html; charset=iso-8859-1";
	}
	if (is_null($from) || $from == '') $from = 'priceTrackr <admin@priceTrackr.com>';
	if (is_array($to)) return false;
	$headers = 'From: ' .$from;	
	return mail($to,$subject,$body,$headers);
}

function sendPearMail($to,$subject,$body,$from=null,$html=false) {
	require_once('Mail.php');
	if ($html) {
		$body = '<html><body>'.$body.'</body></html>';
		$headers['MIME-Version'] = '1.0';
		$headers['Content-Type'] = "text/html; charset=iso-8859-1";
	}
	if (is_null($from) || $from == '') $headers['From'] = 'priceTrackr <admin@priceTrackr.com>';
	else $headers['From'] = $from;
	if (is_array($to)) return false;
	$headers['To'] = $to;
	$headers['Subject'] = $subject;
	
	$mail =& Mail::factory('mail');
	return $mail->send($to, $headers, $body);
}
?>