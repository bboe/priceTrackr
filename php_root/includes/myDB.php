<?php
require_once 'MDB2.php';

class myDB {
  private $db;
  
  function myDB() {
    // Set PEAR Error Handling function
    if (defined('ERROR_SET') && ERROR_SET)
      PEAR::setErrorHandling (PEAR_ERROR_CALLBACK, 'pear_error_handler');

    $dsn = 'mysqli://pt_user:pritshiz@localhost/priceTrackr';
    $options = array('debug' => 2, 'result_buffering' => false);
    $this->db =& MDB2::factory($dsn, $options);
    
    // This only happens if ERROR_SET is not TRUE
    if (PEAR::isError($this->db)) {
      // TODO: This should display the footer
      die('Sorry the page could not be processed at this time.');
    }
    $this->db->setFetchMode(MDB2_FETCHMODE_ASSOC);
  }
  
  function prepare_execute($sql, $args, $types, $select, $allowError) {
    $prep = $this->db->prepare($sql, $types,
			       $select?MDB2_PREPARE_RESULT:MDB2_PREPARE_MANIP);

    // Disable error handling if we need to catch it.
    if (defined('ERROR_SET') && ERROR_SET && $allowError)
      PEAR::setErrorHandling(PEAR_ERROR_RETURN);

    $result = $prep->execute($args);
    
    // Reenable error handling
    if (defined('ERROR_SET') && ERROR_SET && $allowError)
      PEAR::setErrorHandling (PEAR_ERROR_CALLBACK, 'pear_error_handler');

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

function pear_error_handler ($err_obj) {
  // Trigger a generic PHP error so email reporting happens.
  $error_string = $err_obj->getMessage() . '<br>' . $err_obj->getDebugInfo();
  trigger_error($error_string, E_USER_ERROR);
}
?>
