<?php
include('db.php');
$link = connectDB();

if (isset($_GET['id'])) {
    $id = $_GET['id'];
    $query = "SELECT result FROM comparisons WHERE id = ?";
    if ($stmt = mysqli_prepare($link, $query)) {
        mysqli_stmt_bind_param($stmt, "i", $id);
        mysqli_stmt_execute($stmt);
        mysqli_stmt_bind_result($stmt, $result);
        mysqli_stmt_fetch($stmt);
        if ($result !== null) {
            echo "true";
            exit();
        }
        mysqli_stmt_close($stmt);
    }
}
echo "false";
?>
