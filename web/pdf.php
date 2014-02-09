<?php

 // do all this moving to ensure there is no way that user filename can be passed to the command line
 $info = pathinfo($_FILES['file']['name']);
 $ext = $info['extension']; // get the extension of the file
 $newname = generateRandomString().$ext;
 $output = "./" . generateRandomString().$pdf; 

 $target = "../".$newname;
 move_uploaded_file( $_FILES['file']['tmp_name'], $target);

$ret = exec("python ../mePrePrint.py generate ../resources/coversheet.docx ". $newname . " " . $output . " -t '" . escapeshellcmd($_POST['type']) . "' -a '" . escapeshellcmd($_POST['name']) . "' -c '" . escapeshellcmd($_POST['citation']) . "' -r '" . escapeshellcmd($_POST['title']) . "' -o '" . escapeshellcmd($_POST['copyright']) . "' -y '" . escapeshellcmd($_POST['year']) . "' -u '" . escapeshellcmd($_POST['URL']) . "'", $out, $err);

var_dump($ret);
var_dump($out);
var_dump($err);

function generateRandomString($length = 10) {
    $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $randomString = '';
    for ($i = 0; $i < $length; $i++) {
        $randomString .= $characters[rand(0, strlen($characters) - 1)];
    }
    return $randomString;
}

?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" 
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head>
    	<title>Open Library of Humanities: Green Generator</title>
	<link rel="stylesheet" href="css/shared.css" type="text/css" media="screen" />
	<!--[if lte IE 6]><link rel="stylesheet" type="text/css" media="screen" href="css/ie6.css" /><![endif]-->
	<!--[if gte IE 7]><link rel="stylesheet" type="text/css" media="screen" href="css/ie7.css" /><![endif]-->
    </head>
    <body>
        <div class="header">
		<h1>Open Library of Humanities: Green Generator</h1>
        </div>
    
	<div class="main">
		<p>Many thanks for using the generator. Your <a href="<?php $output ?>">PDF is now ready</a>.</p>

	</div>
        
    </body>
</html>
