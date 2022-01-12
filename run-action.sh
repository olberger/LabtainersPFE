#!/bin/bash

curl \
  -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token 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" \
  https://api.github.com/repos/Ironem/LabsPFE/actions/workflows/17417990/dispatches \
  -d '{"ref":"main" }'