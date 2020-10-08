#!/bin/bash

gcloud run deploy "$SERVICE_NAME" \
      --quiet \
      --image gcr.io/squalify/squat_recognizer_api
      --region "$RUN_REGION" \
      --platform "managed" \
      --allow-unauthenticated \
      --memory "3096M"
      --timeout 30
