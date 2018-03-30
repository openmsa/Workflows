#!/bin/sh

USERNAME=admin
PASSWORD=`cat /dev/urandom | tr -dc '[:graph:]' | head -c 9`
echo ${USERNAME}:${PASSWORD} | chpasswd

cat > /home/admin/.ssh/authorized_keys <<EOF
%rsa_pub_key%
EOF

chmod 600 /home/admin/.ssh/authorized_keys
chown admin:admin /home/admin/.ssh/authorized_keys

