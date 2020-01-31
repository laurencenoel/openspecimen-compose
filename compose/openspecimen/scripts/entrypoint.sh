#!/bin/bash

. defaultvar.sh

/opt/scripts/build_war.sh

# Setting up config files
/opt/scripts/customize_files.sh

echo "Wait for DB server to be ready"
/opt/scripts/waitforit.sh "${DATABASE_HOST}:${DATABASE_PORT}"

/opt/tomcat/latest/bin/catalina.sh start

tail -f /opt/tomcat/latest/logs/catalina.out
