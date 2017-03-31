# -*- coding: utf-8
import re
from parsers import get_status, get_percent
# YQB-OPN-F02WB1-SW1# dir log:
#          31    Mar 23 10:40:38 2013  dmesg
#           0    Mar 23 10:40:53 2013  libfipf.3118
#           0    Mar 23 10:40:57 2013  libfipf.3256
#     4194304    Dec 26 17:51:34 2016  messages
#        1048    Mar 23 10:41:56 2013  startupdebug
#
# Usage for log://sup-local
#    72302592 bytes used
#   347127808 bytes free
#   419430400 bytes total


def parse(text):

    results = [
        {
            'name': u'Log 存储空间',
            "id": "InfraLog",
            "grp": "infra",
            "icon": "fa-hdd-o",
            'unit': 'MB',
            'detail': {}
        }
    ]

    for line in text:

        m_line = re.match(r'(\d+)\s+bytes\s+used', line, re.M | re.I)
        if m_line:
            m_used = int(m_line.group(1))
            continue

        m_line = re.match(r'(\d+)\s+bytes\s+free', line, re.M | re.I)
        if m_line:
            m_free = int(m_line.group(1))

    results[0]['total'] = round((m_free + m_used)/1048576.0, 1)
    results[0]['used'] = round(m_used / 1048576.0, 1)
    results[0]['free'] = round(m_free / 1048576.0, 1)

    results[0]['rate'] = get_percent(results[0]['total'], results[0]['used'])
    results[0]['stat'] = get_status(results[0]['rate'])

    return results
