#!/bin/sh

cd /src

chown -R tor:root /var/lib/tor

su -c "nginx" -s /bin/sh nginx
su -c "tor --runasdaemon 1" -s /bin/sh tor

flask run --host=0.0.0.0