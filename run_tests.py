"""Tests for nginx-access-log-frequency."""

import unittest
from StringIO import StringIO
import sys

from nginx_access_log_frequency import (
    count_nginx_log_frequency,
    create_parser,
    NGINX_ACCESS_LOG_REGEX,
    print_report
)

EXPECTED_IP_TEST_STRING_OUTPUT = """=========================================
Top 5 Most Frequently Logged IP Addresses
  According to file: example-access.log  
=========================================
 1. 111.222.333.444 : 10
 2. 33.444.55.666   : 9
 3. 222.333.444.555 : 8
 4. 444.555.666.77  : 3
 5. 55.666.777.888  : 2"""


class NGINXAccessLogFrequencyTest(unittest.TestCase):
    """Test Case for for nginx_access_log_frequency.py."""

    def setUp(self):
        """Setup the test client."""
        self.parser = create_parser()

    def test_nginx_access_log_frequency(self):
        """Test nginx_access_log_frequency.py."""
        args = self.parser.parse_args([
            '-s',
            'ip_address',
            '-l',
            '5',
            '-f',
            'example-access.log'
        ])
        log_file_path = args.file
        regex_group_key = args.segment
        limit = args.limit
        c = count_nginx_log_frequency(
            log_file_path,
            regex_group_key,
            NGINX_ACCESS_LOG_REGEX
        )
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            print_report(c, regex_group_key, limit, log_file_path)
            output = out.getvalue().strip()
            assert output == EXPECTED_IP_TEST_STRING_OUTPUT
        finally:
            sys.stdout = saved_stdout

if __name__ == '__main__':
    unittest.main()
