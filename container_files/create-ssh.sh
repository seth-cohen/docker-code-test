#!/bin/sh
if [ "${AUTHORIZED_KEYS}" != "" ]; then
  echo "=> Found authorized keys"
  su -c 'mkdir -p /wayfairer/.ssh' wayfairer
  su -c 'chmod 700 /wayfairer/.ssh' wayfairer
  su -c 'touch /wayfairer/.ssh/authorized_keys' wayfairer
  su -c 'chmod 600 /wayfairer/.ssh/authorized_keys' wayfairer
  echo "=> Adding public key to .ssh/authorized_keys: ${AUTHORIZED_KEYS}"
  su -c 'echo "${AUTHORIZED_KEYS}"  >> /wayfairer/.ssh/authorized_keys' wayfairer
else
  echo "ERROR: No authorized keys found"
  exit 1
fi
