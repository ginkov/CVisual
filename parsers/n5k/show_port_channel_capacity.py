# -*- coding: utf-8
import re
from parsers import get_percent, get_status


def parse(text):

    _MAX_PORTCHANNEL = 1200

    results = [
        {
            'name': u'VPC 容量',
            "id": "L2Vpc",
            "grp": "l2",
            "icon": "fa-slider",
            'unit': u'个',
            'detail': None,
            'total': _MAX_PORTCHANNEL
        }
    ]

    for _line in text:

        m_line = re.match(r'\d+\stotal\s+(\d+)\sused\s+(\d+)\sfree', _line, re.I | re.M)

        if m_line:
            results[0]['used'] = int(m_line.group(1))
            results[0]['free'] = results[0]['total'] - results[0]['used']

            results[0]['rate'] = get_percent(results[0]['total'], results[0]['used'])
            results[0]['stat'] = get_status(results[0]['rate'])

            break

    return results
