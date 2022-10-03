# `clamav-api`

HTTP API on a `clamd` instance.

## `docker build`

To build a Docker image:

```bash
docker build --tag clamav-rest .
```

## `docker run`

To run the service:

```bash
docker run \
    --rm \
    --interactive \
    --tty \
    --publish 8000:8000 \
    clamav-rest
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

The OpenAPI definition will be available at <http://0.0.0.0:8000/doc>.

This should be largely functional, though the `/instream` endpoint
expects binary data and may not work with the web interface. However,
you can verify the behaviour with `curl` and the
[EICAR Anti-Virus Test File](https://en.wikipedia.org/wiki/EICAR_test_file):

```bash
curl --include \
    --request POST \
    --header 'Content-Type: application/octet-stream' \
    --header 'Accept: application/json' \
    --data 'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*' \
    http://0.0.0.0:8000/v1/instream
```

You should then receive a positive response:

```bash
{
  "output": "stream: Win.Test.EICAR_HDB-1 FOUND\u0000"
}
```
