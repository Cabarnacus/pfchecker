#!/bin/sh

# PROVIDE: gwmonitor
# REQUIRE: LOGIN
# KEYWORD: shutdown

. /etc/rc.subr

name=gwmonitor
rcvar=gwmonitor_enable  # Set gwmonitor_enable="YES" in /etc/rc.conf.local

load_rc_config $name

pidfile="/var/run/${name}.pid"
procname=/root/gatewaymonitor.py
command=/usr/sbin/daemon
command_interpreter=/usr/local/bin/python3.8
command_args="-f -r -p ${pidfile} -u root ${procname}"

run_rc_command "$1"

# You can then use "service gatewaymonitor.sh start/stop/status/enable/disable" but beware the -r flag in command_args will spin up
# another process. Kill this in usual way to fully close. "kill [PID]"