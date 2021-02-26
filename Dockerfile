ARG PYTHON_VERSION=3.9.1-alpine

FROM python:${PYTHON_VERSION} AS builder
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/app/wheels
WORKDIR /usr/src/app/wheels

COPY requirements.txt ./
RUN     apk add --no-cache --virtual .build-deps gcc musl-dev && \
        pip wheel -r requirements.txt

###

FROM python:${PYTHON_VERSION} AS BUILD
ARG USER=app
ARG USER_UID=1000
ARG USER_GID=1000

ENV PYTHONUNBUFFERED 1

ENV bot_token="S3CR3TP@55W0RD"
ENV server_ip="127.0.0.1"
ENV mc_version="mc_version"
ENV whitelist_location="/config/whitelist.json"
ENV adminlist_location="/config/adminlist.json"
ENV requests_location="/config/requests.pk1"

WORKDIR /usr/src/app

COPY --from=builder /usr/src/app/wheels /usr/src/app/wheels
RUN     pip install -r ./wheels/requirements.txt \
                    -f ./wheels && \
        rm -rf ./wheels /root/.cache/pip/* && \
        addgroup --gid "${USER_GID}" "${USER}" && \
        adduser --disabled-password --gecos "" --no-create-home --home "/usr/src/app" \
                --ingroup "${USER}" --uid "${USER_UID}" "${USER}"

COPY bot.py ./
COPY modules ./modules/

USER "${USER}"
CMD [ "python3", "./bot.py" ]
