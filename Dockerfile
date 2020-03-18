FROM debian:buster-slim

RUN apt-get update && \
    apt-get install -y clamav clamav-daemon python3 python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    freshclam && \
    /etc/init.d/clamav-daemon start && \
    /etc/init.d/clamav-daemon stop

COPY ./entrypoint.sh /entrypoint.sh

EXPOSE 8000

COPY --chown=clamav:clamav ./app /app

USER clamav

WORKDIR /app

RUN python3 -m pip install --user --no-warn-script-location -r /app/requirements/production.txt

ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8000"]
