# -*- coding: utf-8
import re
from parsers import get_status, get_percent


def parse(text):

    _TOTAL_MAC_ENTRY = 32000
    _MAX_UNICAST_MAC_ENTRY = 24000
    _MAX_IGMP_MAC_ENTRY = 3400

    results = [
        {
            'name': u'MAC 地址表容量',
            "id": "L2Mac",
            "grp": "l2",
            "icon": "fa-barcode",
            'unit': u'项',
            'total': _TOTAL_MAC_ENTRY,
            'detail': {}
        }
    ]

    for _line in text:

        m_line = re.match(r'Total MAC Addresses in Use:\s+(\d+)', _line, re.M | re.I)

        if m_line:
            m_used = int(m_line.group(1))

    results[0]['used'] = m_used
    results[0]['free'] = results[0]['total'] - m_used

    results[0]['rate'] = get_percent(results[0]['total'], results[0]['used'])
    results[0]['stat'] = get_status(results[0]['rate'])

    return results
