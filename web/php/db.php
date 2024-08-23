<?php
function connectDB() {
    $login = "root";
    $pass = "gkitoaFBmQM5oMde9v3c";
    $server = "188.225.10.135";
    $name_db = "codd";
    mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);
    $link = mysqli_connect($server, $login, $pass, $name_db);
    mysqli_set_charset($link, 'utf8mb4');
    return $link;
}
?>
