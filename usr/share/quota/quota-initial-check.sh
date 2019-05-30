#!/bin/sh

# names of binaries
check=/sbin/quotacheck
on=/sbin/quotaon
quotaisnew=/var/lib/quota/new

ALLFLAGS=-aug
CHECKALLFLAGS=${ALLFLAGS}m

set -e

. /lib/lsb/init-functions

# Check if quota has been enabled already
LC_MESSAGES=C $on -ap|grep -q "is on" && exit 0

# option 'skip' takes precedence even for newly installed quota package 
skip="no"
if grep "quotacheck.mode=skip" /proc/cmdline >/dev/null 2>&1; then
	skip="yes"
fi

# Check all filesystems if quota is new
if [ -x $check -a $skip = "no" -a -f $quotaisnew ] ; then
	log_action_begin_msg 'Checking quotas';
	$check -c $CHECKALLFLAGS
	log_action_end_msg 0
fi

# Remove special file
rm -f $quotaisnew

exit 0
