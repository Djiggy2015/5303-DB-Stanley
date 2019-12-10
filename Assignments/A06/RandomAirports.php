<?php

error_reporting(-1);

// connect to db
$conn = mysqli_connect('localhost', 'stanley', 'Secret', 'stanley');
if(mysqli_connect_errno())
{
	echo "Failed to connect to MySQL: " . mysqli_connect_error();	
}
else
{
	echo "Connected...";
}
	

function getRandomAirportPerCountry()
{
	global $conn;
	
	// Create the SQL Statement
	$sql = "SELECT distinct(Country) FROM Edited__Airports";
	
	// preformat tag
	echo"<pre>";
	
	//Print the statement
	echo"{$sql}\n";
	
	// run query
	$result = $conn->query($sql);
	
	// create an empty array
	$airports = [];
	
	// while there are more rows in query result
	while($row = mysqli_fetch_assoc($result)){
		
		// create a sub query
		$sql1 = "SELECT * FROM Edited__Airports WHERE Country = '{$row['Country']}' order by RAND() LIMIT 1"; 
		
		// run sub query
		$sub_result = $conn->query($sql1);
		
		// get single row result of sub query
		$row2 = mysqli_fetch_assoc($sub_result);
		
		// push that result onto our array
		$airports[] = $row2;
		
	}
	
	// return resulting array
	return $airports;
}


/**
* findClosestWithinRadius
*
* Params:
*	$lon : x coord
*	$lat : y coord
*	$distance : radius
*/
function findClosestWithinRadius($lon,$lat,$distance = 0)
{
	global $conn;
	
	if($distance == 0)
	{
		$limit = " LIMIT 1";
	}
	else{
		// otherwise don't use a limit on query
		$limit = '';
	}
	
	// respect whitespace and newlines
	echo"<pre>";
	
	// select everything and the distance from 'geopoint' to (lon, lat)
	$sql = "SELECT *, ST_Distance_Sphere({$lon},{$lat}),geopoint) / 1609.3 as distance FROM airports order by distance {$limit}";
	
	// print the query
	echo"$sql\n";
	
	// run the query
	$result = $conn->query($sql);
	
	// create an empty array
	$airports = [];
	
	// if distance > 0 get more than a single match
	if($distance > 0)
	{
		while($row = mysqli_fetch_assoc($result))
		{
			// print_r($row);
			if($row['distance'] < $distance)
			{
				$airports[] = $row;
			}
		}
	}else{
		// give a single closest result
		$airports = mysqli_fetch_assoc($result);
	}
	
	// return result
	return $airports;
}

print_r(getRandomAirportPerCountry());

?>
