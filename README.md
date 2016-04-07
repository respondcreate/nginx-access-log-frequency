
[![GitHub Logo](https://img.shields.io/coveralls/respondcreate/nginx-access-log-frequency.svg?style=flat)](https://coveralls.io/github/respondcreate/nginx-access-log-frequency)

# nginx-access-log-frequency

Determine the most frequently logged values from a standard nginx access log.

## Optional Arguments

* `-s, --segment <segment>`
                        
    The data segment whose frequency you'd like to determine. Allowed choices:

    * `status_code` (Status Code)
    * `remote_user` (Remote User)
    * `ip_address` (IP Address)
    * `http_user_agent` (User Agent)
    * `http_referrer` (Referrer)

    **Default:** `ip_address`

* `-l, --limit <limit>`

    An integer which determines the length of the list returned.

    **Default:** `10`

* `-f, --file <path-to-access-log-file>`

    The path on disk of the nginx access log you'd like evaluated.

    **Default:** `/var/log/nginx/access.log`

## Example Usage

To see a list of the top 10 most frequently logged IP addresses:

```bash
$ python nginx_access_log_frequency.py --segment ip_address --limit 10
```

To see a list of the top 5 most frequently logged user agents from a log file stored in a location other than `/var/log/nginx/access.log`:

```bash
$ python nginx_access_log_frequency.py -s http_user_agent -l 5 -f /var/log/custom-log-location/access.log
```

**NOTE:** If you've cloned down this repo and want to test this script but don't have an nginx access log handy just include `-f example-access.log` to use the included example log.

## Running Tests

Use the following command to run tests:

```bash
$ python run_tests.py
```
