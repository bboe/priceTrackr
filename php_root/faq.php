<?php
require_once('Cache/Lite.php');
// Set a id for this cache
$id = 'faq';

// Set a few options
$options = array(
'cacheDir' => '/tmp/',
'lifeTime' => 3600
);

// Create a Cache_Lite object
$Cache_Lite = new Cache_Lite($options);

// Test if thereis a valide cache for this id
if ($data = $Cache_Lite->get($id)) {
	print $data;
} else { // No valid cache found (you have to make the page)
	ob_start();
	define('START', true);
	$title = 'FAQ';
	require_once 'includes/header.php';

	print '<h1>Frequently Asked Questions</h1>';

	$result = $db->query('select id, question, answer from faq order by date_added');

	$count = 0;
	print '<ol>';
	foreach ($result as $value) {
		print '<li><a href="#'.$count .'">'.$value['question'].'</a></li>'."\n";
		$count++;
	}
	print '</ol>';

	$count = 0;
	foreach ($result as $value) {
		print '<div class="faq">';
		print '<h2><a name="' . $count . '"></a>'.$value['question'].'</h2>'."\n";
		print '<div class="answer">'.$value['answer'].'</div>';
		print '</div>'."\n";
		$count++;
	}

	require_once 'includes/footer.php';
	$data = ob_get_flush();
	$Cache_Lite->save($data);
}
?>