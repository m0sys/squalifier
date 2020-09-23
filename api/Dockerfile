# The "buster" flavor of the official docker Python image is based on Debian and includes common packages.
FROM python:3.8-buster

# Create the working directory.
RUN set -ex && mkdir / repo
WORKDIR /repo

# Copy only the relevant directories to the working directory.
COPY squat_recognizer ./squat_recognizer
COPY api/ ./api

# Install Python dependencies.
RUN set -ex && pip3 install -r api/requirements.txt

# Run the web server.
EXPOSE 8000
ENV PYTHONPATH /repo
CMD python3 /repo/api/app.py