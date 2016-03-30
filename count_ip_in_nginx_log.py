from collections import Counter
import io

FILE = 'access.log'
LIMIT = 10

with io.open(FILE, 'r') as log_file:
    c = Counter([
        line.split(' ', 1)[0]
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
