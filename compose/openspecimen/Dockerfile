FROM debian:jessie
ARG DEBIAN_FRONTEND=noninteractive
ARG VERSION="v6.2.x"

RUN apt-get update \
    && apt-get install -y software-properties-common apt-utils wget gnupg \
    apt-transport-https ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Setup JDK
RUN wget -qO - https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public | apt-key add - \
    && add-apt-repository --yes https://adoptopenjdk.jfrog.io/adoptopenjdk/deb/ \
    && apt-get update \
    && apt install -y adoptopenjdk-8-hotspot

# Setup tomcat and dependencies
RUN apt-get install -y build-essential libpng-dev \
    && mkdir /opt/tomcat/ \
    && useradd -r -m -U -d /opt/tomcat -s /bin/false tomcat \
    && wget https://archive.apache.org/dist/tomcat/tomcat-9/v9.0.33/bin/apache-tomcat-9.0.33.tar.gz -P /tmp/ \
    && tar xf /tmp/apache-tomcat-9*.tar.gz -C /opt/tomcat \
    && sed -i 's#allow=".*"#allow="(^.*$)"#g' /opt/tomcat/apache-tomcat-9.0.33/webapps/manager/META-INF/context.xml \
    && ln -s /opt/tomcat/apache-tomcat-9.0.33 /opt/tomcat/latest \
    && sh -c 'chmod +x /opt/tomcat/latest/bin/*.sh' \
    && chown -R tomcat:tomcat /opt/tomcat/apache-tomcat-9.0.33

# Copy config files
ADD config/build.properties /tmp/
ADD config/context.xml /opt/tomcat/latest/conf/context.xml.default
ADD config/openspecimen.properties /opt/tomcat/latest/conf/openspecimen.properties.default
ADD config/tomcat-users.xml /opt/tomcat/latest/conf/tomcat-users.xml.default

RUN mkdir -p /opt/tomcat/latest/OpenSpecimen/plugins
RUN wget https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.18/mysql-connector-java-8.0.18.jar -P /opt/tomcat/latest/lib/

ADD scripts /opt/scripts
WORKDIR /opt/scripts
RUN chmod a+x *.sh

ENTRYPOINT ["/opt/scripts/entrypoint.sh"]
