FROM weihan/webdriver-python
MAINTAINER redshoga
RUN set -x && \
    pip3 install httplib2 pyvirtualdisplay tweepy && \
    apt-get install -y cron busybox-static && \
    echo '*/10 * * * * python3 /main/tweet.py' >> /var/spool/cron/crontabs/root
    CMD ["busybox", "crond", "-f", "-L", "/dev/stderr"]
