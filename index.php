<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Skycraft Wins</title>
</head>
<body>
    <h1>Contador de Wins do Sycraft que Reseta</h1>
    <p>Obs: Por enquanto ele só lista a primeira página.</p>

    <div class="wins">
        <?php
            $data = shell_exec("get_data.py");

            echo $data;
        
        ?>
    </div>

    
    <a href="#">Atualizar</a>
</body>
</html>