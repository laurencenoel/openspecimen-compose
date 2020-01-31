#!/bin/bash
. defaultvar.sh

cp /opt/tomcat/latest/conf/context.xml.default /opt/tomcat/latest/conf/context.xml
cp /opt/tomcat/latest/conf/openspecimen.properties.default /opt/tomcat/latest/conf/openspecimen.properties
cp /opt/tomcat/latest/conf/tomcat-users.xml.default /opt/tomcat/latest/conf/tomcat-users.xml

chown tomcat:tomcat /opt/tomcat/latest/conf/openspecimen.properties
chown tomcat:tomcat /opt/tomcat/latest/conf/context.xml
chown tomcat:tomcat /opt/tomcat/latest/conf/tomcat-users.xml


sed -i "s#§§username#${MYSQL_USER}#g" /opt/tomcat/latest/conf/context.xml
sed -i "s#§§password#${MYSQL_PASSWORD}#g" /opt/tomcat/latest/conf/context.xml
sed -i "s#§§useddatabasetype#${DATABASE_TYPE}#g" /opt/tomcat/latest/conf/context.xml
sed -i "s#§§useddatabasedriver#${DATABASE_DRIVER}#g" /opt/tomcat/latest/conf/context.xml
sed -i "s#§§host#${DATABASE_HOST}#g" /opt/tomcat/latest/conf/context.xml
sed -i "s#§§port#${DATABASE_PORT}#g" /opt/tomcat/latest/conf/context.xml
sed -i "s#§§database#${MYSQL_DATABASE}#g" /opt/tomcat/latest/conf/context.xml

sed -i "s#<database_type>#${DATABASE_TYPE}#g" /opt/tomcat/latest/conf/openspecimen.properties
sed -i "s#<data_dir>#${APP_DATA_DIR}#g" /opt/tomcat/latest/conf/openspecimen.properties
sed -i "s#<plugin_dir>#${PLUGIN_DIR}#g" /opt/tomcat/latest/conf/openspecimen.properties
sed -i "s#<log_dir>#${APP_LOG_CONF}#g" /opt/tomcat/latest/conf//openspecimen.properties

sed -i "s#§§name#${TOMCAT_ADMIN}#g" /opt/tomcat/latest/conf/tomcat-users.xml
sed -i "s#§§password#${TOMCAT_PASSWORD}#g" /opt/tomcat/latest/conf/tomcat-users.xml
