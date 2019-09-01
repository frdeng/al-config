#!/bin/bash
#
# Copyright © 2019 Oracle Corp., Inc.  All rights reserved.
# Licensed under the Universal Permissive License v 1.0 as shown at http://oss.oracle.com/licenses/upl
#
# pre_config.sh: pre-conifure for AL
#  - Disable yum-cron cron job by disabling yum-cron service
#  - Disable uptrack/ksplice cron jobs
#  - Enable ksplice Known-Exploit-Detection
#

. /usr/lib/al-config/functions

usage() {
    cat >&2 << EOF
Usage: $0 [OPTION]...
 -h This message
EOF
    exit 1
}

run_as_root_check

while getopts "h" OPTION; do
    case "$OPTION" in
      h)
        usage
        ;;
      *)
        usage
        ;;
    esac
done

# We disable yum-cron systemd service and ksplice cron jobs.
# AL cron job will directly run ksplice and yum-cron commands.

# Stop and disable yum-cron systemd service, then yum-cron con jobs won't actually run
systemctl stop yum-cron.service &>/dev/null
# yum-cron is pre set to disable by default
systemctl preset yum-cron.service &>/dev/null

# Disable ksplice cron jobs by commenting out the cron job entries.
for cron in /etc/cron.d/uptrack /etc/cron.d/ksplice; do
    if [ -f "$cron" ]; then
        sed -i '/^[0-9]/s/^/# /g' $cron
    fi
done

# Enable ksplice Known-Exploit-Detection
if [ -f /etc/uptrack/uptrack.conf ]; then
    if ! grep -q 'Known-Exploit-Detection' /etc/uptrack/uptrack.conf; then
        cat >> /etc/uptrack/uptrack.conf <<EOF

[Known-Exploit-Detection]
# Known Exploit Detection is another way Ksplice secures your system.
# Ksplice continues to close down vulnerabilities with zero downtime.
# And now you have the added security of being notified when attempted
# privilege escalation attacks are taken on your system.
enabled = yes
EOF
    fi
fi
