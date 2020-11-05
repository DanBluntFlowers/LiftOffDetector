FROM puckel/docker-airflow:1.10.9
COPY . /opt/app
WORKDIR /opt/app
USER root

# install Java
#RUN echo "deb http://security.debian.org/debian-security stretch/updates main" >> /etc/apt/sources.list                                                   
#RUN mkdir -p /usr/share/man/man1 && \
#    apt-get update -y && \
#    apt-get install -y openjdk-8-jdk

#RUN apt-get install unzip -y && \
#    apt-get autoremove -y


# Setup dependencies for pyodbc
RUN \
  export ACCEPT_EULA='Y' && \
  export MYSQL_CONNECTOR='mysql-connector-odbc-8.0.18-linux-glibc2.12-x86-64bit' && \
  export MYSQL_CONNECTOR_CHECKSUM='f2684bb246db22f2c9c440c4d905dde9' && \
  apt-get update && \
  apt-get install -y git &&\
  apt-get install ca-certificates && \
  apt-get install -y curl build-essential unixodbc-dev g++ apt-transport-https gnupg dirmngr && \
  #gpg --keyserver hkp://keys.gnupg.net --recv-keys 5072E1F5 && \
  (gpg --keyserver ha.pool.sks-keyservers.net --recv-keys "5072E1F5" \
  || gpg --keyserver pgp.mit.edu --recv-keys "5072E1F5" \
  || gpg --keyserver keyserver.pgp.com --recv-keys "5072E1F5") && \
  #
  # Install pyodbc db drivers for MSSQL, PG and MySQL
  curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
  curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
  curl -L -o ${MYSQL_CONNECTOR}.tar.gz https://dev.mysql.com/get/Downloads/Connector-ODBC/8.0/${MYSQL_CONNECTOR}.tar.gz && \
  curl -L -o ${MYSQL_CONNECTOR}.tar.gz.asc https://downloads.mysql.com/archives/gpg/\?file\=${MYSQL_CONNECTOR}.tar.gz\&p\=10 && \
  gpg --verify ${MYSQL_CONNECTOR}.tar.gz.asc && \
  echo "${MYSQL_CONNECTOR_CHECKSUM} ${MYSQL_CONNECTOR}.tar.gz" | md5sum -c - && \
  apt-get update && \
  gunzip ${MYSQL_CONNECTOR}.tar.gz && tar xvf ${MYSQL_CONNECTOR}.tar && \
  cp ${MYSQL_CONNECTOR}/bin/* /usr/local/bin && cp ${MYSQL_CONNECTOR}/lib/* /usr/local/lib && \
  myodbc-installer -a -d -n "MySQL ODBC 8.0 Driver" -t "Driver=/usr/local/lib/libmyodbc8w.so" && \
  myodbc-installer -a -d -n "MySQL ODBC 8.0" -t "Driver=/usr/local/lib/libmyodbc8a.so" && \
  apt-get install -y msodbcsql17 odbc-postgresql && \
  #
  # Update odbcinst.ini to make sure full path to driver is listed
  sed 's/Driver=psql/Driver=\/usr\/lib\/x86_64-linux-gnu\/odbc\/psql/' /etc/odbcinst.ini > /tmp/temp.ini && \
  mv -f /tmp/temp.ini /etc/odbcinst.ini && \
  # Install dependencies
  pip install --upgrade pip && \
  python -m pip install nltk && \
  update-ca-certificates -f && \
  python -c 'import nltk; nltk.download("stopwords", download_dir="/usr/local/lib/nltk_data")' && \
  pip install -r requirements.txt && rm requirements.txt && \
  python -m spacy download fr_core_news_md && \
  python -m pip install git+https://github.com/boudinfl/pke.git && \
  # Cleanup build dependencies
  rm -rf ${MYSQL_CONNECTOR}* && \
  apt-get remove -y curl apt-transport-https debconf-utils g++ gcc rsync unixodbc-dev build-essential gnupg2 && \
  apt-get autoremove -y && apt-get autoclean -y

#RUN update-ca-certificates -f \
#  && apt-get update \
#  && apt-get upgrade -y \
#  && apt-get install -y \
#    wget \
#    git \
#    libatlas3-base \
#    libopenblas-base \
#  && apt-get clean

# Java
#RUN cd /opt/ \
#    && wget \
#	--no-cookies \
#	--no-check-certificate \
#	--header "Cookie: oraclelicense=accept-securebackup-cookie" \
#	"https://javadl.oracle.com/webapps/download/AutoDL?BundleId=242980_a4634525489241b9a9e1aa73d9e118e6" \
#	-O jdk-8.tar.gz \
#    && tar xzf jdk-8.tar.gz \
#    && rm jdk-8.tar.gz \
#    && update-alternatives --install /usr/bin/java java /opt/jdk1.8.0_151/bin/java 100 \
#    && update-alternatives --install /usr/bin/jar jar /opt/jdk1.8.0_151/bin/jar 100 \
#    && update-alternatives --install /usr/bin/javac javac /opt/jdk1.8.0_151/bin/javac 100


# Airflow
ARG AIRFLOW_USER_HOME=/usr/local/airflow
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}


COPY script/entrypoint.sh /entrypoint.sh
COPY config/airflow.cfg ${AIRFLOW_USER_HOME}/airflow.cfg

RUN chown -R airflow: ${AIRFLOW_USER_HOME}

EXPOSE 8080 5555 8793

USER airflow
WORKDIR ${AIRFLOW_USER_HOME}
ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"]
