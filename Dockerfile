<<<<<<< HEAD
FROM vincreator/eunhamirror:latest
=======
FROM anasty17/mltb:latest
# FROM anasty17/mltb-oracle:latest
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

<<<<<<< HEAD
COPY extract /usr/local/bin
COPY pextract /usr/local/bin
RUN chmod +x /usr/local/bin/extract && chmod +x /usr/local/bin/pextract
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
COPY .netrc /root/.netrc
RUN chmod 600 /usr/src/app/.netrc
RUN chmod +x aria.sh

CMD ["bash","run.sh"]
=======
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash", "start.sh"]
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
