#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Specify a path to output zipfile"
  exit 1
fi

OUTPUT=$1

# Remove outout zip to avoid appending files
[ -e "$OUTPUT" ] && rm "$OUTPUT"

# Build bundle
find . -type f -iname '*.py' -not -path './ve/*' -not -path './build/*' -exec zip "$OUTPUT" {} +
zip "$OUTPUT" requirements.txt
zip "$OUTPUT" config.ini config.production.ini
zip -r "$OUTPUT" .ebextensions/
