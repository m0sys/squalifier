#!/bin/bash

## sed '' requirements.txt > api/requirements.txt

docker build --network=host -t gcr.io/$PROJECT_ID/squat_recognizer_api:$GITHUB_SHA -f api/Dockerfile .  