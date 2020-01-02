#!/usr/bin/env bash
#
# resto
#
# chkconfig: - 80 20
. /lib/lsb/init-functions

# Directories
product="peopledoc-test"
module="resto"

# Files
pidfile="/var/run/$product/$module.pid"
logfile="/var/log/$product/$module.log"
lockfile="/var/lock/subsys/$module"
configfile="/etc/$product/$module.ini"

# TODO: switch uid / gid to something else
uid=jtag
gid=jtag

isrunning() {
	if [ -f "$pidfile" ]; then
		read pid < "$pidfile"
		command=$(ps hp $pid -o %c)

		if [ "$command" == "resto" ]; then
			return 0
		fi
	fi
	return 1
}

start() {
    log_begin_msg "Starting $module"
    resto-server && log_end_msg 0 || log_end_msg 1
	touch "$lockfile"
}

profile() {
    log_begin_msg "Starting (profiling enabled /!\ not implemented /!\) $module"
    # TODO implement profiling
    resto-server && log_end_msg 0 || log_end_msg 1
	touch "$lockfile"
}

stop() {
    log_begin_msg "Stopping $module"
	if isrunning; then
		read pid < "$pidfile"
		kill "$pid"

        # TODO max wait
		while isrunning; do
			sleep 1
		done
        log_end_msg 0

		rm -f "$lockfile"

	else
        log_end_msg 0
        log_warning_msg "Not running!"
	fi
}

case "$1" in
	start)
		start
		;;

	stop)
		stop
		;;

	status)
		status -p "$pidfile" "$module"
		;;

	profile)
		profile
		;;

	restart)
		stop
		start
		;;

	condrestart)
		if isrunning; then
			stop
			start
		else
            log_warning_msg "Module $module not running!"
		fi
		;;

	*)
		echo "Usage: service $module {start|stop|restart|condrestart|profile|status}"
esac
