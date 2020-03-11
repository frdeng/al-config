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

source_config_file

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

schedule_auto_update "$force"
