<?php 
include 'db.php';
 
 

$conn = new mysqli($servername, $username, $password, $database);
 
 
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
 

$video = array(); 
 
 
$sql = "SELECT id, href, name FROM video_cards;";
 

$stmt = $conn->prepare($sql);
 

$stmt->execute();
 
 
$stmt->bind_result($id, $name);
 

while($stmt->fetch()){
 
 
 $temp = [
 'id'=>$id,
 'name'=>$name,
 'href'=>$href
 ];
 
  
 array_push($heroes, $temp);
}
 

echo json_encode($heroes);

 ?>