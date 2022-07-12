FROM mcr.microsoft.com/playwright/python:v1.24.0-focal

# Reduce the size of the image
RUN rm -rf ms-playwright/chromium* ms-playwright/firefox* ms-playwright/webkit*
RUN cd home && git clone https://github.com/lupohan44/SteamDBFreeGamesClaimer
RUN cd /home/SteamDBFreeGamesClaimer && pip3 install -r requirements.txt
# Need to re-install webkit after reduce the size of the image
RUN python3 -m playwright install webkit

ENTRYPOINT cd /home/wd && python3 /home/SteamDBFreeGamesClaimer/app.py
