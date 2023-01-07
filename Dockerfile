FROM mcr.microsoft.com/playwright/python:focal as build-deps

RUN apt-get update \
    && apt-get --no-install-recommends install -y python3-dev python3-pip build-essential \
    && ln -s /usr/bin/pip3 /usr/bin/pip3.8 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp/python_requirements

COPY ./requirements.txt .
COPY plugins plugins

RUN find . -name 'requirements*.txt' -print0 | while read -d $'\0' file; do pip3 install --user --no-cache-dir -r $file; done \
    && python3 -m playwright install webkit firefox chromium

FROM mcr.microsoft.com/playwright/python:focal

ENV GAMESHUB_CONF_DIR_CWD=true

COPY --from=build-deps /root/.local /root/.local
COPY . /src

WORKDIR /config

ENTRYPOINT ["python", "/src/app.py"]

