#!/bin/dash

conf=iobox.conf

if [ -r $conf ]
then

	if  grep -sq Enabled=no $conf; then

		echo "Not enabled!"

	else
		echo "Enabled!"
	fi
else
	echo "No file here!"
fi

! grep -sq Enabled=yes $conf || echo "!0 is false"
grep -sq Enabled=no $conf || echo "1 is false"

