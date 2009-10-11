<?php
require_once 'Cache/Lite.php';

$options = array('cacheDir' => '../cache08/');
$cache = new Cache_Lite($options);

$cache->clean();

header('Location: /');
exit();

?>

