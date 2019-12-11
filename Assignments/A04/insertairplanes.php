<?php

// Make the connection
$conn = mysqli_connect('localhost', 'stanley', 'secret', 'stanley');

if(mysqli_connect_errno()){
	echo "Failed to connect to MySQL: " . mysqli_connect_error();
}
else{
	echo "Connected...\n";
}

  /* change character set to utf8 */
if (!$conn->set_charset("utf8")) {
    printf("Error loading character set utf8: %s\n", $conn->error);
} else {
    printf("Current character set: %s\n", $conn->character_set_name());
}


/**
* Clean Strings for processing
*/

function cleanData($data){
	// remove commas from field
	if(strpos($data, ",")){
		$data = str_ireplace(",","",$data);
	}
	
	// escape string if it has single quotes
	if(strpos($data,"'")){
		$data = addslashes($data);
	}
	
	// get rid of \N
	if($data == "\N"){
		$data = NULL;
	}
	
	return $data;
}

$columns = ['Airport_ID','Name','City','Country','IATA','ICAO','Latitude','Longitude','Altitude','Timezone','DST','Tz','Type','Source', 'LonLat'];

$cnames = $columns;

$csv = array_map('str_getcsv', file('airports.dat'));

$i = 0;
foreach($csv as $row){
	
	$debug = [];
	
	//Build insertion query
	$A = "INSERT INTO Airports ";
	
	// adds column names to query
	$B = "(".implode(',',$cnames).")";
	$C = "VALUES (";
	
	// If first column name is Id add $i as id value
    if($cnames[0] == 'Id'){
        $C .= "'{$i}',";
		}
    // add values to be inserted
    foreach($row as $val){
        $val = cleanData($val);
        $debug[] = $val;
        $C .= "'{$val}',";
        }
    // trim off last trailing comma 
    $C = rtrim($C,",");
	 
	 // pull out lat lon and build a point type
	 if(sizeof($row) > 14){
		$lat = $row[7];
		$long = $row[8];
	 }
	 else{
		 $lat = $row[6];
		 $lon = $row[7];
	 }
	 $C .= ",GeomFromText('POINT({$lon} {$lat})')";
	 //Add last parenthesis
	 $D = ");";
	 
	 // Concatenate all parts
	 $sql = "{$A}{$B}{$C}{$D}";
	 
	 $result = $conn->query($sql);
	 
	 //print errors
	 if(!$result){
		 echo "Error message: " . $conn->error."\n";
		 print_r($debug);
		 echo $sql;
		 exit;
	 }
	 $i++;
}

?>
