#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
nginx_access_log_ip_frequency.py

Determine the most frequently logged IP addresses in a nginx access log.

Examples:

    Print out a list of the top 10 most frequently logged IP addresses:

        $ python nginx_access_log_ip_frequency.py -s ip_address

    Print out a list of the top 5 most frequently logged user agents from
    a log file stored in a custom location:

        $ python nginx_access_log_ip_frequency.py -l 5
          -f /var/log/custom-log-location/access.log
"""

from __future__ import print_function
import argparse
from collections import Counter
import io
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


def count_nginx_log_ip_address_frequency(log_file_path):
    """
    Tally the appearance of IP addresses in a nginx log file.

    Args:
        log_file_path (str): The path on disc of the nginx log file to process.

    Returns:
        A collections.Counter instance.

    Raises:
        IOError: If `log_file_path` points to a non-existant file.
        ValueError: If `regex_group_key` cannot be found on a line of
        `log_file_path` with `per_line_regex`.
    """
    with io.open(log_file_path, 'r') as log_file:
        c = Counter([
            line.split(' ', 1)[0]
            for line in log_file
        ])
    return c


def create_parser():
    """Create a command line parser for this module."""
    parser = argparse.ArgumentParser(
        description='Determine the most frequently logged values from a '
                    'standard nginx access log.'
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
                 top_list_length,
                 log_file_path):
    """
    Print a summary of the tally operation to the shell.

    Args:
        counter_instance (instance): A collections.Counter instance.
        top_list_length (int): The length of the 'top' list you'd like printed.
        log_file_path (str): The path to the proceseed log file for inclusion
        in the title section.

    Returns: None
    """
    table_header = (
        "Top {limit} Most Frequently Logged IP Addresses".format(
            limit=top_list_length
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

    c = count_nginx_log_ip_address_frequency(log_file_path)
    print_report(c, top_list_limit, log_file_path)
