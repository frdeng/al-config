#!/bin/bash
#
# Copyright © 2019 Oracle Corp., Inc.  All rights reserved.
# Licensed under the Universal Permissive License v 1.0 as shown at http://oss.oracle.com/licenses/upl
#
# add_cron_job.sh: add cron job for AL auto update
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

# Add AL auto update cron job
cat > $al_cron_job_file <<CRON
# Daily cron job for AL updates
$(($RANDOM%60)) $(($RANDOM%24)) * * * root /usr/sbin/al-update &>/dev/null
CRON
