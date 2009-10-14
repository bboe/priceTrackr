<?php if(!(defined('START') && START)) exit('Not A Valid Entry Point'); ?>
<div id="menu">
    <ul id="nav">
    	<?php ($_SERVER['SCRIPT_NAME'] == '/index.php')?$class = ' class="active"':$class=''; ?>
	    <li><a href="/"<?php echo $class; ?>>Home</a></li>
	    <?php ($_SERVER['SCRIPT_NAME'] == '/daily.php')?$class = ' class="active"':$class=''; ?>
		<li><a href="/daily/"<?php echo $class; ?>>Daily Drops</a></li>
    	<?php ($_SERVER['SCRIPT_NAME'] == '/add.php')?$class = ' class="active"':$class=''; ?>
		<li><a href="/faq/"<?php echo $class; ?>>FAQ</a></li>
    	<?php ($_SERVER['SCRIPT_NAME'] == '/contact.php')?$class = ' class="active"':$class=''; ?>
		<li><a href="/contact/"<?php echo $class; ?>>Contact</a></li>
    	<?php ($_SERVER['SCRIPT_NAME'] == '/about.php')?$class = ' class="active"':$class=''; ?>
		<li><a href="/about/"<?php echo $class; ?>>About</a></li>
    </ul>
</div>