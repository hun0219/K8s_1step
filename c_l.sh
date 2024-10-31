#!/bin/bash

# 기본값 설정
n=${1:-10000}
nn=${2:-0}

# 요청 URL 설정
url="http://localhost:8949"

for ((i=1; i<=n; i++)); do
  echo "Request #$i"
  curl -I "$url"
  echo ""
  sleep "$nn"
done
