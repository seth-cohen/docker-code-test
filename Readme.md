# To Run:
 * python docker_create.py 
 * it will ask for a username, so type one in (no spaces)
 * Note: A config file ~/.dockerrc must be present with the following sections and options
  * [Tutum] 
   * user = \<Tutum API usernamne\>
   * key = \<Tutum API key\>
  * [Git]
   * dir = \<Directory where gitolite config repo was cloned\>

# What does this do?
 * The script will create a new SSH key for a new git user with the user name entered when running the script.
 * Create a new user in a gitolite managed EC2 git server.
  * Involves editing a special gitolite cloned repo config file, adding the public key, and pushing to the server
  * This also initializes a bare repo that is private to that user (and the master git user has access as well)
 * Gives the user temporary http access to clone the repo (required to get the repo on the remote server before SSH is configured)
 * Configures the user's private git repo:
  * Adds the necessary files: index.php with instructions, user's private key, .htaccess to protect the private key and a download script
 * Fires up an EC2 instance via the Tutum python SDK, and then waits patiently for the instance to be deployed.
 * Deploys a docker container already configured with a LAMP stack on that EC2 instance.
  * Uses the Tutum python SDK to ensure that the proper ports on the container are available and/or forwarded from/to the host.
 * Clones the user's private repo via HTTP; then changes remote to connect via ssh.
 * The IP of the node/container is output of the script along with (currently) some debug information.

# How to connect?
 * You can use a browser and connect directly to the IP that was printed out by the script. There are instructions that you will
see at that URL that will tell you how to proceed to connect to the git repo, ssh into the remote box, etc.
