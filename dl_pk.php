<?php
$local_file = '{1}';
$download_file = '{1}.pem';

header('Cache-control: private');
header('Content-Type: application/octet-stream');
header('Content-Length: '.filesize($local_file));
header('Content-Disposition: filename='.$download_file);

readfile($local_file);
