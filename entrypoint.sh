#!/bin/bash

/etc/init.d/clamav-daemon start

export PATH="/var/lib/clamav/.local/bin:${PATH}"

exec "$@"
