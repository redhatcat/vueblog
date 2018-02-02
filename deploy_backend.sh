#!/bin/bash

TS=$(date -u +"%Y%m%d%H%M%S")

cd backend
./build_bundle.sh deploy.zip

cd ..
eb deploy -l $TS
