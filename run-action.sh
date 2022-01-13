#!/bin/bash

curl \
  -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token $1" \
  https://api.github.com/repos/Ironem/LabsPFE/actions/workflows/17417990/dispatches \
  -d '{"ref":"main", inputs: {name: $@:2 } }'
