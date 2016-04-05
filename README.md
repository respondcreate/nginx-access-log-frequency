# nginx-access-log-frequency

Determine the most frequently logged values from a standard nginx access log.

Allowed data 'segments' to tally (with the -s/--segment argument):
    * ip_address: IP Address
    * remote_user: Remote User
    * status_code: Status Code
    * http_referrer: Referrer
    * http_user_agent: User Agent

## Examples
Print out a list of the top 10 most frequently logged IP addresses:

```bash
$ python nginx_access_log_frequency.py --segment ip_address --limit 10
```

Print out a list of the top 5 most frequently logged user agents from
a log file stored in a custom location:

```bash
$ python nginx_access_log_frequency.py --segment http_user_agent --limit 5
      --file /var/log/custom-log-location/access.log
```
