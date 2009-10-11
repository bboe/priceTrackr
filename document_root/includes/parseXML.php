<?php
$type = 0;
$toScan = array();
function getDeals() {
	global $toScan;
	$file = 'http://www.newegg.com/Product/RSS.asp?Submit=RSSDailyDeals';
	$xml_parser = xml_parser_create();
	xml_parser_set_option($xml_parser, XML_OPTION_CASE_FOLDING, true);
	xml_set_element_handler($xml_parser, "startElement", "endElement");
	xml_set_character_data_handler($xml_parser, "characterData");
	if (!($fp = fopen($file, "r"))) {
		die("could not open XML input");
	}
	while ($data = fread($fp, 1024)) {
		if (!xml_parse($xml_parser, $data, feof($fp))) {
			die(sprintf("XML error: %s at line %d",
			xml_error_string(xml_get_error_code($xml_parser)),
			xml_get_current_line_number($xml_parser)));
		}
	}
	xml_parser_free($xml_parser);
	return $toScan;
}

function startElement($parser, $name, $attrs) {
	global $type;
	if ($name == 'GUID') $type = 1;
}

function endElement($parser, $name) {
	global $type;
	$type = 0;
}

function characterData($parser, $data) {
	global $type;
	global $toScan;
	if ($type == 1 && substr($data,0,2) == 'ht') {
		$toScan[] = substr($data,-15);
	}
}
?>