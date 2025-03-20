#!/usr/bin/env bash
set -e

cd "$(dirname "${BASH_SOURCE[0]}")"
PROJECT_DIR=$(git rev-parse --show-toplevel)
PROJECT_NAME=$(basename "${PROJECT_DIR}")

running_containers=$(docker ps -f name="${PROJECT_NAME}"_* -aq)

if [[ $running_containers ]]; then
    echo "Stopping running containers..."
    docker stop "$running_containers"
fi

while [[ $# -gt 0 ]]
do
    key="$1"
    case $key in
        -b|--remove_db_volume)
        remove_db_volume=true
        shift
        ;;
        -f|--force)
        force=true
        shift
        ;;
        *)
        shift
    esac
done

echo "This will delete your current database (your entire data) and create new one using fixtures."

if [ "${force}" != "true" ]; then
    read -r -p "Are you sure? [y/N] " response

    if ! [[ "$response" =~ ^([yY][eE][sS]|[yY])+$ ]]
    then
        exit 1
    fi
fi

echo "Removing unused containers (this may take a while)..."
docker container prune --force

echo "Removing docker volumes..."
if [ "${remove_db_volume}" = true ]; then
    volumes="${PROJECT_NAME}_postgres_data ${volumes}"
else
    echo "Postgres database volume will not be removed"
fi
docker volume rm -f "${volumes}"

echo "Clearing cache..."
make command clear_cache --all --skip-checks
echo "Recreating empty database..."
make command recreate_empty_database
echo "Running migrations..."
# shellcheck disable=SC2154
if [ "${with_migrations}" = true ]; then
    make command migrate
else
    make command migrate --run-syncdb
    make command migrate --fake
fi
echo "Checking apps initial data..."
make command check_apps_initial_data

echo "Done."