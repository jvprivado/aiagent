<?php
$data = file_get_contents($_FILES['file']['tmp_name']);    

$fp = fopen("asd.mp3", 'wb');

fwrite($fp, $data);
fclose($fp);

?>