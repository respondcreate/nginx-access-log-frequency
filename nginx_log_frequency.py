"""
nginx_log_frequency.py

Determine the most frequently logged values from a standard nginx access log.
"""

from __future__ import print_function
import argparse
from collections import Counter
import io
import re


class InvalidSegment(Exception):
    pass

SEGMENT_VERBOSE_MAPPING = {
    'ip_address': {
        'verbose': 'IP Address',
        'verbose_plural': 'IP Addresses'
    },
    'remote_user': {
        'verbose': 'Remote User',
        'verbose_plural': 'Remote Users',
    },
    'status_code': {
        'verbose': 'Status Code',
        'verbose_plural': 'Status Codes',
    },
    'http_referer': {
        'verbose': 'Referer',
        'verbose_plural': 'Referers',
    },
    'http_user_agent': {
        'verbose': 'User Agent',
        'verbose_plural': 'User Agents',
    }
}

ALLOWED_CHOICES_STR = "Allowed choices: {}.".format(
    ', '.join([
        "{} ({})".format(key, value['verbose'])
        for key, value in SEGMENT_VERBOSE_MAPPING.iteritems()
    ])
)

parser = argparse.ArgumentParser(
    description='Determine the most frequently logged values from a standard '
                'nginx access log.'
)
parser.add_argument(
    '-s',
    '--segment',
    type=str,
    default='ip_address',
    help="The data segment whose frequency you'd like to determine. "
         "{}".format(ALLOWED_CHOICES_STR)
)
parser.add_argument(
    '-l',
    '--limit',
    type=int,
    default=10,
    help='The limit of most-frequently-logged IPs to list. Defaults to 10.'
)
parser.add_argument(
    '-f',
    '--file',
    type=str,
    default='/etc/nginx/access.log',
    help="The path on disk of the nginx access log you'd like evaluated."
)

# Arguments to set
args = parser.parse_args()
FILE = args.file
LIMIT = args.limit
SEGMENT_TO_COUNT = args.segment

if SEGMENT_TO_COUNT not in SEGMENT_VERBOSE_MAPPING.keys():
    raise InvalidSegment(
        "'{}' is an invalid data segment type. {}".format(
            SEGMENT_TO_COUNT,
            ALLOWED_CHOICES_STR
        )
    )

if LIMIT > 1:
    verbose_key = 'verbose_plural'
else:
    verbose_key = 'verbose'

nginx_access_log_regex = re.compile(
    r'(?P<ip_address>.*?)\ \-\ (?P<remote_user>.*?)\ \[(?P<time_local>.*?)\]'
    r'\ \"(?P<request>.*?)\"\ (?P<status_code>.*?)\ (?P<body_bytes_sent>.*?)\ '
    r'\"(?P<http_referer>.*?)\"\ \"(?P<http_user_agent>.*?)\"',
    re.IGNORECASE
)

with io.open(FILE, 'r') as log_file:
    c = Counter([
        nginx_access_log_regex.match(line).group(SEGMENT_TO_COUNT)
        for line in log_file.readlines()
    ])


table_header = (
    "Top {limit} Most Frequently Logged {segment_verbose_plural}".format(
        limit=LIMIT,
        segment_verbose_plural=SEGMENT_VERBOSE_MAPPING[
            SEGMENT_TO_COUNT
        ][verbose_key]
    )
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
