<?php
include('php/db.php');
$link = connectDB();

//if ($_SERVER['REQUEST_METHOD'] == 'POST') {
//    if (isset($_FILES['file']) && $_FILES['file']['error'] == UPLOAD_ERR_OK) {
//        $fileTmpPath = $_FILES['file']['tmp_name'];
//        $fileName = $_FILES['file']['name'];
//        $fileSize = $_FILES['file']['size'];
//        $fileType = $_FILES['file']['type'];
//        $fileExtension = strtolower(pathinfo($fileName, PATHINFO_EXTENSION));
//
//        if ($fileExtension == 'wav') {
//            processWavFile($fileTmpPath, $fileName);
//        } elseif ($fileExtension == 'zip') {
//
//        } else {
//            echo 'Unsupported file type.';
//        }
//    }
//}

function convertImageToBase64($file) {
    if (isset($file) && $file['error'] === UPLOAD_ERR_OK) {
        $imageData = file_get_contents($file['tmp_name']);
        return base64_encode($imageData);
    } else {
        echo "Ошибка при загрузке изображения: " . $file['name'] . "\n";
        return null;
    }
}

$img1Base64 = convertImageToBase64($_FILES['img1']);
$img2Base64 = convertImageToBase64($_FILES['img2']);

if ($img1Base64 and $img2Base64) {
    $stmt = mysqli_prepare($link, "INSERT INTO `comparisons` (`img1Name`, `img1`, `img2Name`, `img2`) VALUES (?, ?, ?, ?);");
    mysqli_stmt_bind_param($stmt, "ssss", $_FILES['img1']["name"], $img1Base64, $_FILES['img2']["name"], $img2Base64);
    mysqli_stmt_execute($stmt);
    $newId = mysqli_insert_id($link);

    header("Location: /workspace.php?id=".$newId);
    exit();
}