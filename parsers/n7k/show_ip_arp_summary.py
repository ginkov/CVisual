# -*- coding: utf-8
import re
from parsers import get_percent, get_status

# YQB-OPN-DIS3-SW1# show ip arp summary
#
# IP ARP Table - Adjacency Summary
#
#   Resolved   : 4
#   Incomplete : 4 (Throttled : 0)
#   Unknown    : 0
#   Total      : 8


def parse(text):

    _MAX_ARP_ENTRY = 128000

    results = [
        {
            'name': u'ARP 表条目录',
            "id": "L3Arp",
            "grp": "l3",
            'icon': 'fa-map-marker',
            'unit': u'条',
            'total': _MAX_ARP_ENTRY,
            'detail': {}
        }
    ]

    for _line in text:
        m_line = re.match(r'Total\s+:\s(\d+)', _line, re.M | re.I)
        if m_line:
            results[0]['detail']['arp'] = int(m_line.group(1))
            break

    results[0]['used'] = results[0]['detail']['arp']
    results[0]['free'] = results[0]['total'] - results[0]['used']
    results[0]['rate'] = get_percent(results[0]['total'], results[0]['used'])
    results[0]['stat'] = get_status(results[0]['rate'])

    return results
