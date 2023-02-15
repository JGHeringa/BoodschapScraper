<?php
require '../config.php';
$productenJson = $_POST['producten'];
$productenJson = str_replace("'", '"', $productenJson);
$key = $_POST['key'];

$today = date("Y-m.d");

if ($key != "") {
    exit;
}
file_put_contents("producten1.json", $productenJson);

$producten = json_decode($productenJson, true);
echo $productenJson;
echo "\n";
foreach ($producten as $item) {
    $naam = mysqli_real_escape_string($mysqli, $item["naam"]);
    // $naam = $item["naam"];
    $prijs = $item["prijs"];
    $perWat = $item["perWat"];
    $cat = $item["catogorie"];
    $winkel = $item["winkel"];

    $sql = "INSERT INTO Prijzen (Naam, Prijs, PerWat, Cat, Supermarkt, Datum) VALUES  (?, ?, ?, ?, ?, ?)";
    if ($stmt = $mysqli->prepare($sql)) {
        $stmt->bind_param('sdssss', $naam, $prijs, $perWat, $cat, $winkel, $today);
        if ($stmt->execute()) {
            echo "is gelukt";
        } else {
            echo "is mislukt";
        }
    } else {
        echo "zit een fout in de query: " . $mysqli->error;
    }
}
