#!/bin/bash

sed '' requirements.txt > api/requirements.txt

sudo docker build -t squat_recognizer_api -f api/Dockerfile . 