FROM mcr.microsoft.com/playwright:focal
  
RUN rm -rf ms-playwright/chromium* ms-playwright/firefox*
RUN cd home && git clone https://github.com/lupohan44/SteamDBFreeGamesClaimer
RUN cd /home/SteamDBFreeGamesClaimer && pip3 install -r requirements.txt

ENTRYPOINT cd /home/wd && python3 /home/SteamDBFreeGamesClaimer/app.py