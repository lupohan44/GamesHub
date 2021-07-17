FROM mcr.microsoft.com/playwright:focal

RUN apt-get update && apt-get install -y wget
RUN mkdir docker_tmp
RUN cd docker_tmp
RUN wget "https://raw.githubusercontent.com/lupohan44/SteamDBFreeGamesClaimer/main/requirements.txt"
RUN pip3 install -r requirements.txt
RUN cd .. && rm -rf docker_tmp

ENTRYPOINT cd /home/SteamDBFreeGamesClaimer && python3 app.py