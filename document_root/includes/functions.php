<?php
if(!(defined('START') && START)) exit('Not A Valid Entry Point');

function id_to_num($newegg_id) {
  preg_match('/^N82E168(\d+)((IN)|R|(SF))?$/', $newegg_id, $matches);
  switch (count($matches)) {
  case 0:
    return NULL;
    break;
  case 2:
    return $matches[1];
    break;
  case 3:
    assert($matches[2] == 'R');
    return $matches[1] | 1 << 28;
    break;
  case 4:
    if ($matches[3] == 'SF') {
      return $matches[1] | 1 << 29;
    }
    else {
      assert($matches[2] == 'IN');
      return $matches[1] | 1 << 30;
    }
    break;
 default:
   return NULL;
   break;
  }
}

function intToDollar($int) {
  if ($int == 0)
    return 'FREE!';
  return '$'.substr($int,0,-2).'.'.substr($int,-2);
}

function dropPercent($curr, $drop) {
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