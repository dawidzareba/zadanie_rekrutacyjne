## Django template with Docker and PostgreSQL

### Getting Started
```
django-admin startproject --template=https://github.com/dawidzareba/django_template/archive/master.zip -e "ini,yml,conf,json" site_name
```

#### Then change .env file.

### Development version:
```
$ make up
```

or

```
$ docker compose up
```
In the development version, the application runs on port 8000 \
http://localhost:8000/