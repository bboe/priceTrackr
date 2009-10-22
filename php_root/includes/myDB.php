<?php
require_once 'MDB2.php';

class myDB {
  private $db;
  
  function myDB() {
    $dsn = 'mysqli://pt_user:pritshiz@localhost/priceTrackr';
    $options = array('debug' => 2, 'result_buffering' => false);
    $this->db =& MDB2::factory($dsn, $options);
    
    if (PEAR::isError($this->db)) {
      // TODO: This should display the footer
      die('Sorry the page could not be processed at this time.');
    }
    $this->db->setFetchMode(MDB2_FETCHMODE_ASSOC);
  }
  
  function prepare_execute($sql, $args, $types, $select, $allowError) {
    $prep = $this->db->prepare($sql, $types,
			       $select?MDB2_PREPARE_RESULT:MDB2_PREPARE_MANIP);
    $result = $prep->execute($args);
    $prep->free();
    if ($allowError && PEAR::isError($result))
      return false;
    elseif (PEAR::isError($result)) {
      // TODO: The footer should be displayed
      die('Sorry the page could not be processed at this time.');
    }

    $row = false;
    if (is_object($result)) {
      while ($row[] = $result->fetchRow());
      unset($row[count($row)-1]);
      $result->free();
    }
    else $row = $result;
    return $row;
  }
  
  function query($sql) {
    $result =& $this->db->query($sql);
    if (PEAR::isError($result)) {
      // TODO: Should display footer
      die('Sorry the page could not be processed at this time.');
    }

    $row = false;
    if (is_object($result)) {
      while ($row[] = $result->fetchRow());
      unset($row[count($row)-1]);
      $result->free();
    }
    else $row = $result;
    return $row;
  }
  
  function affectedRows() {
    return $this->db->affectedRows();
  }
  
  function free() {
    $this->db->disconnect();
  }
}

?>
