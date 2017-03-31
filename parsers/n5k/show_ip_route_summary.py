# -*- coding: utf-8
import re
from parsers import get_status, get_percent

# YQB-OPN-F07AP1-SW1# sh ip route summary
# IP Route Table for VRF "default"
# Total number of routes: 11
# Total number of paths:  11
#
# Best paths per protocol:      Backup paths per protocol:
#   am             : 3            None
#   local          : 1
#   direct         : 1
#   static         : 1
#   broadcast      : 5
#
# Number of routes per mask-length:
#   /0 : 1       /8 : 1       /24: 1       /32: 8


def parse(text):

    _MAX_DYNAMIC_ROUTE = 16384

    results = [
        {
            'name': u'动态路由条目',
            "id": "L3Route",
            "grp": "l3",
            "icon": "fa-list",
            'unit': u'条',
            'total': _MAX_DYNAMIC_ROUTE,
            'detail': {}
        }
    ]

    # 动态路由条目

    for line in text:

        m_line = re.match(r'(ospf\S*)\s+:\s(\d+)', line, re.M | re.I)
        if m_line:
            results[0]['detail'][m_line.group(1)] = int(m_line.group(2))

        m_line = re.match(r'(bgp\S*)\s+:\s(\d+)', line, re.M | re.I)
        if m_line:
            results[0]['detail'][m_line.group(1)] = int(m_line.group(2))

        m_line = re.match(r'(rip\S*)\s+:\s(\d+)', line, re.M | re.I)
        if m_line:
            results[0]['detail'][m_line.group(1)] = int(m_line.group(2))

        m_line = re.match(r'(isis\S*)\s+:\s(\d+)', line, re.M | re.I)
        if m_line:
            results[0]['detail'][m_line.group(1)] = int(m_line.group(2))

    results[0]['used'] = sum(results[0]['detail'].values())
    results[0]['free'] = results[0]['total'] - results[0]['used']

    results[0]['rate'] = get_percent(results[0]['total'], results[0]['used'])
    results[0]['stat'] = get_status(results[0]['rate'])

    return results
