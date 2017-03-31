# -*- coding: utf-8
import re
from parsers import get_percent, get_status

# YQB-OPN-F07DB1-SW2(config)# show system internal forwarding ip route summary
#
# IP routes summary
# Max Host Route Entries: 19456
# Total number of Host Routes: 5
# Max LPM Table Entries : 8192
# Total number of LPM Routes : 4


def parse(text):

    results = [
        {
            'name': u'主机路由容量',
            "id": "L3Hostroute",
            "grp": "l3",
            "icon": "fa-address-card-o",
            'unit': u'条',
            'detail': {}
        },
        {
            'name': u'最长前缀匹配(LPM)路由容量',
            "id": "L3Lpmroute",
            "grp": "l3",
            "icon": "fa-address-card-o",
            'unit': u'条',
            'detail': {}
        }
    ]

    for _line in text:

        m_line = re.match(r'Max Host Route Entries:\s+(\d+)', _line, re.M | re.I)

        if m_line:
            m_host_max = int(m_line.group(1))
            continue

        m_line = re.match(r'Total number of Host Routes:\s+(\d+)', _line, re.M | re.I)

        if m_line:
            m_host_used = int(m_line.group(1))
            continue

        m_line = re.match(r'Max LPM Table Entries :\s+(\d+)', _line, re.M | re.I)

        if m_line:
            m_lpm_max = int(m_line.group(1))
            continue

        m_line = re.match(r'Total number of LPM Routes :\s+(\d+)', _line, re.M | re.I)

        if m_line:
            m_lpm_used = int(m_line.group(1))

    results[0]['total'] = m_host_max
    results[0]['used'] = m_host_used
    results[0]['free'] = m_host_max - m_host_used

    results[0]['rate'] = get_percent(results[0]['total'], results[0]['used'])
    results[0]['stat'] = get_status(results[0]['rate'])

    results[1]['total'] = m_lpm_max
    results[1]['used'] = m_lpm_used
    results[1]['free'] = m_lpm_max - m_lpm_used

    results[0]['rate'] = get_percent(results[0]['total'], results[0]['used'])
    results[0]['stat'] = get_status(results[0]['rate'])

    return results
