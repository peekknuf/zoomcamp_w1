FROM debian:latest

WORKDIR /home/
RUN apt-get update && apt-get install -y curl vim wget software-properties-common ssh net-tools wamerican wamerican-insane wbrazilian wdutch wbritish-large
RUN apt-get install -y python3 python3-pip python3-numpy python3-matplotlib python3-scipy python3-pandas python3-simpy python3-psycopg2
RUN apt-get install -y python3-venv

RUN ln -s /usr/bin/python3 /usr/bin/python 
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN /venv/bin/pip install pyspark

RUN wget -O jdk8_linux.tar.gz https://javadl.oracle.com/webapps/download/AutoDL?BundleId=248751_8c876547113c4e4aab3c868e9e0ec572 
RUN mkdir -p /usr/local/oracle-java-8
RUN tar -zxf jdk8_linux.tar.gz -C /usr/local/oracle-java-8/
RUN rm jdk8_linux.tar.gz
ENV JAVA_HOME="/usr/local/oracle-java-8/jdk1.8.0_381"

RUN wget -O spark-3.5.0-bin-hadoop3.tgz https://dlcdn.apache.org/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz
RUN mkdir -p /usr/local/spark-3.5.0
RUN tar -zxf spark-3.5.0-bin-hadoop3.tgz -C /usr/local/
RUN rm spark-3.5.0-bin-hadoop3.tgz
ENV SPARK_HOME="/usr/local/spark-3.5.0-bin-hadoop3"

ENV PATH=$PATH:/usr/bin/python3
ENV PATH=$PATH:$SPARK_HOME/bin

COPY postgresql-42.6.0.jar /usr/local/spark-3.5.0-bin-hadoop3/jars

EXPOSE 22
EXPOSE 8081

WORKDIR /app
COPY uploading_data.py uploading_data.py 
RUN chmod +x /app/uploading_data.py
ENTRYPOINT [ "python", "uploading_data.py" ]