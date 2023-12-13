FROM ibmcom/websphere-traditional:8.5.5.24-ubi8

# Manadatory Env vars:
ENV ORACLE_JDBC_DRIVER_PATH=/work/wasconf/db-drivers/oracle
ENV DB2UNIVERSAL_JDBC_DRIVER_PATH=/work/wasconf/db-drivers/db2
ENV UNIVERSAL_JDBC_DRIVER_PATH=/work/wasconf/db-drivers/db2

RUN mkdir -p /work/wasconf/shlibs/esposizioneContratti/
RUN mkdir -p /work/wasconf/db-drivers/db2
RUN mkdir -p /work/wasconf/db-drivers/oracle
RUN mkdir -p /work/wasconf/db-drivers/m_sql


# Copy shared libs
COPY jar/commons-codec-1.4.jar /work/wasconf/shlibs/esposizioneContratti/commons-codec-1.4.jar
COPY jar/commons-httpclient-3.1.jar /work/wasconf/shlibs/esposizioneContratti/commons-httpclient-3.1.jar
COPY jar/httpcore-4.4.10.jar /work/wasconf/shlibs/esposizioneContratti/httpcore-4.4.10.jar
COPY jar/httpclient-4.5.6.jar /work/wasconf/shlibs/esposizioneContratti/httpclient-4.5.6.jar
COPY jar/neethi-3.0.3.jar /work/wasconf/shlibs/esposizioneContratti/neethi-3.0.3.jar
COPY jar/woden-core-1.0M10.jar /work/wasconf/shlibs/esposizioneContratti/woden-core-1.0M10.jar
COPY jar/axis2-transport-local-1.7.8.jar /work/wasconf/shlibs/esposizioneContratti/axis2-transport-local-1.7.8.jar
COPY jar/axis2-transport-http-1.7.8.jar /work/wasconf/shlibs/esposizioneContratti/axis2-transport-http-1.7.8.jar
COPY jar/axis2-kernel-1.7.8.jar /work/wasconf/shlibs/esposizioneContratti/axis2-kernel-1.7.8.jar
COPY jar/axis2-adb-1.7.8.jar /work/wasconf/shlibs/esposizioneContratti/axis2-adb-1.7.8.jar
COPY jar/axiom-impl-1.2.20.jar /work/wasconf/shlibs/esposizioneContratti/axiom-impl-1.2.20.jar
COPY jar/axiom-api-1.2.20.jar  /work/wasconf/shlibs/esposizioneContratti/axiom-api-1.2.20.jar

# Copy jdbc drivers
## DB2
COPY drivers/db2/db2jcc_license_cisuz.jar /work/wasconf/db-drivers/db2/db2jcc_license_cisuz.jar
COPY drivers/db2/db2jcc_license_cu.jar /work/wasconf/db-drivers/db2/db2jcc_license_cu.jar
COPY drivers/db2/db2jcc.jar /work/wasconf/db-drivers/db2/db2jcc.jar
COPY drivers/db2/db2jcc4.jar /work/wasconf/db-drivers/db2/db2jcc4.jar
## ORACLE
COPY drivers/oracle/ojdbc8.jar /work/wasconf/db-drivers/oracle/ojdbc8.jar
## SQL SERVER
COPY drivers/m_sql/sqljdbc4.jar /work/wasconf/db-drivers/sqljdbc4.jar

# Copy EAR
COPY app.ear /work/config/app.ear

# Copy configurations (this need to be extracted)
COPY custom-urls.csv /tmp/custom-urls.csv
COPY custom-users.csv /tmp/custom-users.csv
COPY custom-datasources.csv /tmp/custom-datasources.csv
COPY custom-shared-libs.csv /tmp/custom-shared-libs.csv

# Copy custom scripts
COPY add_custom_url.py /work/config/add_custom_url.py
COPY add_shared_libs.py /work/config/add_shared_libs.py
COPY add_datasources.py /work/config/add_datasources.py
COPY install_app.py /work/config/install_app.py

COPY was-config.props /work/config/was-config.props
RUN /work/configure.sh
