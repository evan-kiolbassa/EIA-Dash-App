FROM apache/spark:latest

# Set environment variables
ENV PYSPARK_PYTHON=python3
ENV PYTHONUNBUFFERED=1
ENV SPARK_HOME=/usr/local/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

# Copy Python dependencies and install them
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

# Copy application code
COPY . /app

# Set the entry point
CMD ["python3", "/app/my_spark_app.py"]