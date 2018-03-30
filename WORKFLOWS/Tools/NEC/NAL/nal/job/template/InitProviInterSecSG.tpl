#!/bin/sh

GATEWAY_IP=%gatewayIP%
REMOTE_HOST_LIST=(%remoteHostList%)

index=0
for item in ${REMOTE_HOST_LIST[@]};
do
    index=`expr $index + 1`
    if [ $index -eq 1 ] ; then
       sed -i "s/^host=.*/host=$item/g" /opt/necfws/etc/fws.ini
    else
       sed -i "/^$before_line$/a host=$item" /opt/necfws/etc/fws.ini
    fi
    before_line=host\=$item
done

sed -i "s/^default=.*/default=$GATEWAY_IP/g" /opt/necfws/etc/fws.ini

USERNAME=admin
PASSWORD=`cat /dev/urandom | tr -dc '[:graph:]' | head -c 9`
echo ${USERNAME}:${PASSWORD} | chpasswd

cat > /var/opt/necfws/admin/.ssh/authorized_keys <<EOF
%rsa_pub_key%
EOF

chmod 600 /var/opt/necfws/admin/.ssh/authorized_keys
chown admin:admin /var/opt/necfws/admin/.ssh/authorized_keys
