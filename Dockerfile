# Stage 1 - Compile needed python dependencies
FROM python:3.6-alpine AS build
RUN apk --no-cache add \
    gcc \
    musl-dev \
    pcre-dev \
    linux-headers \
    postgresql-dev

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install pip setuptools -U
RUN pip install -r requirements.txt


# Stage 2 - Build docker image suitable for execution and deployment
FROM python:3.6-alpine AS production
RUN apk --no-cache add \
    ca-certificates \
    mailcap \
    musl \
    pcre \
    postgresql

COPY --from=build /usr/local/lib/python3.6 /usr/local/lib/python3.6
COPY --from=build /usr/local/bin/uwsgi /usr/local/bin/uwsgi

# Stage 4.2 - Copy source code
WORKDIR /app
COPY ./bin/docker_start.sh /start.sh
COPY ./bin/uwsgi.sh /uwsgi.sh
COPY ./manage.py /app/manage.py
COPY ./main.py /app/main.py
RUN mkdir /app/log

COPY ./bot /app/bot

ENV DJANGO_SETTINGS_MODULE=bot.settings

ARG SECRET_KEY=dummy

# Run collectstatic, so the result is already included in the image
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["/start.sh"]
