# The "buster" flavor of the official docker Python image is based on Debian and includes common packages.
FROM python:3.8.5-buster

# Create the working directory.
RUN set -ex && mkdir /repo
WORKDIR /repo

ENV PORT 8080

# Copy only the relevant directories to the working directory.
COPY squat_recognizer ./squat_recognizer
COPY api/ ./api
COPY data/raw ./data/raw

# Install Python dependencies.
RUN set -ex && pip3 install -r api/requirements.txt --find-links https://download.pytorch.org/whl/torch_stable.html

# Run the web server.
EXPOSE $PORT
ENV PYTHONPATH /repo
CMD python3 /repo/api/graphql_app.py