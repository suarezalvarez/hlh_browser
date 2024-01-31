<?php
// Include database connection and other necessary files
require_once 'db_connect.php'; // Adjust the filename as 
necessary

// Define a function to handle gene search
function searchGene($geneName, $databases, $species) {
    // ... Implement the search logic here (similar to 
what was provided earlier)
}

// Define a function to retrieve available databases
function getDatabases() {
    // ... Implement the logic to retrieve available 
databases
}

// Define a function to retrieve available species
function getSpecies() {
    // ... Implement the logic to retrieve available 
species
}

// Main request handling
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Retrieve POST data
    $geneName = $_POST['gene'] ?? null;
    $databases = $_POST['databases'] ?? []; // Assuming 
this is an array of database IDs
    $species = $_POST['species'] ?? null;

    // Validate and sanitize inputs here

    // Perform the search
    $results = searchGene($geneName, $databases, 
$species);

    // Return results
    header('Content-Type: application/json');
    echo json_encode($results);
} else {
    // For GET requests, you might want to provide the 
necessary data for the frontend to build the search form
    $availableDatabases = getDatabases();
    $availableSpecies = getSpecies();

    // You might want to include a HTML form here for GET 
requests or render a JSON with available options
    // For simplicity, the JSON option is shown here
    header('Content-Type: application/json');
    echo json_encode([
        'databases' => $availableDatabases,
        'species' => $availableSpecies
    ]);
}
?>

