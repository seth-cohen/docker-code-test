#!/bin/bash

/usr/bin/mysqld_safe > /dev/null 2>&1 &

RET=1
while [[ RET -ne 0 ]]; do
    echo "=> Waiting for confirmation of MySQL service startup"
    sleep 5
    mysql -uroot -e "status" > /dev/null 2>&1
    RET=$?
done

PASS = 'wAyfAir1'
echo "=> Creating MySQL admin user (wayfairer) with default password"

mysql -uroot -e "CREATE USER 'wayfairer'@'%' IDENTIFIED BY 'wAyfAir1'"
mysql -uroot -e "GRANT ALL PRIVILEGES ON *.* TO 'wayfairer'@'%' WITH GRANT OPTION"


echo "=> Done!"

echo "========================================================================"
echo "You can now connect to this MySQL Server using:"
echo ""
echo "    mysql -uwayfairer -p$PASS -h<host> -P<port>"
echo ""
echo "Please remember to change the above password as soon as possible!"
echo "MySQL user 'root' has no password but only allows local connections"
echo "========================================================================"

mysqladmin -uroot shutdown
