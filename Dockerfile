FROM apache/airflow:2.6.3-python3.8

# Switch to root user for system package installation
USER root

# Install git
RUN apt-get update && apt-get install -y git

# Switch back to airflow user
USER airflow

COPY requirements.txt requirements.txt

# Declare the ARG for credentials content
ARG GOOGLE_APPLICATION_CREDENTIALS_CONTENT

# Set the ENV for the path where the credentials file will be located inside the container
ENV GOOGLE_APPLICATION_CREDENTIALS=/opt/airflow/application_default_credentials.json

# Installing requirements
RUN pip install -r requirements.txt