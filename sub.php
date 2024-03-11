<?php

// Create By FebryEnsz
$host = $_GET['host'];

function getSubdomains($host) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, "https://crt.sh/?q=%.$host&output=json");
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    
    $response = curl_exec($ch);
    curl_close($ch);
    
    $subdomains = json_decode($response, true);
    
    $subdomainNames = array_map(function($subdomain) {
        return $subdomain['name_value'];
    }, $subdomains);
    
    return $subdomainNames;
}

$subdomains = getSubdomains($host);

foreach ($subdomains as $subdomain) {
    echo $subdomain . "\n";
}
