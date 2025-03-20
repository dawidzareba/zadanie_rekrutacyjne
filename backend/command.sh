#!/usr/bin/env bash

if [ "${USE_DOCKER}" == "yes" ]; then
    python $(dirname "$0")/manage.py "$@"
else
    cd $(dirname "${BASH_SOURCE[0]}")
    PROJECT_DIR=$(git rev-parse --show-toplevel)
    cd $PROJECT_DIR
    docker compose run -w /app/backend/ --rm -e DATABASE_PER_BRANCH=${DATABASE_PER_BRANCH} django python manage.py "$@"
    mytask_containers=$(docker ps --format "{{.Names}}" | grep zadanie)
    if [ "${mytask_containers}" != "" ]; then
      echo
      echo "Django container has finished it's job, but following containers are still working:"
      echo $mytask_containers
      echo "These containers may still be doing work related to the command. If you're sure they're done, you can stop them by running 'docker compose down'"
    fi
fi
