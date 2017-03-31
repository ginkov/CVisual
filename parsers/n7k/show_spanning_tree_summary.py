# -*- coding: utf-8
import re
from parsers import get_status, get_percent


def parse(text):

    _MAX_LOGICAL_PORT = 16000

    results = [
        {
            'name': u'STP 逻辑端口容量',
            "id": "L2Stp",
            "grp": "l2",
            'icon': 'fa-sitemap',
            'unit': u'个',
            'total': _MAX_LOGICAL_PORT,
            'detail': {}
        }
    ]

    header_count = 0
    for _line in text:
        if _line.startswith('-------'):
            header_count = 1
        else:
            m_line = re.match(r'^(\d+)\svlans\s+\d+\s+\d+\s+\d+\s+\d+\s+(\d+)', _line, re.M | re.I)
            if m_line and header_count == 1:
                results[0]['detail']['total_configured_vlans'] = int(m_line.group(1))
                results[0]['detail']['logical_ports'] = int(m_line.group(2))
                break
            else:
                header_count = 0

    results[0]['used'] = results[0]['detail']['logical_ports']
    results[0]['free'] = results[0]['total'] - results[0]['used']
    results[0]['rate'] = get_percent(results[0]['total'], results[0]['used'])
    results[0]['stat'] = get_status(results[0]['rate'])

    return results
