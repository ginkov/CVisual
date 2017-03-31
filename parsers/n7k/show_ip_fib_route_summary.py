# -*- coding: utf-8
import re
from parsers import get_status, get_percent

# YQB-OPN-F07DB1-SW2(config)# show ip fib route summary
#
# IPv4 routes for table default/base
#
# Cumulative route updates: 5
# Cumulative route inserts: 0
# Cumulative route deletes: 0
# Total number of routes: 7
# Total number of paths : 7


def parse(text):

    _MAX_FIB_ENTRY = 8192

    results = [
        {
            'name': u'FIB表容量',
            "id": "L3Fibtab",
            "grp": "l3",
            "icon": "fa-location-arrow",
            'unit': u'条',
            'total': _MAX_FIB_ENTRY,
            'detail': {}
        }
    ]

    found = False

    for _line in text:

        m_line = re.match(r'Total number of paths :\s+(\d+)', _line, re.M | re.I)

        if m_line:
            m_used = int(m_line.group(1))
            found = True

    if found:
        results[0]['used'] = m_used
        results[0]['free'] = results[0]['total'] - m_used
        results[0]['rate'] = get_percent(results[0]['total'], results[0]['used'])
        results[0]['stat'] = get_status(results[0]['rate'])

    else:
        results = None

    return results
