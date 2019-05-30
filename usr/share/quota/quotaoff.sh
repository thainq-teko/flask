#!/bin/sh

# names of binaries
off=/sbin/quotaoff
quotaisoff=/var/lib/quota/off
ALLFLAGS=-aug

set -e

. /lib/lsb/init-functions

if [ -x $off ]
then
	log_action_begin_msg 'Turning off quotas'
	$off $ALLFLAGS || true
	# Create quota-off file
	touch $quotaisoff
	log_action_end_msg 0
fi

exit 0
