RELEASEURL="${RELEASEURL:-https://github.com/krishagni/openspecimen}"
RELEASEBRANCH="${RELEASEBRANCH:-v6.3.x}"
APP_HOME="${APP_HOME:-/opt/tomcat}"
APP_DATA_DIR="${APP_DATA_DIR:-/opt/openspecimen/os-data}"
APP_LOG_CONF="${APP_LOG_CONF:-}"
DATASOURCE_JNDI="${DATASOURCE_JNDI:-java:/comp/env/jdbc/openspecimen}"
DEVELOPMENT_TYPE="${DEVELOPMENT_TYPE:-fresh}"
DATABASE_TYPE="${DATABASE_TYPE:-mysql}"
DATABASE_HOST="${DATABASE_HOST:-mysql}"
DATABASE_PORT="${DATABASE_PORT:-3306}"
DATABASE_DRIVER="${DATABASE_DRIVER:-com.mysql.jdbc.Driver}"
MYSQL_DATABASE="${MYSQL_DATABASE:-openspecimen}"
MYSQL_USER="${MYSQL_USER:-openspecimen}"
MYSQL_PASSWORD="${MYSQL_PASSWORD:-openspecimen}"
SHOW_SQL="${SHOW_SQL:-false}"
PLUGIN_DIR="${PLUGIN_DIR:-/opt/openspecimen/os-plugins}"
TOMCAT_ADMIN="${TOMCAT_ADMIN:-admin}"
TOMCAT_PASSWORD="${TOMCAT_PASSWORD:-admin}"
