<?php
// TODO Add user authentication here.
header('Content-Type: application/pdf');
header('Content-Disposition: attachment; filename="{1}"');
readfile('../{1}');
