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
        <div class="page pg-center">
	        <div class="titleFlex">
                <div class="title large">BannerGuard</div>
		        <div class="stitle">Проверьте ваши дисплеи</div>
	        </div>
            <div class="pc-content">
	            <form id="uploadForm" method="POST" enctype="multipart/form-data" action="workspace.php">
		            <label class="input-file">
			            <input type="submit">
			            <span>Выберите файлы</span>
		            </label>
	            </form>
	            <span class="comment">Может занять некоторое время.<br>Создано для демонстрации. Более точный результат при запуске скриптов локально.</span>
            </div>
        </div>
    </div>
    <script>
    function toggle(el) {
        el.style.display = (el.style.display == 'block') ? '' : 'block'
    }
    document.getElementById('fileInput').addEventListener('change', function() {
        if (this.files.length > 0) {
            document.getElementById('uploadForm').submit();
        }
    });
    </script>
</html>