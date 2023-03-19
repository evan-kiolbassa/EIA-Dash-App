FROM apache/airflow:latest

# Set the user to root to run apt-get commands
USER root

RUN apt-get update && \
    apt-get install -y build-essential


COPY /custom_scripts/ /opt/airflow/custom_scripts/
WORKDIR /opt/airflow

RUN chown -R airflow:root /opt/airflow/custom_scripts/

# Switch back to the airflow user after installing the packages and changing ownership
USER airflow
# Set any necessary environment variables
ENV EXECUTOR=Local
ENV LOAD_EXAMPLES=yes



# Expose any necessary ports
EXPOSE 8080

# Start the Airflow webserver
CMD ["airflow", "webserver"]