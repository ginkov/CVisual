# -*- coding: utf-8
import re
from parsers import get_percent, get_status


def parse(text):

    _MAX_NEIGHBORS = 300

    results = [
        {
            'name': u'OSPF 邻居数量',
            "id": "L3Ospfnei",
            "grp": "l3",
            'icon': 'fa-external-link',
            'unit': u'个',
            'total': _MAX_NEIGHBORS,
            'detail': {}
        }
    ]

    for _line in text:
        m_line = re.match(r'Total number of neighbors: (\d+)', _line, re.M | re.I)
        if m_line:
            results[0]['detail']['total_neighbors'] = int(m_line.group(1))
            break

    results[0]['used'] = results[0]['detail']['total_neighbors']
    results[0]['free'] = results[0]['total'] - results[0]['used']
    results[0]['rate'] = get_percent(results[0]['total'], results[0]['used'])
    results[0]['stat'] = get_status(results[0]['rate'])

    return results
