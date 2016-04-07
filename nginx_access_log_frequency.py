#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
nginx_access_log_frequency.py

Determine the most frequently logged values from a standard nginx access log.

Allowed data 'segments' to tally (with the -s/--segment argument):
    * ip_address: IP Address
    * remote_user: Remote User
    * status_code: Status Code
    * http_referrer: Referrer
    * http_user_agent: User Agent

Examples:
    Print out a list of the top 10 most frequently logged IP addresses:

        $ python nginx_access_log_frequency.py -s ip_address

    Print out a list of the top 5 most frequently logged user agents from
    a log file stored in a custom location:

        $ python nginx_access_log_frequency.py -s http_user_agent -l 5
          -f /var/log/custom-log-location/access.log
"""

from __future__ import print_function
import argparse
from collections import Counter
import io
import re
try:
    dict.iteritems
except AttributeError:
    # Python 3
    def iteritems(d):
        """Define iteritems for Python 3."""
        return iter(d.items())
else:
    # Python 2
    def iteritems(d):
        """Define iteritems for Python 2."""
        return d.iteritems()

__version__ = '0.1'
__author__ = 'Jonathan Ellenberger'
__license__ = 'MIT'
__copyright__ = 'Copyright 2016 Jonathan Ellenberger'


class InvalidSegment(Exception):
    """
    An Exception for signaling invalid segments.

    Used to notifying users that they entered a non-supported
    data segment for tallying.
    """

    pass

NGINX_ACCESS_LOG_REGEX = re.compile(
    r'(?P<ip_address>.*?)\ \-\ (?P<remote_user>.*?)\ \[(?P<time_local>.*?)'
    r'\]\ \"(?P<request>.*?)\"\ (?P<status_code>.*?)\ '
    r'(?P<body_bytes_sent>.*?)\ \"(?P<http_referrer>.*?)\"\ '
    '\"(?P<http_user_agent>.*?)\"',
    re.IGNORECASE
)

ACCESS_LOG_SEGMENT_VERBOSE_MAPPING = {
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
    'http_referrer': {
        'verbose': 'Referrer',
        'verbose_plural': 'Referrers',
    },
    'http_user_agent': {
        'verbose': 'User Agent',
        'verbose_plural': 'User Agents',
    }
}

ALLOWED_CHOICES_STR = "Allowed choices: {}.".format(
    ', '.join([
        "{} ({})".format(key, value['verbose'])
        for key, value in iteritems(ACCESS_LOG_SEGMENT_VERBOSE_MAPPING)
    ])
)


def count_nginx_log_frequency(log_file_path,
                              regex_group_key,
                              per_line_regex):
    """
    Tally the appearance of values in a nginx log file.

    Args:
        log_file_path (str): The path on disc of the nginx log file to process.
        regex_group_key (str): The named group of `per_line_regex` to count.
        per_line_regex (str): The regex used to parse each line of
            `log_file_path`.

    Returns:
        A collections.Counter instance.

    Raises:
        IOError: If `log_file_path` points to a non-existant file.
        ValueError: If `regex_group_key` cannot be found on a line of
        `log_file_path` with `per_line_regex`.
    """
    with io.open(log_file_path, 'r') as log_file:
        c = Counter([
            per_line_regex.match(line).group(regex_group_key)
            for line in log_file.readlines()
        ])
    return c


def create_parser():
    """Create a command line parser for this module."""
    parser = argparse.ArgumentParser(
        description='Determine the most frequently logged values from a '
                    'standard nginx access log.'
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
        default='/var/log/nginx/access.log',
        help="The path on disk of the nginx access log you'd like evaluated. "
             "Defaults to /var/log/nginx/access.log"
    )
    return parser


def print_report(counter_instance,
                 regex_group_key,
                 top_list_length,
                 log_file_path):
    """
    Print a summary of the tally operation to the shell.

    Args:
        counter_instance (instance): A collections.Counter instance.
        regex_group_key (str): The key for the verbose mapping in
        ACCESS_LOG_SEGMENT_VERBOSE_MAPPING to use for the title section.
        top_list_length (int): The length of the 'top' list you'd like printed.
        log_file_path (str): The path to the proceseed log file for inclusion
        in the title section.

    Returns: None
    """
    if top_list_length > 1:
        verbose_key = 'verbose_plural'
    else:
        verbose_key = 'verbose'

    table_header = (
        "Top {limit} Most Frequently Logged {segment_verbose_plural}".format(
            limit=top_list_length,
            segment_verbose_plural=ACCESS_LOG_SEGMENT_VERBOSE_MAPPING[
                regex_group_key
            ][verbose_key]
        )
    )
    table_header_log = 'According to file: {}'.format(log_file_path)
    header_len = max(
        len(table_header),
        len(table_header_log)
    )
    header_separator = ''.ljust(header_len, '=')
    print(header_separator)
    print(table_header.center(header_len))
    print(table_header_log.center(header_len))
    print(header_separator)
    for num, payload in enumerate(
        counter_instance.most_common(n=top_list_length), start=1
    ):
        ip, count = payload
        print(
            "{num}. {ip}: {count}".format(
                num=str(num).rjust(2),
                ip=ip.ljust(16),
                count=count
            )
        )

if __name__ == '__main__':  # pragma: no cover
    parser = create_parser()

    # Arguments to set
    args = parser.parse_args()
    log_file_path = args.file
    top_list_limit = args.limit
    regex_group_key = args.segment

    if regex_group_key not in ACCESS_LOG_SEGMENT_VERBOSE_MAPPING.keys():
        raise InvalidSegment(
            "'{}' is an invalid data segment type. {}".format(
                regex_group_key,
                ALLOWED_CHOICES_STR
            )
        )

    c = count_nginx_log_frequency(
        log_file_path,
        regex_group_key,
        NGINX_ACCESS_LOG_REGEX
    )
    print_report(c, regex_group_key, top_list_limit, log_file_path)
