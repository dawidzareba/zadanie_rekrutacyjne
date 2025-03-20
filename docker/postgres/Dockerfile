FROM public.ecr.aws/docker/library/postgres:14.11

RUN apt update && apt install -y netcat-openbsd

CMD ["postgres", "-c", "jit=off", "-c", "max_locks_per_transaction=1024"]
