# -*- coding: utf-8
import re
from parsers import get_status, get_percent


def parse(text):
    results = [
        {
            'name': u'IPv4 单播路由内存容量',
            "id": "L3U4mem",
            "grp": "l3",
            "icon": "fa-list",
            'unit': u'MB',
            'table': {
                'data': [],
                'column': [
                    {'title': 'VDC', 'data': 'vdc'},
                    {'title': u'总计', 'data': 'max'},
                    {'title': u'已用', 'data': 'used'},
                    {'title': u'利用率%', 'data': 'util'},
                ]
            }
        }
    ]

    flag = False
    for _line in text:
        if _line.startswith('u4route-mem'):
            flag = True
        elif _line.startswith('u6route-mem'):
            break
        elif flag:
            m_line = re.match(r'(\S+)\s+\d+\s+(\d+)\s+(\d+)\s+\d+\s+\d+', _line, re.M | re.I)
            if m_line:
                m_vdc = m_line.group(1)
                m_max = int(m_line.group(2))
                m_used = int(m_line.group(3))
                m_util = round(100.0 * float(m_used) / float(m_max), 1)
                m_item = {
                    'vdc': m_vdc,
                    'max': m_max,
                    'used': m_used,
                    'util': m_util
                }
                results[0]['table']['data'].append(m_item)

    max_item = max(results[0]['table']['data'], key=lambda item: item['util'])

    results[0]['total'] = max_item['max']
    results[0]['used'] = max_item['used']
    results[0]['free'] = max_item['max'] - max_item['used']

    results[0]['rate'] = get_percent(results[0]['total'], results[0]['used'])
    results[0]['stat'] = get_status(results[0]['rate'])

    return results
