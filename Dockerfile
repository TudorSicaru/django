# Please note that this Dockerfile does not build a volume, which means the stuff stored in the sqlite3 db
# will be lost whenever you restart the container. In a real life scenario you'll have a database running on
# another server to which django would connect to send queries or to insert new data.

FROM rackspacedot/python38

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python3 -m pip install -r requirements.txt

COPY . .

RUN chmod +x /app/startup.sh

EXPOSE 8000

# Install redis cache
RUN apt-get update
RUN apt-get install -y redis-server
RUN echo supervised systemd >> /etc/redis/redis.conf

CMD ["/app/startup.sh"]
