# -*- coding: utf-8
import re
from parsers import get_percent, get_status


def parse(text):

    _MAX_OSPF_ROUTE = 15000
    _MAX_STATIC_ROUTE = 1000

    results = [
        {
            'name': u'OSPF 路由条目',
            "id": "L3Ospfroute",
            "grp": "l3",
            'icon': 'fa-address-card-o',
            'unit': u'条',
            'total': _MAX_OSPF_ROUTE,
            'detail': {}
        },
        {
            'name': u'静态路由条目',
            "id": "L3Staticroute",
            "grp": "l3",
            'icon': 'fa-external-link',
            'unit': u'条',
            'total': _MAX_STATIC_ROUTE,
            'detail': {}
        }
    ]

    # OSPF 路由条目

    for _line in text:
        m_line = re.match(r'(ospf\S*)\s+:\s(\d+)', _line, re.M | re.I)
        if m_line:
            results[0]['detail'][m_line.group(1)] = int(m_line.group(2))

    results[0]['used'] = sum(results[0]['detail'].values())
    results[0]['free'] = results[0]['total'] - results[0]['used']
    results[0]['rate'] = get_percent(results[0]['total'], results[0]['used'])
    results[0]['stat'] = get_status(results[0]['rate'])

    # 静态路由条目

    for _line in text:
        m_line = re.match(r'static\s+:\s(\d+)', _line, re.M | re.I)
        if m_line:
            results[1]['detail']['static'] = int(m_line.group(1))
            break

    results[1]['used'] = results[1]['detail']['static']
    results[1]['free'] = results[1]['total'] - results[1]['used']
    results[1]['rate'] = get_percent(results[1]['total'], results[1]['used'])
    results[1]['stat'] = get_status(results[1]['rate'])

    return results
