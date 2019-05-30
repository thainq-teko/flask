#!/bin/sh


# names of binaries
DAEMON=/usr/sbin/rpc.rquotad

# check if quota are enabled
need_rquotad=0
if test -f /etc/exports && grep -q '^/' /etc/exports /etc/exports.d/* 2>/dev/null; then
	if grep -q '^[^#]*quota' /etc/fstab; then # normal quota option
        	need_rquotad=1
	elif grep -q '^[^#]*qnoenforce' /etc/fstab; then # xfs non-enforced quota
        	need_rquotad=1
	fi
fi

test -f $DAEMON || exit 0

. /lib/lsb/init-functions

# check if there are some options to rpc.rquotad
if test -f /etc/default/quota; then
	. /etc/default/quota
fi

pidp=`pidof portmap`
pidr=`pidof rpcbind`

set -e

# To start the daemon, portmap must be up and running
if [ -x $DAEMON ] && [ $need_rquotad = 1 ]; then
   if [ -z "$pidp" ] && [ -z "$pidr" ] ; then
	log_warning_msg "Not starting $DESC rpc.rquotad, because neither portmap nor rcpbind are running"
   else
	log_daemon_msg "Starting $DESC" "rpc.rquotad"
	start-stop-daemon --start --quiet --exec $DAEMON -- $RPCRQUOTADOPTS
	log_end_msg $?
   fi
fi	

exit 0
