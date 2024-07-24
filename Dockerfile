FROM debian:bullseye-slim

RUN apt-get update && \
    apt-get install -y clamav clamav-daemon python3 python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    freshclam && \
    /etc/init.d/clamav-daemon start && \
    /etc/init.d/clamav-daemon stop

COPY ./entrypoint.sh /entrypoint.sh

EXPOSE 8000

COPY --chown=clamav:clamav ./clamav /clamav/clamav/
COPY --chown=clamav:clamav ./requirements/base.txt /tmp/requirements.txt

USER clamav

WORKDIR /clamav

RUN python3 -m pip install \
    --user \
    --no-warn-script-location \
    --requirement /tmp/requirements.txt && \
    rm /tmp/requirements.txt

ENTRYPOINT ["/entrypoint.sh"]

CMD ["uvicorn", "clamav:app", "--host", "0.0.0.0", "--port", "8000"]
