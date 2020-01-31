if [ -f  /opt/tomcat/latest/webapps/openspecimen.war ]; then
    echo ".war file found. Skipping build"
    exit 0
fi

echo "Building .war file"
. defaultvar.sh


GRADLE_HOME="/opt/gradle/gradle-2.0"
PATH="${GRADLE_HOME}/bin:${PATH}"

wget https://services.gradle.org/distributions/gradle-2.0-bin.zip -P /tmp
apt-get install -y unzip curl git
unzip -d /opt/gradle /tmp/gradle-*.zip
curl -sL https://deb.nodesource.com/setup_10.x | bash -
apt-get install -y nodejs
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash
cd /tmp
git clone $RELEASEURL
rm /tmp/openspecimen/build.properties
rm /opt/tomcat/latest/conf/context.xml
cd openspecimen/www/
npm install --loglevel=error
npm install --loglevel=error -g grunt gulp-cli bower
npm audit fix
bower install --allow-root
apt remove -y unzip curl
rm -rf /var/lib/apt/lists/*

cd /tmp/openspecimen
git checkout $RELEASEBRANCH
mv /tmp/build.properties /tmp/openspecimen/

sed -i "s#<app_container_home>#${APP_HOME}#g" /tmp/openspecimen/build.properties
sed -i "s#<app_data_dir>#${APP_DATA_DIR}#g" /tmp/openspecimen/build.properties

sed -i "s/<database_type>/${DATABASE_TYPE}/g" /tmp/openspecimen/build.properties
sed -i "s/<database_host>/${DATABASE_HOST}/g" /tmp/openspecimen/build.properties
sed -i "s/<database_port>/${DATABASE_PORT}/g" /tmp/openspecimen/build.properties
sed -i "s/<database_name>/${MYSQL_DATABASE}/g" /tmp/openspecimen/build.properties
sed -i "s/<database_username>/${MYSQL_USER}/g" /tmp/openspecimen/build.properties
sed -i "s/<database_password>/${MYSQL_PASSWORD}/g" /tmp/openspecimen/build.properties

sed -i "s/app_log_conf =/app_log_conf = ${APP_LOG_CONF}/g" /tmp/openspecimen/build.properties
sed -i "s#<datasource_jndi>#${DATASOURCE_JNDI}#g" /tmp/openspecimen/build.properties
sed -i "s/<deployment_type>/${DEVELOPMENT_TYPE}/g" /tmp/openspecimen/build.properties
sed -i "s/<show_sql>/${SHOW_SQL}/g" /tmp/openspecimen/build.properties
sed -i "s#<plugin_dir>#${PLUGIN_DIR}#g" /tmp/openspecimen/build.properties

# TEMPFIX

sed -i 's#mavenCentral()#maven { url "https://repo.maven.apache.org/maven2" }#g' /tmp/openspecimen/build.gradle

# Build WAR file
gradle build
cp build/libs/openspecimen.war /opt/tomcat/latest/webapps/
rm -rf /tmp/openspecimen
apt remove -y git
