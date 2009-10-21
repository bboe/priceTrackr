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

function SendChartData( $chart=array() ){
	
  $xml="<chart>\r\n";
  $Keys1= array_keys((array) $chart);
  for ($i1=0;$i1<count($Keys1);$i1++){
    if(is_array($chart[$Keys1[$i1]])){
      $Keys2=array_keys($chart[$Keys1[$i1]]);
      if(is_array($chart[$Keys1[$i1]][$Keys2[0]])){
	$xml.="\t<".$Keys1[$i1].">\r\n";
	for($i2=0;$i2<count($Keys2);$i2++){
	  $Keys3=array_keys((array) $chart[$Keys1[$i1]][$Keys2[$i2]]);
	  switch($Keys1[$i1]){
	  case "chart_data":
	    $xml.="\t\t<row>\r\n";
	    for($i3=0;$i3<count($Keys3);$i3++){
	      switch(true){
	      case ($chart[$Keys1[$i1]][$Keys2[$i2]][$Keys3[$i3]]===null):
		$xml.="\t\t\t<null/>\r\n";
		break;
		
	      case ($Keys2[$i2]>0 and $Keys3[$i3]>0):
		$xml.="\t\t\t<number>".$chart[$Keys1[$i1]][$Keys2[$i2]][$Keys3[$i3]]."</number>\r\n";
		break;
								
	      default:
		$xml.="\t\t\t<string>".$chart[$Keys1[$i1]][$Keys2[$i2]][$Keys3[$i3]]."</string>\r\n";
		break;
	      }
	    }
	    $xml.="\t\t</row>\r\n";
	    break;
						
	  case "chart_value_text":
	    $xml.="\t\t<row>\r\n";
	    $count=0;
	    for($i3=0;$i3<count($Keys3);$i3++){
	      if($chart[$Keys1[$i1]][$Keys2[$i2]][$Keys3[$i3]]===null){$xml.="\t\t\t<null/>\r\n";}
	      else{$xml.="\t\t\t<string>".$chart[$Keys1[$i1]][$Keys2[$i2]][$Keys3[$i3]]."</string>\r\n";}
	    }
	    $xml.="\t\t</row>\r\n";
	    break;

	  case "draw":
	    $text="";
	    $xml.="\t\t<".$chart[$Keys1[$i1]][$Keys2[$i2]]['type'];
	    for($i3=0;$i3<count($Keys3);$i3++){
	      if($Keys3[$i3]!="type"){
		if($Keys3[$i3]=="text"){$text=$chart[$Keys1[$i1]][$Keys2[$i2]][$Keys3[$i3]];}
		else{$xml.=" ".$Keys3[$i3]."=\"".$chart[$Keys1[$i1]][$Keys2[$i2]][$Keys3[$i3]]."\"";}
	      }
	    }
	    if($text!=""){$xml.=">".$text."</text>\r\n";}
	    else{$xml.=" />\r\n";}
	    break;
						
						
	  default://link, etc.
	    $xml.="\t\t<value";
	    for($i3=0;$i3<count($Keys3);$i3++){
	      $xml.=" ".$Keys3[$i3]."=\"".$chart[$Keys1[$i1]][$Keys2[$i2]][$Keys3[$i3]]."\"";
	    }
	    $xml.=" />\r\n";
	    break;
	  }
	}
	$xml.="\t</".$Keys1[$i1].">\r\n";
      }else{
	if($Keys1[$i1]=="chart_type" or $Keys1[$i1]=="series_color" or $Keys1[$i1]=="series_image" or $Keys1[$i1]=="series_explode" or $Keys1[$i1]=="axis_value_text"){							
	  $xml.="\t<".$Keys1[$i1].">\r\n";
	  for($i2=0;$i2<count($Keys2);$i2++){
	    if($chart[$Keys1[$i1]][$Keys2[$i2]]===null){$xml.="\t\t<null/>\r\n";}
	    else{$xml.="\t\t<value>".$chart[$Keys1[$i1]][$Keys2[$i2]]."</value>\r\n";}
	  }
	  $xml.="\t</".$Keys1[$i1].">\r\n";
	}else{//axis_category, etc.
	  $xml.="\t<".$Keys1[$i1];
	  for($i2=0;$i2<count($Keys2);$i2++){
	    $xml.=" ".$Keys2[$i2]."=\"".$chart[$Keys1[$i1]][$Keys2[$i2]]."\"";
	  }
	  $xml.=" />\r\n";
	}
      }
    }else{//chart type, etc.
      $xml.="\t<".$Keys1[$i1].">".$chart[$Keys1[$i1]]."</".$Keys1[$i1].">\r\n";
    }
  }
  $xml.="</chart>\r\n";
  echo $xml;
}
?>