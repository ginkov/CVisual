# -*- coding: utf-8
import re
from parsers import get_status, get_percent

# Total Power Capacity                              780.00 W
#
# Power reserved for Supervisor(s)                  492.00 W
# Power currently used by Modules                   234.00 W


def parse(text):
    results = [
        {
            'name': u'电源容量',
            "id": "InfPower",
            "grp": "infra",
            "icon": "fa-plug",
            'unit': 'W',
            'detail': {}
        }
    ]

    for _line in text:
        m_line = re.match(r'Total Power Capacity\s+(\S+)\s+W', _line, re.M | re.I)
        if m_line:
            m_total = float(m_line.group(1))
            continue
        m_line = re.match(r'Power reserved for Supervisor\S+\s+(\S+)\s+W', _line, re.M | re.I)
        if m_line:
            m_super = float(m_line.group(1))
            continue
        m_line = re.match(r'Power currently used by Modules\s+(\S+)\s+W', _line, re.M | re.I)
        if m_line:
            m_module = float(m_line.group(1))

    results[0]['detail']['total'] = m_total / 2
    results[0]['detail']['reserved_for_superengine'] = m_super
    results[0]['detail']['used_by_modules'] = m_module

    results[0]['total'] = m_total / 2
    results[0]['used'] = m_super + m_module
    results[0]['free'] = m_total - results[0]['used']
    results[0]['rate'] = get_percent(results[0]['total'], results[0]['used'])
    results[0]['stat'] = get_status(results[0]['rate'])

    return results

