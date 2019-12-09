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
 -f Re-create cron job
 -h This message
EOF
    exit 1
}

run_as_root_check

force=0
while getopts "fh" OPTION; do
    case "$OPTION" in
      f)
        force=1
        ;;
      h)
        usage
        ;;
      *)
        usage
        ;;
    esac
done

if [ ! -f "$al_cron_job_file" ] || [ $force -eq 1 ]; then
    # Add or re-create AL auto update cron job
    cat > "$al_cron_job_file" <<CRON
# Daily cron job for AL updates
$((RANDOM%60)) $((RANDOM%24)) * * * root /usr/sbin/al-update >/dev/null
CRON
    log "Created cron job file $al_cron_job_file ."
fi
