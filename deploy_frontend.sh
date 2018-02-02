#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Specify the S3 bucket to deploy to"
  exit 1
fi

BUCKET=$1

TS=$(date -u +"%Y%m%d%H%M%S")

sed "s/VERSION/${TS}/" src/version.js.example > src/version.js

npm run build && \
aws s3 sync --acl public-read --sse --delete dist/ "$BUCKET"
