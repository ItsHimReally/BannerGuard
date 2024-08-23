<?php
include('php/db.php');
$link = connectDB(); $new = false;

if (is_numeric($_GET["id"])) {
    $stmt = mysqli_prepare($link, "SELECT * FROM `comparisons` WHERE `id` = ?");
    mysqli_stmt_bind_param($stmt, "s", $_GET["id"]);
    mysqli_stmt_execute($stmt);
    $info = mysqli_fetch_array(mysqli_stmt_get_result($stmt));
	if (!isset($info["id"])) {
        $new = true;
	}
} else {
	$new = true;
}
?>
<html>
<head>
    <title>BannerGuard</title>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="css/style.css" media="all">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="Description" content="BannerGuard">
    <meta http-equiv="Content-language" content="ru-RU">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&family=Roboto&display=swap" rel="stylesheet">
</head>
<div class="wrapper">
	<div class="sideBar">
		<div class="menu">
			<a href="/"><img class="icon" src="/images/speedometer.svg" alt="Главная"></a>
			<a href="/comparisons"><img class="icon" src="/images/file-earmark-text-fill.svg" alt="История"></a>
		</div>
	</div>
	<div class="mheader">
		<a href="/"><img class="icon" src="/images/speedometer.svg" alt="Главная"></a>
		<a href="/comparisons"><img class="icon" src="/images/file-earmark-text-fill.svg" alt="История"></a>
	</div>
    <div class="page">
	    <div class="titleFlex">
		    <div class="title">Сравнение бок о бок</div>
	    </div>
	    <div class="content">
		    <?php if ($new): ?>
		    <form id="uploadForm" method="POST" enctype="multipart/form-data" action="handler.php">
			    <div class="files">
				    <div class="file">
					    <span>Приложите фотографию или видео с камеры</span>
					    <label class="input-file-r">
						    <input type="file" name="img1" id="fileInput1" accept=".png,.jpg,.jpeg,.mp4" required>
					    </label>
					    <div class="preview">
						    <img id="preview1" style="display:none;" width="200px" alt="Preview 1" src="">
					    </div>
				    </div>
				    <div class="file">
					    <span>Приложите фотографию отображаемого контента для сравнения</span>
					    <label class="input-file-r">
						    <input type="file" name="img2" id="fileInput2" accept=".png,.jpg,.jpeg" required>
					    </label>
					    <div class="preview">
						    <img id="preview2" style="display:none;" width="200px" alt="Preview 2" src="">
					    </div>
				    </div>
			    </div>
			</form>
		    <?php else: ?>
		    <div class="files">
			    <div class="file">
				    <span><?=$info["img1Name"]?></span>
				    <div class="preview">
					    <?php if (isset($info["processedImg"])): ?>
					    <img width="200px" alt="Preview 1" src="data:image/png;base64,<?=$info["processedImg"]?>">
					    <?php else: ?>
					    <img width="200px" alt="Preview 1" src="data:image/png;base64,<?=$info["img1"]?>">
					    <?php endif; ?>
				    </div>
			    </div>
			    <div class="file">
				    <span><?=$info["img2Name"]?></span>
				    <div class="preview">
					    <img width="200px" alt="Preview 2" src="data:image/png;base64,<?=$info["img2"]?>">
				    </div>
			    </div>
		    </div>
		    <?php endif; ?>
		    <?php if (isset($info["result"])): ?>
		    <div class="result">
				<div class="center">
                    <?php
                    if ($info["result"] > 0.7) {
						$percClass = "pgreen";
						$percSubtitle = "Объекты совпадают с референсом";
                    } elseif ($info["result"] > 0.5) {
                        $percClass = "pyellow";
                        $percSubtitle = "Возможные искажения";
                    } else {
                        $percClass = "pred";
                        $percSubtitle = "Совпадений нет или есть искажения";
                    }
                    ?>
					<div class="perc <?=$percClass?>">
						<span class="pt"><?=round($info["result"]*100, 1)?>%</span>
						<span class="psubtitle"><?=$percSubtitle?></span>
					</div>
					<div class="checks">
                        <?php
                        $data = json_decode($info["checks"], true);
                        function getColorClass($key, $data) {
                            $global = $data['global'];
                            $isValid = true;
                            $isMismatched = false;
                            foreach ($data as $objectKey => $object) {
                                if ($objectKey === 'global') continue;
                                if ($global[$key] !== $object[$key]) {
                                    $isMismatched = true;
                                }
                                if (!$object[$key]) {
                                    $isValid = false;
                                }
                            }
                            if (!$isValid) {
                                return 'red';
                            } elseif ($isMismatched) {
                                return 'yellow';
                            } else {
                                return 'green';
                            }
                        }
                        $items = [
                            "global_text" => "Текст на изображении в целом",
                            "text" => "Текст на объектах",
                            "color" => "Контуры на объектах",
                            "cnn" => "Сверточная нейронная сеть",
                            "oa" => "Дополнительные источники"
                        ];
                        foreach ($items as $key => $text) {
                            $colorClass = getColorClass($key, $data);
                            echo '<div class="c"><div class="icon '.$colorClass.'"></div> <span>' . $text . '</span></div>';
                        }
                        ?>
					</div>
				</div>
		    </div>
            <?php else: ?>
		    <?php if (!$new): ?>
		    <div class="result">
				<div class="center">
					<img src="images/svg.svg" alt="Loading">
					<span class="wtitle">Загрузка результатов...</span>
					<span class="wsubtitle">Наши модели активно работают, чтобы предоставить наилучший результат.</span>
				</div>
		    </div>
		    <script>
                function checkForUpdate() {
                    fetch('https://codd.tw1.su/php/isResults.php?id=<?=$info["id"]?>')
                        .then(response => response.text())
                        .then(data => {
                            if (data === 'true') {
                                location.reload();
                            }
                        })
                        .catch(error => console.error('Ошибка при запросе к API:', error));
                }
                setInterval(checkForUpdate, 2000);
		    </script>
		    <?php endif; ?>
		    <?php endif; ?>
	    </div>
    </div>
</div>
<script src="css/script.js"></script>
</html>