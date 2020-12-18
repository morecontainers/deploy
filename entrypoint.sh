#!/bin/sh
if [ x"$1" == x"sh" ] || [ x"$1" == x"/bin/sh" ]
then
	exec "$@"
fi
exec python3 -m docker-redeploy -- "$@"
