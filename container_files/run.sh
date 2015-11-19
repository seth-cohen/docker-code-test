#!/bin/bash

VOLUME_HOME="/var/lib/mysql"

sed -ri -e "s/^upload_max_filesize.*/upload_max_filesize = ${PHP_UPLOAD_MAX_FILESIZE}/" \
    -e "s/^post_max_size.*/post_max_size = ${PHP_POST_MAX_SIZE}/" \
    -e "s/^display_errors.*/display_errors = On/"  /etc/php5/apache2/php.ini
if [[ ! -d $VOLUME_HOME/mysql ]]; then
    echo "=> An empty or uninitialized MySQL volume is detected in $VOLUME_HOME"
    echo "=> Installing MySQL ..."
    mysql_install_db > /dev/null 2>&1
    echo "=> Done!"  
    /create-mysql-admin-user.sh
else
    echo "=> Using an existing volume of MySQL"
fi

echo "=> Installing ssh keys"
/create-ssh.sh

echo "=> Cloning the remote repository: ${LABS_USER_NAME}"

# Using su here to let me run the command as wayfairer, and change remote from HTTP to ssh/git
su -c "git clone http://${LABS_USER_NAME}:wAyfAir1@52.91.239.205/git/${LABS_USER_NAME}.git /var/www/html" wayfairer
(cd /var/www/html; git remote set-url origin git@52.91.239.205:${LABS_USER_NAME}.git)

# Create user/pw in htpasswd so we can protect the private web folder
htpasswd -c -b /var/www/.htpassword wayfairer wAyfAir1

exec supervisord -n
