FROM apache/spark:latest

# Update packages and install Python 3 and pip3
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    ln -s /usr/bin/pip3 /usr/bin/pip

# Set environment variables
ENV PYSPARK_PYTHON=python3
ENV PYTHONUNBUFFERED=1
ENV SPARK_HOME=/usr/local/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

# Copy application code
COPY . /app

# Set the entry point
CMD ["python3", "/app/my_spark_app.py"]