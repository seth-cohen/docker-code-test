# Let's start from vanilla ubuntu, with a little kick
FROM ubuntu:trusty
MAINTAINER Seth Cohen <scohen@wayfair.com>

# Install packages. Yeah, I know, that's a lot of stuff to install, We could probably do without apc and 
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
  apt-get -y install supervisor git apache2 apache2-utils libapache2-mod-php5 mysql-server php5-mysql php-apc php5-mcrypt openssh-server && \
  echo "ServerName localhost" >> /etc/apache2/apache2.conf

# Add image configuration and scripts
COPY start-apache2.sh /start-apache2.sh
COPY start-mysqld.sh /start-mysqld.sh
COPY start-sshd.sh /start-sshd.sh
COPY run.sh /run.sh
COPY create-ssh.sh /create-ssh.sh
RUN chmod 755 /*.sh
COPY my.cnf /etc/mysql/conf.d/my.cnf
COPY supervisord-apache2.conf /etc/supervisor/conf.d/supervisord-apache2.conf
COPY supervisord-mysqld.conf /etc/supervisor/conf.d/supervisord-mysqld.conf
COPY supervisord-sshd.conf /etc/supervisor/conf.d/supervisord-sshd.conf

# Remove pre-installed database
RUN rm -rf /var/lib/mysql/*

# Add MySQL utils
COPY create-mysql-admin-user.sh /create-mysql-admin-user.sh
RUN chmod 755 /*.sh

# Config to enable .htaccess
COPY apache-default /etc/apache2/sites-available/000-default.conf
RUN a2enmod rewrite

# SSH daemon requires this directory
RUN mkdir /var/run/sshd

#Enviornment variables to configure php
ENV PHP_UPLOAD_MAX_FILESIZE 10M
ENV PHP_POST_MAX_SIZE 10M

# Add volumes for MySQL 
VOLUME  ["/etc/mysql", "/var/lib/mysql" ]

# Create user and final setup: exposed ports and run command as labs user
RUN adduser --disabled-password --home=/wayfairer --gecos "" wayfairer
RUN rm -R /var/www/html
RUN chown -R wayfairer:wayfairer /var/www
EXPOSE 22 80 3306

CMD ["/run.sh"]
