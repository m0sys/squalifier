#!/bin/bash

gcloud run deploy "$SERVICE_NAME" \
      --quiet \
      --region "$RUN_REGION" \
      --image "gcr.io/$PROJECT_ID/squat_recognizer_api:$GITHUB_SHA" \
      --platform "managed" \
      --allow-unauthenticated \
      --memory "3096M" \
      --timeout 30
