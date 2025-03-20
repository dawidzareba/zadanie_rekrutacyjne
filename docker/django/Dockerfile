ARG PYTHON_VERSION=3.12.7

FROM public.ecr.aws/docker/library/python:${PYTHON_VERSION} AS builder
ENV PYTHONUNBUFFERED=1
ARG requirements_version

WORKDIR /app

RUN apt-get update
RUN apt-get install -y libxml2-dev libxmlsec1-dev libxmlsec1-openssl postgresql-client libpoppler-cpp-dev

COPY ./backend/requirements /requirements

RUN python -m pip install -r /requirements/$requirements_version.txt


################################################################################
# DEV configuration
FROM builder AS development

COPY ./docker/django/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]