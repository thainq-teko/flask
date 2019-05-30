#!/bin/sh

# names of binaries
check=/sbin/quotacheck
on=/sbin/quotaon
quotaisoff=/var/lib/quota/off
quotaisnew=/var/lib/quota/new
forcequotacheck=/forcequotacheck

ALLFLAGS=-aug
CHECKALLFLAGS=${ALLFLAGS}m
CHECKUSERFLAGS=-ucm
CHECKGROUPFLAGS=-gcm

set -e

. /lib/lsb/init-functions

# create list of all fs with quota
scan_fstab()
{
	tmplist=`grep "^[ ]*[^#].*$1" /etc/fstab | \
    	      sed -e 's/\(^[[:space:]]*[^[:space:]]*[[:space:]]*[^[:space:]]*[[:space:]]*[^[:space:]]*\).*/\1/g' \
                  -e 's/^[[:space:]]*[^[:space:]]*[[:space:]]*//g'`
	list=${tmplist:=empty}
}

# if fs needs a quotacheck, check it
check_quota()
{
	if [ "$2" != "xfs" ]
	then	
		if [ ! -e $1/quota.user -a ! -e $1/aquota.user ] ; then
			log_warning_msg "Warning: user quota not configured in filesystem \`$1.'"
		elif [ "$4" != "journaled" -a ! -f $quotaisoff ] ; then
			# quota was not shut down correctly, check filesystem
			$check $3 $1
		elif test ! -e $1/aquota.user; then
			# filesystem is new, check it	
			test ! -s $1/quota.user && $check $3 $1
		elif test ! -s $1/aquota.user; then
			# filesystem is new, check it	
			$check $3 $1
		fi
	fi
}

# Check if quota has been enabled already
LC_MESSAGES=C $on -ap|grep -q "is off" || exit 0

# Did we get a quota option on boot?
force="no"
if [ -f $forcequotacheck ]; then
	log_warning_msg "Warning: Please pass 'quotacheck.mode=force' on the kernel command line rather than creating /forcequotacheck on the root file system."
	force="yes"
elif grep "quotacheck.mode=force" /proc/cmdline >/dev/null 2>&1; then
	force="yes"
fi

skip="no"
if grep "quotacheck.mode=skip" /proc/cmdline >/dev/null 2>&1; then
	skip="yes"
fi

if [ -x $check -a $skip = "no" ] ; then
	log_action_begin_msg 'Checking quotas';
	# Check all filesystems if quota is new
	if [ -f $quotaisnew -o $force = "yes" ] ; then
		$check $CHECKALLFLAGS || $check -c $CHECKALLFLAGS
		log_action_end_msg 0
	else
		# check filesystems that seem to need a check
		scan_fstab "usrquota"
		set -- $list

		while [ $# -ge 2 ]
		do
			check_quota "$1" "$2" "$CHECKUSERFLAGS" "normal"
			shift; shift
		done

		scan_fstab "grpquota"
		set -- $list
		
		while [ $# -ge 2 ]
		do
			check_quota "$1" "$2" "$CHECKGROUPFLAGS" "normal"
			shift; shift
		done

		scan_fstab "usrjquota"
		set -- $list

		while [ $# -ge 2 ]
		do
			check_quota "$1" "$2" "$CHECKUSERFLAGS" "journaled"
			shift; shift
		done

		scan_fstab "grpjquota"
		set -- $list
		
		while [ $# -ge 2 ]
		do
			check_quota "$1" "$2" "$CHECKGROUPFLAGS" "journaled"
			shift; shift
		done
		log_action_end_msg 0
	fi
fi

# Remove special files
rm -f $quotaisoff $quotaisnew $forcequotacheck

# Turn quotas on.
if [ -x $on ] ; then
   log_action_begin_msg 'Turning on quotas';
   $on $ALLFLAGS
   log_action_end_msg 0
fi

exit 0
