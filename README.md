# IP Tools Web

Python web app with various IP Subnet/CIDR tools.

## Install

Download either source or release file and put somewhere on your filesystem.

### Build Virtual environment

Poetry is used to build the virtual environment although
any other venv tools can be used to build it. Pipx is a good way to [install
poetry](https://python-poetry.org/docs/#installing-with-pipx) although you
can use any of the install methods listed
[here](https://python-poetry.org/docs/#installation)

```console
poetry install --nodev
```

### Configuration

Copy the [examples/env.example](examples/env.example) to `.env` in ipwebtools
root folder (not in the package folder.)

Make sure to change the `SECRET_KEY` and `CSRF_SECRET` in the `.env` file
and also set `DEBUG=False` for a production environment.

#### Maxmind GeoIP

By default the IP Whois information is gathered on the IP Info tool. To add additional
GeoIP information from Maxmind configure the following:

```ini
GEOIP_ENABLED=True
GEOIP_USER_ID=12344
GEOIP_API_KEY=ApISecrEt
```

To use Maxmind paid service change GEOIP_HOST to geoip.maxmind.com, default host is
geolite.info.

```ini
# Maxmind paid service
GEOIP_HOST=geoip.maxmind.com
```

```ini
# Maxmind Lite service (default)
GEOIP_HOST=geolite.info
```

More information on Maxmind services are available [here](https://dev.maxmind.com/geoip).
Testing has only been done with GeoLite2 City database but should work with the paid version.

## Running development server

Run the helper app directly. Use poetry or another virtual environment.

```console
poetry shell
python3 app.py
```

With uvicorn.

```console
poetry shell
uvicorn --reload --log-level debug ipwebtools:app
```

With gunicorn through the uvicorn worker class, this will use gunicorn
default listen address and port. Use `-b <LISTEN>:<PORT>` to change that.

```console
 gunicorn -k ipwebtools.workers.ConfigurableWorker ipwebtools:app
```

## Systemd service

Create a systemd unit file to start the ipwebtools service at startup.
An example unit file [examples/ipwebtools.service](examples//ipwebtools.service)
can be used and edited as needed.

```console
cp examples/ipwebtools.service /etc/systemd/system/ipwebtools.service
```

Edit the file and change the following as needed `WorkingDirectory`,
`User`, `Group`. Also alter `PATH` and `VIRTUAL_ENV`
Environment variables to match your install location.

Make the log directory used by the service (gunicorn logs). Set `LOG_DIR` in
the `.env` file to change this if required and change the username to the
same user and group as in the unit file.

```console
mkdir /var/log/ipwebtools/
chown www-data.www-data /var/log/ipwebtools/
```

By default it runs on port 8000 and listens only on localhost. Change
this in the `.env` file.

Finally enable the service

```console
systemctl daemon-reload
systemctl enable ipwebtools.service
systemctl start ipwebtools.service
```

## Nginx configuration

A reverse proxy via Nginix is optional but recommeded step. If the pages are
served under a sub path modify the `ROOT_PATH` in `.env`
to match for example `ROOT_PATH=/iptools`

See [examples/nginx.conf](examples/nginx.conf) and
[examples/nginx-subpath.conf](examples/nginx-subpath.conf) configuration for
a base to get started.
