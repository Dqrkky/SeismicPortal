<?php

header_remove("x-powered-by");
header("Content-Type: application/javascript");

// Get the callback function name from the query string
$callback = isset($_GET['callback']) ? $_GET['callback'] : 'callback';

// My data
$data = [
    "name" => "alice"
];

// Encode the data as JSON and wrap it in the callback
echo $callback . '(' . json_encode($data, JSON_PRETTY_PRINT) . ');';

?>