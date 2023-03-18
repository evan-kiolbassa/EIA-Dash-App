FROM cassandra:latest

# Install build dependencies
RUN apt-get update && \
    apt-get install -y build-essential

COPY cassandra.yaml /etc/cassandra/cassandra.yaml
ENTRYPOINT ["cassandra", "-f"]