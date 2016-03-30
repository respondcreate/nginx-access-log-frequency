from __future__ import print_function
from collections import Counter
import io
import re

# Arguments to set
FILE = 'access.log'
LIMIT = 10
SEGMENT_TO_COUNT = 'ip_address'

nginx_access_log_regex = re.compile(
    r'(?P<ip_address>.*?)\ \-\ (?P<remote_user>.*?)\ \[(?P<time_local>.*?)\]'
    r'\ \"(?P<request>.*?)\"\ (?P<status>.*?)\ (?P<body_bytes_sent>.*?)\ '
    r'\"(?P<http_referer>.*?)\"\ \"(?P<http_user_agent>.*?)\"',
    re.IGNORECASE
)

with io.open(FILE, 'r') as log_file:
    c = Counter([
        nginx_access_log_regex.match(line).group(SEGMENT_TO_COUNT)
        for line in log_file.readlines()
    ])


table_header = (
    "Top {limit} Most Frequently Logged IP Addresses".format(limit=LIMIT)
)
table_header_log = 'According to file: {}'.format(FILE)
table_header_len = len(table_header)
table_header_log_len = (table_header_len)
header_len = max(table_header_len, table_header_log_len)
header_separator = ''.ljust(table_header_len, '=')
print(header_separator)
print(table_header.center(header_len))
print(table_header_log.center(header_len))
print(header_separator)
for num, payload in enumerate(c.most_common(n=LIMIT), start=1):
    ip, count = payload
    print(
        "{num}. {ip}: {count}".format(
            num=str(num).rjust(2),
            ip=ip.ljust(16),
            count=count
        )
    )
