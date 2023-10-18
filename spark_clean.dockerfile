FROM debian:bullseye-slim

ENV SPARK_VERSION=3.5.0
ENV JAVA_VERSION=8u381
ENV JAVA_HOME=/usr/local/oracle-java-8/jdk1.8.0_381
ENV SPARK_HOME=/usr/local/spark-${SPARK_VERSION}-bin-hadoop3
ENV PATH=${PATH}:/venv/bin:${SPARK_HOME}/bin

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl vim wget software-properties-common ssh net-tools \
    wamerican wamerican-insane wbrazilian wdutch wbritish-large \
    python3 python3-pip python3-numpy python3-matplotlib python3-scipy python3-pandas python3-simpy python3-psycopg2 \
    python3-venv && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /tmp/*
RUN wget -O jdk8_linux.tar.gz https://javadl.oracle.com/webapps/download/AutoDL?BundleId=248751_${JAVA_VERSION} && \
    mkdir -p ${JAVA_HOME} && \
    tar -zxf jdk8_linux.tar.gz -C /usr/local/oracle-java-8/ && \
    rm jdk8_linux.tar.gz
RUN wget -O spark-${SPARK_VERSION}-bin-hadoop3.tgz https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz && \
    mkdir -p ${SPARK_HOME} && \
    tar -zxf spark-${SPARK_VERSION}-bin-hadoop3.tgz -C /usr/local/ && \
    rm spark-${SPARK_VERSION}-bin-hadoop3.tgz

WORKDIR /app
COPY uploading_data.py uploading_data.py
COPY postgresql-42.6.0.jar ${SPARK_HOME}/jars

EXPOSE 22
EXPOSE 8081

ENTRYPOINT ["python", "uploading_data.py"]