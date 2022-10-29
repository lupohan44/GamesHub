FROM mcr.microsoft.com/playwright/python:v1.23.0-focal

# Reduce the size of the image
RUN cd home && git clone https://github.com/lupohan44/GamesHub
RUN cd /home/GamesHub && pip3 install -r requirements.txt
# Need to re-install webkit after reduce the size of the image
RUN python3 -m playwright install webkit firefox chromium

ENTRYPOINT cd /home/wd && python3 /home/GamesHub/app.py
