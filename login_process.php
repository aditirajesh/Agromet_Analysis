<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $login_email = $_POST["email"];
    $login_password = $_POST["password"];
    
    // Read the contents of the CSV file
    $csvFile = fopen("data.csv", "r");
    $found = false;

    // Skip the header row
    fgetcsv($csvFile);

    while (($data = fgetcsv($csvFile)) !== false) {
        list($first_name, $last_name, $email, $phone, $password) = $data;
        if ($email === $login_email && $password === $login_password) {
            // Successful login
            $found = true;
            break;
        }
    }

    fclose($csvFile);

    if ($found) {
        // Redirect to the dashboard page or a success page
        header("Location: index.html");
        exit();
    } else {
        // Redirect to the login page with an error message
        echo ("log in failed, log in credentials are wrong please try again");
        exit();
    }
}
?>
