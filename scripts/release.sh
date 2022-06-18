#!/bin/bash

CURRENT_TAG=$(git describe --tags --abbrev=0)
NEW_TAG=${1}


[[ -z ${NEW_TAG} ]] && { echo "Please specify a tag." && exit 1 ; }

echo "Running release script"
echo "current tag: ${CURRENT_TAG}"

git pull && \
    git commit --allow-empty -m "Release ${NEW_TAG}" && \
    git tag -a "${NEW_TAG}" -m "Version ${NEW_TAG}" && \
    git push --tags
