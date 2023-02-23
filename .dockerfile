FROM puckel/docker-airflow:2.0.2

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Install pyspark
RUN pip install pyspark

# Set environment variables
ENV SPARK_HOME=/usr/local/spark
ENV PATH=$PATH:$SPARK_HOME/bin
ENV PYSPARK_PYTHON=python3
ENV AIRFLOW_HOME=/usr/local/airflow

# Copy Spark scripts and Airflow DAGs
COPY spark-scripts/ /usr/local/spark/scripts/
COPY airflow-dags/ /usr/local/airflow/dags/

# Set command to run services
CMD ["webserver"]