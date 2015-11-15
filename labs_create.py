import tutum      # Tutum API to fire up nodecluster and run docker image
import sys        # For writing to std out and exiting the application
import time       # Duh
import threading  # Cause maybe it was a good idea to run the websocket event loop in a separate thread?
import subprocess # Cause maybe it was a good idea to run git through subprocess.Popen()?
import shutil     # to copy over the .pub key files for git
import os         # to create any directories needed for shutil

# TODO pull tutum globals and functions into separate module 
tutum.user   = "wayfairseth"
tutum.apikey = "7a0aa0f595e3a3d9f8e5f9b3e1dd5956a69f3981"
node_ready   = False
nodecluster  = False # this will be the handle to the EC2 instance via the tutum API
node         = False # this is the particular node that fired up on the EC2 instance
service      = False # this is the service that will run the actual docker container

# event loop message handler, being called by the thread running the Tutum Stream websocket
def process_event(event):
  global node_ready
  global nodecluster

  # This may be too obvious for a comment but, we are looking for the Deployed event of the Cluster
  if event['resource_uri'].encode('UTF-8') == nodecluster.resource_uri:
    if event['state'].encode('UTF-8') == 'Deployed':
      print 'All nodes have been deployed.'
      node_ready = True

# Create an empty node with tag that is labs candidate's username
def create_node(username):
  print 'Creating node: %s' % username
  region      = tutum.Region.fetch('aws/us-east-1')
  node_type   = tutum.NodeType.fetch('aws/t2.micro')
  node_tags   = [{'name':username}]
  nodecluster = tutum.NodeCluster.create(name=username, node_type=node_type, region=region, disk=60, nickname=username, target_num_nodes=1, tags=node_tags)

  if nodecluster.save():
    print 'Successfully created server: %s' % username
    print 'Deploying server with name: %s' % username
    if nodecluster.deploy():
      print 'Succesfully deployed server: %s' % username
      return nodecluster
    else:
      nodecluster.delete()
  
  print 'There was an error deploying the server node please contact Seth Cohen <scohen@wayfair.com> for support'
  return false

# Gets the IP address of the node that is running on our nodecluster
def get_node_ip(cluster):
  # TODO determine if we really need to fetch the nodecluster again or if it will dynamically update
  # it looks like the API does not require us to fetch the nodecluster again, the call to .nodes must make an http request
  print('cluster', cluster)
  print('nodes', cluster.nodes)
  nodes     = cluster.nodes
  node_uri  = nodes[0]
  # why oh why wouldn't the nodes array of the cluster be keyed by uuid so we didn't have to manipulate the URI to get it?
  node_uuid = node_uri.replace('/api/v1/node/', '').replace('/', '')
  node      = tutum.Node.fetch(node_uuid)
  print 'node ip: %s' % node.public_ip

# Will deploy a new service with the image name, to all nodeclusters with the tad 'username'
# note that the clusters must already be in a deployed state for this to succeed
def create_service(username, pub_key_file):
  print 'Creating containter: %s' % username 
  # Copy over the public ssh key that we created for gitolite (we might as well use it for SSH also)
  with open(pub_key_file) as pub_key:
    key_data = pub_key.read()

  service_tags  = [{'name': username}]
  service_image = 'wayfairseth/labslamp'
  service_ports = [
      {'protocol': 'tcp', 'inner_port': 80, 'outer_port': 80, 'published': True},
      {'protocol': 'tcp', 'inner_port': 22, 'outer_port': 2222, 'published': True}
  ]
  service_env = [
      {'key': 'AUTHORIZED_KEYS', 'value': key_data},
      {'key': 'LABS_USER_NAME', 'value': username}
  ]
  service = tutum.Service.create(image=service_image, name=username, container_ports=service_ports, tags=service_tags, container_envvars=service_env)
  
  if service.save():
    print 'Successfully created service: %s' % username
    print 'Starting the service: %s' % username
    if service.start():
      print 'Successfully started service, waiting to deploy: %s' %username
      return service
    else:
      service.delete()
  
  print 'There was an error starting the application service please contact Seth Cohen <scohen@wayfair.com for support'
  return false

# TODO Pull git methods into own module
git_dir = r'/Users/seth/Labs/Gitserver/gitolite_config'
# Configures the repository 'name' into the calling directory. Then adds the default
def git_configure_repo(name):
  # Clone the repo that we just created when we created the user (we don't need to keep this; 
  #   just setting up the user's repo with the files they'll need)
  # Add the index.php file to the public folder add the PEM to the private folder
  pvt_src         = r'/Users/seth/Docker/keys/' + name
  pvt_dst_path    = r'/Users/seth/Docker/' + name + r'/private'
  index_src       = r'/Users/seth/Docker/index.php' 
  dl_pk_src       = r'/Users/seth/Docker/dl_pk.php' 
  public_dst_path = r'/Users/seth/Docker/' + name + r'/public'
 
  PIPE = subprocess.PIPE
  print 'Cloning the User\'s repository locally'
  proc = subprocess.Popen(['git', 'clone', 'git@52.91.239.205:' + name + '.git'], stdout=PIPE, stdin=PIPE)
  print proc.communicate()[0] # debug only - print '\t=>Adding the index.php file and private key'
  
  # Actually copy the files over, creating the directories as necessary
  if not os.path.exists(pvt_dst_path + r'/'):
    os.mkdir(pvt_dst_path)
  shutil.copy2(pvt_src, pvt_dst_path + r'/' + name)
  
  if not os.path.exists(public_dst_path + r'/'):
    os.mkdir(public_dst_path)
  shutil.copy2(index_src, public_dst_path + r'/index.php')
  shutil.copy2(dl_pk_src, public_dst_path + r'/dl_pk.php')

  print '\t=>Adding the new files and directories'
  proc = subprocess.Popen(['git', 'add', '.'], cwd=name, stdout=PIPE, stdin=PIPE)
  print proc.communicate()[0] # debug only - print '\t=>commiting adding the new files'
  proc = subprocess.Popen(['git', 'commit', '-am', 'Added initial setup files for candidate'], cwd=name, stdout=PIPE, stdin=PIPE)
  print proc.communicate()[0] # debug only - print '\t=>pushing changes'
  proc = subprocess.Popen(['git', 'push'], cwd=name, stdout=PIPE, stdin=PIPE)
  print proc.communicate()[0]

# Creates an SSH key for the candidate with the name of user's name. This will be used for ssh'ing into the container and also, to provide
# secure access from the cadidate's local and container boxes into the git server.
def git_create_user(name):
  # Create new user for the git repo by the same name
  # Generate a new ssh_key for this user 
  PIPE = subprocess.PIPE
  proc = subprocess.Popen(['ssh-keygen', '-t', 'rsa', '-f', 'keys/' + name, '-N', ''], stdout=PIPE, stdin=PIPE)
  print proc.communicate()[0]
  
  # Copy the public key file to the gitolite admin repo we should also use this key for administration
  src = r'/Users/seth/Docker/keys/' + name + '.pub'
  dst = git_dir + r'/keydir/' + name + '.pub'
  shutil.copy2(src, dst)
  
  # Add the repo and user to the config file
  with open(git_dir + r'/conf/gitolite.conf', 'a') as config_file:
    config_file.write('\nrepo\t' + name + '\n\tRW+\t=\t' + name )

  # Here we are running shell commands through subprocess to execute the git calls necessary to manage the remote git server
  # via gitolite, when we push this change it will create a new user and repo and give only that user read/write access to it.
  print 'Updating gitolite config to control user access, modified config and added key'
  proc = subprocess.Popen(['git', 'status'], cwd=git_dir, stdout=PIPE, stdin=PIPE)
  print proc.communicate()[0] # debug only - print '\t=>committing changes'
  proc = subprocess.Popen(['git', 'commit', '-am', 'Added user and repo: %s; modified config and added key' % name], cwd=git_dir, stdout=PIPE, stdin=PIPE)
  print proc.communicate()[0] # debug only - print '\t=>pushing changes to remote'
  proc = subprocess.Popen(['git', 'push'], cwd=git_dir, stdout=PIPE, stdin=PIPE)
  print proc.communicate()[0]
 
  # Need to give the user access to his remote repository on the git server so ssh in and set that up
  # This will let us clone, via HTTP, the git repository that we made for this candidate on the git server.
  print 'Adding user %s to the git server. For HTTP access to only that repo on the container' % name
  proc = subprocess.Popen(['ssh', 'ubuntu@52.91.239.205', 'sudo htpasswd -b %s %s %s' % (r'/etc/apache2/.htpassword', name, 'wAyfAir1')], stdout=PIPE, stdin=PIPE)
  print proc.communicate()[0] # debug only
  
  # Return the public ssh file. We will use this in authorized_keys on the deployed container to ssh into it.
  return src

# --------------- ENTRY POINT ----------------
name = raw_input('Enter candidate\'s username: ')

# Need to set up the user's repos and access on the git server.
pub_key_file = git_create_user(name)
git_configure_repo(name)

# Create the node cluster
nodecluster = create_node(name)
print('The result of create_node is:', nodecluster)
if not nodecluster:
  sys.exit()

# Event loop to wait until node is deployed
events = tutum.TutumEvents()
events.on_message(process_event)
event_thread = threading.Thread(target=events.run_forever)
event_thread.daemon = True
event_thread.start()

# Wait for the event loop to indicate that the nodecluster is up and running.
progress = '-\|/'
count = 0
millis = int(time.time() * 1000)
while node_ready == False:
  sys.stdout.write ('\rWaiting for node to deploy %s' % progress[count])
  # Wait half a second before printing again... but let's not block with sleep
  if int(time.time() * 1000) - millis > 500:
    count += 1
    millis = int(time.time() * 1000)
    if count >= len(progress):
      count = 0

# Get the IP address of the node that we will be deploying on
node_ip = get_node_ip(nodecluster)

# Create the service (which is really just an alias for the Docker container)
service = create_service(name, pub_key_file)
print('The service is', service)
if not service:
  sys.exit()
