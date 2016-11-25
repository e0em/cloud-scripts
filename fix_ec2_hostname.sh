#! /bin/bash
TARGET_KEY=HOSTNAME
PUBLIC_IP=`curl -s http://169.254.169.254/latest/meta-data/public-ipv4`
REPLACEMENT_VALUE=`host  -t mx browan.com |cut -d" " -f 7|xargs -I{} host {}|grep $PUBLIC_IP|cut -f 1 -d" "`
# echo $REPLACEMENT_VALUE
CONFIG_FILE=/etc/sysconfig/network
sed -c -i "s/\($TARGET_KEY *= *\).*/\1$REPLACEMENT_VALUE/" $CONFIG_FILE
