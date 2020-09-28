#!/bin/bash

## sed '' requirements.txt > api/requirements.txt

docker build --network=host -t squat_recognizer_api -f api/Dockerfile .  