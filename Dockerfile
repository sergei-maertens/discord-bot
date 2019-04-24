# Stage 1 - Compile needed python dependencies
FROM python:3.7-alpine AS build
RUN apk --no-cache add \
    gcc \
    musl-dev \
    pcre-dev \
    linux-headers \
    postgresql-dev
    # python3-dev
    # libraries installed using git
    # git \
    # lxml dependencies
    # libxslt-dev \
    # pillow dependencies
    # jpeg-dev \
    # openjpeg-dev \
    # zlib-dev

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install pip setuptools -U
RUN pip install -r requirements.txt


# Stage 4 - Build docker image suitable for execution and deployment
FROM python:3.7-alpine AS production
RUN apk --no-cache add \
    ca-certificates \
    mailcap \
    musl \
    pcre \
    postgresql
    # lxml dependencies
    # libxslt \
    # pillow dependencies
    # jpeg \
    # openjpeg \
    # zlib \
    # nodejs

COPY --from=build /usr/local/lib/python3.7 /usr/local/lib/python3.7
COPY --from=build /usr/local/bin/uwsgi /usr/local/bin/uwsgi

# Stage 4.2 - Copy source code
WORKDIR /app
COPY ./bin/docker_start.sh /start.sh
COPY ./bin/uwsgi.sh /uwsgi.sh
COPY ./manage.py /app/manage.py
RUN mkdir /app/log

COPY ./bot /app/bot

ENV DJANGO_SETTINGS_MODULE=bot.settings

ARG SECRET_KEY=dummy

# Run collectstatic, so the result is already included in the image
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["/start.sh"]
