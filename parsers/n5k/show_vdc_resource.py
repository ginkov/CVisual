# -*- coding: utf-8
import re
from parsers import get_percent, get_status


def parse(text):

    _MAX_VRF = 1000

    results = [
        {
            'name': u'SPAN 会话容量',
            "id": "PhySpan",
            "grp": "phy",
            "icon": "fa-headphones",
            'unit': u'个',
            'detail': {}
        },
        {
            'name': u'VRF 容量',
            "id": "L3Vrf",
            "grp": "l3",
            "icon": "fa-window-restore",
            'unit': u'个',
            'total': _MAX_VRF,
            'detail': {}
        }
   ]

    for _line in text:

        m_line = re.match(r'(\S+)\s+(\d+) used\s+\d+ unused\s+(\d+) free\s+\d+ avail\s+(\d+) total', _line, re.M | re.I)
        if m_line:
            if m_line.group(1) == 'monitor-session':
                results[0]['total'] = int(m_line.group(4))
                results[0]['used'] = int(m_line.group(2))
                results[0]['free'] = results[0]['total'] - results[0]['used']

                results[0]['rate'] = get_percent(results[0]['total'], results[0]['used'])
                results[0]['stat'] = get_status(results[0]['rate'])

            elif m_line.group(1) == 'vrf':
                results[1]['used'] = int(m_line.group(2))
                results[1]['free'] = results[1]['total'] - results[1]['used']

                results[1]['rate'] = get_percent(results[1]['total'], results[1]['used'])
                results[1]['stat'] = get_status(results[1]['rate'])

    return results
