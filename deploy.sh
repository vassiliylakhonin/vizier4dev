#!/bin/sh
# Publish the demo to Cloudflare Pages.
#
# Uses the wrangler login already on this machine, so there is no API token
# to create and no secret to store. Only the four files copied below are
# served; the repository itself stays private.

set -eu

cd "$(dirname "$0")"

out=$(mktemp -d)
trap 'rm -rf "$out"' EXIT

cp index.html landing.html robots.txt _headers "$out/"

npx --yes wrangler@latest pages deploy "$out" \
  --project-name=vizier4dev \
  --branch=main \
  --commit-dirty=true
