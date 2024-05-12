<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (isset($_POST["first_name"]) && isset($_POST["last_name"]) && isset($_POST["email"]) && isset($_POST["phone"]) && isset($_POST["password"])) {
        $first_name = $_POST["first_name"];
        $last_name = $_POST["last_name"];
        $email = $_POST["email"];
        $phone = $_POST["phone"];
        $password = $_POST["password"];
        
        // Replace with the correct file path on your server
        $csvFilePath = "data.csv";
        
        // Create or open the CSV file for appending
        $csvFile = fopen($csvFilePath, "a");
        
        if ($csvFile) {
            // Write the data to the CSV file
            fputcsv($csvFile, [$first_name, $last_name, $email, $phone, $password]);

            // Close the CSV file
            fclose($csvFile);
            
            
            header("Location: signup.html");
            
        } else {
            echo "Error opening CSV file for writing.";
        }
    } else {
        echo "All form fields are required.";
    }
    

}
?>
