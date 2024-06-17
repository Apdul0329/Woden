# Dockerfile
FROM confluentinc/cp-kafka-connect:7.6.1

USER root

# Add Confluent Hub client
RUN mkdir -p /tmp/confluent-hub-client && \
    wget -qO- http://client.hub.confluent.io/confluent-hub-client-latest.tar.gz | tar -xzf - -C /tmp/confluent-hub-client && \
    mv /tmp/confluent-hub-client /usr/local/confluent-hub-client && \
    ln -sf /usr/local/confluent-hub-client/bin/confluent-hub /usr/local/bin/confluent-hub

# Install the JDBC connector
RUN confluent-hub install --no-prompt confluentinc/kafka-connect-jdbc:latest

# Download MySQL JDBC driver
RUN wget -qO /usr/share/java/mysql-connector-java.jar https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.28/mysql-connector-java-8.0.28.jar

# Download PostgreSQL JDBC driver
RUN wget -qO /usr/share/java/postgresql.jar https://jdbc.postgresql.org/download/postgresql-42.2.23.jar


# Set back to the connect user
#USER appuser
