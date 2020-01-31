# openspecimen-compose

Docker-compose file (and dockerfile to build the associated image) to run openspecimen. Inspired by https://github.com/bibbox/app-openspecimen.


# Env variables

Several environment variables can be set in .env/openspecimen-web.
You should change at least set a custom value for TOMCAT_ADMIN and TOMCAT_PASSWORD

*NB: The default openspecimen user will always be 'admin' with the password 'Login@123'*
*You should change the password as soon as possible* 

| Variable name       | Default value                             | Info                                                  |
|---------------------|-------------------------------------------|-------------------------------------------------------|
| DATABASE_HOST       | mysql                                     | Needs to be the name of the service in docker-compose |
| MYSQL_DATABASE      | openspecimen                              | The name of the database to create and interact with  |
| MYSQL_USER          | openspecimen                              | The database user                                     |
| MYSQL_PASSWORD      | openspecimen                              | Password for the MYSQL_USER                           |
| MYSQL_ROOT_PASSWORD | password                                  | Mysql root password                                   |
| RELEASEURL          | https://github.com/krishagni/openspecimen | URL for the github repository for the source code     |
| RELEASEBRANCH       | v6.3.x                                    | Branch to checkout to                                 |
| APP_HOME            | /opt/tomcat                               |                                                       |
| APP_DATA_DIR        | /opt/openspecimen/os-data                 |                                                       |
| APP_LOG_CONF        | None                                      |                                                       |
| PLUGIN_DIR          | /opt/openspecimen/os-plugins              |                                                       |
| TOMCAT_ADMIN        | admin                                     | User for tomcat manager.                              |
| TOMCAT_PASSWORD     | admin                                     | Password for tomcat manager                           |

# Bugfixes

There are some bugfixes in the dockerfile, namely 'JAVA_TOOL_OPTIONS=-Dfile.encoding=UTF8' in the env file,
and `sed -i 's#mavenCentral()#maven { url "https://repo.maven.apache.org/maven2" }#g'` in build_war.sh to fix the https issue.

