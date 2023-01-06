FROM mcr.microsoft.com/playwright/python:focal as build-deps

RUN apt-get update \
    && apt-get --no-install-recommends install -y python3-dev python3-pip build-essential \
    && ln -s /usr/bin/pip3 /usr/bin/pip3.8 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp/python_requirements

COPY ./requirements.txt .
COPY plugins plugins

RUN find . -name 'requirements.txt' -exec bash -c "pip3 install --user --no-cache-dir -r {}" \; \
    && python3 -m playwright install webkit firefox chromium

FROM mcr.microsoft.com/playwright/python:focal

COPY --from=build-deps /root/.local /root/.local


ENV GAMESHUB_SRC_DIR=/src
WORKDIR /src
COPY . .

WORKDIR /config

ENTRYPOINT ["python", "/src/app.py"]

