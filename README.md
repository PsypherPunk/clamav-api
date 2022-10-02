# `clamav-api`

HTTP API on a `clamd` instance.

## `Dockerfile`

We're building this on the `slim` variant of the latest Debian build:

```bash
FROM debian:buster-slim
```

In the initial `RUN` command, we install the bare necessities—ClamAV
and Python—before clearing out the `apt` cache.

After the installation of ClamAV, we run `freshclam` to get the latest
virus databases and `start`/`stop` the `clamd` instance to make sure
the initial directory structures are in place before we can switch to
a non-`root` user:

```bash
RUN apt-get update && \
    apt-get install -y clamav clamav-daemon python3 python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    freshclam && \
    /etc/init.d/clamav-daemon start && \
    /etc/init.d/clamav-daemon stop
```

We're using an `ENTRYPOINT` script (the imaginatively-titled
`entrypoint.sh`) as we want to make sure the `clamd` daemon is running
before launching the API and our `PATH` is correctly set up:

```bash
COPY ./entrypoint.sh /entrypoint.sh
…
ENTRYPOINT ["/entrypoint.sh"]
```

Finally, we set up and install the Python application. We're making
sure to use a non-`root` user (`clamav` is the user under which `clamd`
is running):

```bash
EXPOSE 8000
COPY --chown=clamav:clamav ./app /app
USER clamav
WORKDIR /app
RUN python3 -m pip install --user --no-warn-script-location -r /app/requirements/production.txt
```

## `docker build`

To build a Docker image:

```bash
docker build -t clamav-rest .
```

## `docker run`

To run the service:

```bash
docker run --rm -it -p 8000:8000 clamav-rest
```

After which, the service will start the `clamd` daemon and in turn,
the API:

```bash
[ ok ] Starting ClamAV daemon: clamd .
[2020-03-18 13:35:58 +0000] [1] [INFO] Starting gunicorn 20.0.4
[2020-03-18 13:35:58 +0000] [1] [INFO] Listening at: http://0.0.0.0:8000 (1)
[2020-03-18 13:35:58 +0000] [1] [INFO] Using worker: sync
[2020-03-18 13:35:58 +0000] [371] [INFO] Booting worker with pid: 371
```

## OpenAPI

The OpenAPI (formerly _Swagger_) definition will be available at:
[http://0.0.0.0:8000/v1/ui/](http://0.0.0.0:8000/v1/ui/)

This should be largely functional, though the `/instream` endpoint
expects binary data and may not work with the web interface. However,
you can verify the behaviour with `curl` and the
[EICAR Anti-Virus Test File](https://en.wikipedia.org/wiki/EICAR_test_file):

```bash
curl -D - -X POST \
    --header 'Content-Type: application/octet-stream' \
    --header 'Accept: application/json' \
    --data 'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*' \
    http://0.0.0.0:8000/instream
```

You should then receive a positive response:

```bash
{
  "output": "stream: Win.Test.EICAR_HDB-1 FOUND\u0000"
}
```
