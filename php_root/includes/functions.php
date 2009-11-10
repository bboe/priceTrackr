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
?>