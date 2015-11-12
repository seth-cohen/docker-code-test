<html>
<head>
  <meta htp-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <title>Labs Project Instructions</title>
  <style>
    html {
      background-color: #d0d0d0;
    }
    body {
      background-color: #fdfdfd; 
    }
    .bd {
      width:  960px;
      background-color: white;
      color: #000;
      margin: auto;
    }
    .alert {
      color: #f32;
    }
    .step_heading {
      background-color: #efefef;
      font-size: 130%;
      padding: 5px;
      border-bottom: 2px solid black;
    }
    .title {
      font-size: 145%;
      padding: 5px;
    }
  </style>
</head>

<body class="bd">
  <div class="title alert">
    Please follow these instructions carefully.
  </div>
  <div class="step_container" id="step_one">
    <div class="step_heading">STEP 1: Setup SSH Connection Locally To Connect to Your Demo Site</div>
    <ul class="step_list">
      <li>Download private key pem file <a href="src/to/dl/script">here</a> using the password in your email</li>      
      <li>Save file locally: you will need to refer to it when making the ssh connection to the server</li>      
      <li>To facilitate things you can edit/create your .ssh/config file and add your server's IP as host and point to this PEM file</li>      
      <li>Make sure that you have an ssh agent installed. In Windows do: blah.</li>      
      <li>SSH into the server and browse around.  You should be able to locate this file at /var/www/html/public/index.php</li>      
    </ul>
  </div>
  <div class="step_container" id="step_two">
    <div class="step_heading">STEP 2: Setup Git Authorization Locally</div>
    <ul class="step_list">
      <li>Download private key pem file <a href="src/to/dl/script">here</a> using the password in your email</li>      
      <li>Save file locally: you will need to refer to it when making connection to the git server</li>      
      <li>To facilitate things you can edit/create your .ssh/config file and add the git server's IP as host and point to this PEM file</li>      
      <li>Make sure that you have an ssh agent installed. In Windows do: blah.</li>      
      <li>Clone the repo using the url given to you in the email sent into an empty directory</li>      
    </ul>
  </div>
        <li class="alert">NOTE: You will likely need to delete the existing public folder and it's contents for this to work, since you can only clone into an empty directory.</li>
        <li>Alternatively, you can just do a 'git remote add' with the proper switches to allow you to create the repo without deleting the folder.</li>

  <div class="step_container" id="step_three">
    <div class="step_heading">STEP 3: Build an Awesome ToDo Web Application</div>
    <ul class="step_list">
      <li>SSH into your deployed server</li>
      <li>Connect to MySQL database using the following credentials: </li>
      <li>Create a database with the name "wayfairlabs"
        <ul>
          <li class="alert">This step is important, you will not be able to connect to a database by any other name</li>
        </ul>
      </li>
      <li>Create whatever tables you think will be necessary to create a single user ToDo Application.</li>
      <li>Clone the repository from the git server locally. </li>
      <li>Include the Database support file, this will provide you with an object that you can use to connect to the DB and write queries</li>
    </ul>
  </div>

</body>
</html>

