FROM apache/airflow:latest

# Install build dependencies
RUN apt-get update && \
    apt-get install -y build-essential

# Set any necessary environment variables
ENV EXECUTOR=Local
ENV LOAD_EXAMPLES=yes

# Copy over any custom files needed
COPY custom_scripts/ /opt/airflow/custom_scripts/

# Set working directory
WORKDIR /opt/airflow

# Set any necessary user permissions
RUN chown -R airflow:airflow /opt/airflow/custom_scripts/

# Expose any necessary ports
EXPOSE 8080

# Start the Airflow webserver
CMD ["webserver"]