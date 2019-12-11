<?php

error_reporting(-1);

$conn = mysqli_connect('localhost', 'stanley', 'Boisdarc2027!', 'stanley');
if(mysqli_connect_errno()){
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
}
else{
  echo "Connected...";
}

function getRandomAirportPerCountry(){
  global $conn;
  $sql = "SELECT distinct(Country) FROM Edited__Airports ";
  echo"<pre>";
  echo"{$sql}\n";

  $result = $conn->query($sql);

  $airports = [];

  while($row = mysqli_fetch_assoc($result)){
  $sql1 = "SELECT * FROM Edited__Airports WHERE Country = '{$row['Country']}' order by RAND() LIMIT 1";
  $sub_result = $conn->query($sql1);

  $row2 = mysqli_fetch_assoc($sub_result);

  $airports[] = $row2;
  }
  return $airports;
}

function findClosestWithinRadius($lon,$lat,$distance = 0){
  global $conn;

  if($distance == 0){
    $limit = " LIMIT 1";
  }
  else{
    $limit = '';
  }

  echo"<pre>";

  $sql = "select *, ST_Distance_Sphere(point({$lon},{$lat}),geopoint) / 1609.3 as distance FROM Edited__Airports order by distance {$limit}";

  echo"$sql\n";
  $result = $conn->query($sql);

  $airports = [];

  if($distance > 0)
  {
    while($row = mysqli_fetch_assoc($result))
    {
      // print row
      if($row['distance'] < $distance){
        $airports[] = $row;
      }
    }
  }else{
    $airports = mysqli_fetch_assoc($result);
  }

  return $airports;
}

/**
getGeoJson
*/
function getGeoJson(){
	$json = [];
	$json['type'] = 'FeatureCollection';
	$json['features'] = [];
	
	// Get some airports randomly
	$airports = getRandomAirportPerCountry();
	
	// Loop through the results and build a php associative array to be encoded as a geojson object
	foreach($airports as $airport){
		// push a new feature onto our features array
		$json['features'][] = ['type'=>'Feature',
								'geometry'=>[
								'type'=>'Point',
								'coordinates'=>[$airport['Longitude']*1.0,$airport['Latitude']*1.0]],
								"properties"=> [
								"title"=>[$airport['Name']],
								"description"=>[$airport['City'], $airport['Country']],
								"marker-size"=>"medium",
								"marker-symbol"=>"airport",
								"marker-color"=>"#f00",
								"stroke"=>"#55555",
								"stroke-opacity"=>1,
								"stroke-width"=>2,
								"fill"=>"#55555",
								"fill-opacity"=>0.5
								]
							];
	}
	
	// dump to output (json pretty makes it look much better
	print_r(json_encode($json,JSON_PRETTY_PRINT));
	
	// Creates a file from the generated output
	file_put_contents("EveryCountry.geojson",json_encode($json,JSON_PRETTY_PRINT));
}
// Print the random airports per country
//print_r(getRandomAirportPerCountry());
getGeoJson();

?>
