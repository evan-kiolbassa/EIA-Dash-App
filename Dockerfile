FROM ubuntu:20.04

# Install system dependencies
RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install python3 python3-pip openjdk-8-jre wget

# Install PySpark and dependencies
RUN pip3 install pyspark

# Install Apache Cassandra
RUN echo "deb http://www.apache.org/dist/cassandra/debian 311x main" | tee -a /etc/apt/sources.list.d/cassandra.sources.list
RUN wget -q -O - https://www.apache.org/dist/cassandra/KEYS | apt-key add -
RUN apt-get update && apt-get -y install cassandra

# Install Airflow
RUN pip3 install apache-airflow

# Install Plotly Dash and dependencies
RUN pip3 install dash pandas

# Expose Airflow port
EXPOSE 8080

# Start Cassandra and Airflow services
CMD service cassandra start && airflow webserver -p 8080