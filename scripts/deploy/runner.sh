#!/usr/bin/env bash

set -e

if [[ -z "$1" ]] || [[ -z "$2" ]]; then
  echo "PROJECT_ID and SUBMISSION_BUCKET_NAME are mandatory"
  exit 1
fi

PROJECT_ID=$1
SUBMISSION_BUCKET_NAME=$2
IMAGE_TAG="${3:-v3.0.0}"

kubectl create secret generic keys \
    --from-file=keys.yml=docker-keys.yml \
    --dry-run -o yaml | kubectl apply -f -
kubectl create secret generic secrets \
    --from-file=secrets.yml=docker-secrets.yml \
    --dry-run -o yaml | kubectl apply -f -

helm tiller run \
    helm upgrade --install \
    survey-runner \
    helm/runner \
    --set projectId=${PROJECT_ID} \
    --set submissionBucket=${SUBMISSION_BUCKET_NAME} \
    --set image.tag=${IMAGE_TAG}
