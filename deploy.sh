#!/bin/sh
# Publish the demo to Cloudflare Pages.
#
# Uses an existing local Wrangler login, or CLOUDFLARE_API_TOKEN and
# CLOUDFLARE_ACCOUNT_ID in CI. Only the four files copied below are served.

set -eu

cd "$(dirname "$0")"

python3 scripts/check_static.py

out=$(mktemp -d)
trap 'rm -rf "$out"' EXIT

cp index.html landing.html robots.txt _headers "$out/"

npx --yes wrangler@4 pages deploy "$out" \
  --project-name=vizier4dev \
  --branch=main \
  --commit-dirty=true
