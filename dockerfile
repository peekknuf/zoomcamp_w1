FROM debian:bullseye-slim

ENV SPARK_VERSION=3.5.1
ENV JAVA_VERSION=8u381
ENV JAVA_HOME=/usr/local/oracle-java-8/jdk1.8.0_381
ENV SPARK_HOME=/usr/local/spark-${SPARK_VERSION}-bin-hadoop3
ENV PATH=${PATH}:${SPARK_HOME}/bin

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl vim wget software-properties-common ssh net-tools \
    python3 python3-pip python3-numpy python3-matplotlib python3-scipy python3-pandas python3-psycopg2 \
    python3-venv && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /tmp/*
RUN wget -O jdk8_linux.tar.gz https://javadl.oracle.com/webapps/download/AutoDL?BundleId=248751_8c876547113c4e4aab3c868e9e0ec572 && \
    mkdir -p ${JAVA_HOME} && \
    tar -zxf jdk8_linux.tar.gz -C /usr/local/oracle-java-8/ && \
    rm jdk8_linux.tar.gz
RUN wget -O spark-${SPARK_VERSION}-bin-hadoop3.tgz https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz && \
    mkdir -p ${SPARK_HOME} && \
    tar -zxf spark-${SPARK_VERSION}-bin-hadoop3.tgz -C /usr/local/ && \
    rm spark-${SPARK_VERSION}-bin-hadoop3.tgz

WORKDIR /app
COPY pyspark_directory_ingestion.py pyspark_directory_ingestion.py 
COPY postgresql-42.7.3.jar ${SPARK_HOME}/jars
COPY unit.py unit.py

RUN pip3 install pyspark

EXPOSE 22
EXPOSE 8081

ENTRYPOINT [ "python3", "unit.py" ]
