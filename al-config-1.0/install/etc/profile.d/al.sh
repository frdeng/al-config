# Copyright © 2019 Oracle Corp., Inc.  All rights reserved.
# Licensed under the Universal Permissive License v 1.0 as shown at http://oss.oracle.com/licenses/upl

[ -x /usr/bin/id ] || return
[ "$(/usr/bin/id -u)" = 1000 ] || return
[ -x /usr/bin/uptrack-uname ] || return

echo "Welcome to Autonomous Linux"
echo "Effective kernel version is $(/usr/bin/uptrack-uname -r)"

if [ ! -f /etc/al-config/oci.conf ]; then
    echo
    echo "Please add OCI notification service topic OCID with"
    echo "$ sudo al-config -T [topic OCID]"
fi
