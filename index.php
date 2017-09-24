<?php 
$servername = "edvin9kc.beget.tech";
$username = "edvin9kc_edvin";
$password = "iopl87jkl";
$database = "edvin9kc_edvin";
 
 
//creating a new connection object using mysqli 
$conn = new mysqli($servername, $username, $password, $database);
 
//if there is some error connecting to the database
//with die we will stop the further execution by displaying a message causing the error 
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
 
//if everything is fine
 
//creating an array for storing the data 
$viseo = array(); 
 
//this is our sql query 
$sql = "SELECT id, href, name FROM video_cards;";
 
//creating an statment with the query
$stmt = $conn->prepare($sql);
 
//executing that statment
$stmt->execute();
 
//binding results for that statment 
$stmt->bind_result($id, $name);
 
//looping through all the records
while($stmt->fetch()){
 
 //pushing fetched data in an array 
 $temp = [
 'id'=>$id,
 'name'=>$name,
 'href'=>$href
 ];
 
 //pushing the array inside the hero array 
 array_push($heroes, $temp);
}
 
//displaying the data in json format 
echo json_encode($heroes);

 ?>