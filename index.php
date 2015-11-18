<html>
<head>
  <meta htp-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <title>Demo Project Instructions</title>
  <style>
    html {
      background-color: #d0d0d0;
    }
    body {
      background-color: #fdfdfd; 
      font-family: arial, sans-serif;
      box-shadow: 0 0 15px #333;
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
    .code {
      font-family: "Courier New", Courier, monospace
    }
    .note {
      padding: 10px;
    }
  </style>
</head>

<body class="bd">
  <div class="title alert">
    Please follow these instructions carefully. 
  </div>
  <div class="note">  
    We have provisioned you a full LAMP stack running an Ubuntu distribution. You are viewing the default page of that remote server.  We would like for you to take the time allotted and create a working web application on. You are free to implement the application however you like.
  </div>
  <div class="step_container" id="step_one">
    <div class="step_heading">STEP 1: Setup SSH Connection Locally To Connect to Your Remote Server</div>
    <ul class="step_list">
      <li>Download the private key pem file <a href="private/dl_pk.php">here</a> using the username and password in your email (note for seth user = wayfairer; pass = wAyfAir1)
        <ul>
          <li class="alert">You will use this same private key to connect to the git repository as well</li>
        </ul>
      </li>      
      <li>Save file locally: you will need to refer to it when making the SSH connection to the server</li>      
      <li>Ensure that you have an SSH client
        <ul>
          <li>Unix/Linux: Just fire up a Terminal; an SSH client should be included by default</li> 
          <li>Windows: You will likely need to install a client; try PuTTY</li> 
        </ul>
      </li>
      <li>SSH into your private server and browse around. You should be able to locate this file (the one that you a reading right now) at <span class="code">/var/www/html/index.php</span>
        <ul>
          <li>Your remote server has already been configured to accept your private key, so all you need to do is point your client to the private key</li>
        </ul>
      </li>      
    </ul>
  </div>
  <div class="step_container" id="step_two">
    <div class="step_heading">STEP 2: Setup Git Authorization Locally and on Your Remote Server</div>
    <ul class="step_list">
      <li>Ensure that you have Git installed on your local system
        <ul>
          <li>Unix/Linux: Use whatever package manager that comes with your distribution.</li>
          <li>Windows: Several options are available, <a href="http://git-scm.com/download/win">Git for Windows</a> seems to be the most official</li>
        </ul>
      </li>
      <li>Your remote server already has Git installed</li>
      <li>Configure Git, both locally and on your remote server, to use the same <a href="private/dl_pk.php">private key</a> downloaded in Step 1.</li>
      <li>Clone the repository with the username <span class="code">git</span> on server <span class="code">52.91.239.205</span>. The remote repo will be <?= htmlentities('<username>'); ?>.git
        <ul>
          <li>The complete clone command: <span class="code">git clone git@52.91.239.205:<?= htmlentities('<username>'); ?>.git</span></li>
        </ul>
      </li>      
    </ul>
  </div>
  <div class="step_container" id="step_three">
    <div class="step_heading">STEP 3: Build an Awesome ToDo Web Application</div>
    <ul class="step_list">
      <li>SSH into your deployed server</li>
      <li>Connect to the MySQL database with the same username and password that you used to download the pem file</li>
      <li>Create a database with the name "wayfair"
        <ul>
          <li class="alert">This step is important, you will not be able to connect to a database by any other name</li>
        </ul>
      </li>
      <li>Create whatever tables you think will be necessary to create a single user ToDo Application.</li>
      <li>Your personal git repository is already cloned at <span class="code">/var/www/html</span>
        <ul>
          <li>You can create all of your code locally on the cloned repo, push to remote, and then do a pull on the demo server</li>
          <li>Alternatively, you can simply sftp the files into the <span class="code">/var/www/html</span> directoryi. However, you will still need to push your code to the remote repo.</li>
        </ul>
      </li>
      <li>Include the Database support file <span class="code">include once "private/dbo.php"</span>, this will provide you with an object that you can use to connect to the DB and write queries</li>
      <li>There are no other requirements or limitations other than being able to add new ToDo Items, mark them as complete or not and of course viewing them.
        <ul>
          <li>This can be as flashy as you want, can be a single page app or several different scripts</li>
          <li>Please add a link at the bottom of your app that will point to a page that lists, further refinements or alternate design choices that you would have implemented had you been given more time.</li>
        </ul>
      </li>
    </ul>
  </div>
</body>
</html>

