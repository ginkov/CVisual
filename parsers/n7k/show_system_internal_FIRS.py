# -*- coding: utf-8
import re
from parsers import get_status, get_percent


def parse(text):

    results = [
        {
            'name':     u'模块 SoC 上 FIB 条目',
            'id':       'L3Fibroute',
            'grp':      'l3',
            'icon':     'fa-location-arrow',
            'unit':     u'条',
            'table': {
                'data': [
                    {'module': 1, 'size': 0, 'used': 0, 'util': 0.0, 'inst': 0},
                    {'module': 2, 'size': 0, 'used': 0, 'util': 0.0, 'inst': 0},
                    {'module': 3, 'size': 0, 'used': 0, 'util': 0.0, 'inst': 0},
                    {'module': 4, 'size': 0, 'used': 0, 'util': 0.0, 'inst': 0},
                    {'module': 5, 'size': 0, 'used': 0, 'util': 0.0, 'inst': 0},
                    {'module': 6, 'size': 0, 'used': 0, 'util': 0.0, 'inst': 0},
                    {'module': 7, 'size': 0, 'used': 0, 'util': 0.0, 'inst': 0},
                    {'module': 8, 'size': 0, 'used': 0, 'util': 0.0, 'inst': 0}
                ],
                'column': [
                    {'title': 'Module',     'data': 'module'},
                    {'title': u'实例',       'data': 'inst'},
                    {'title': 'Size',       'data': 'size'},
                    {'title': 'Used',       'data': 'used'},
                    {'title': u'利用率%',    'data': 'util'}
                ]
            }
        }
    ]

    inst_ready = 0

    for line in text:

        m_line = re.match(r'slot\s+(\d+)', line, re.M | re.I)
        if m_line:
            m_slot = int(m_line.group(1)) - 1

        m_line = re.match(r'IPv4 routes summary for instance :(\d+)', line, re.M | re.I)
        if m_line:
            m_inst = int(m_line.group(1))
        else:
            m_inst = 0

        m_line = re.match(r'FIB size:\s+(\d+)', line, re.M | re.I)
        if m_line:
            m_size = int(m_line.group(1))

        m_line = re.match(r'Total number of routes:\s+(\d+)', line, re.M | re.I)
        if m_line:
            m_used = int(m_line.group(1))
            inst_ready = 1

        if inst_ready:
            inst_ready = 0
            m_util = round(100.0 * float(m_used) / float(m_size), 2)
            if m_util > results[0]['table']['data'][m_slot]['util']:
                results[0]['table']['data'][m_slot]['size'] = m_size
                results[0]['table']['data'][m_slot]['used'] = m_used
                results[0]['table']['data'][m_slot]['inst'] = m_inst
                results[0]['table']['data'][m_slot]['util'] = m_util

    max_item = max(results[0]['table']['data'], key=lambda item: item['util'])

    results[0]['total'] = max_item['size']
    results[0]['used'] = max_item['used']
    results[0]['free'] = results[0]['total'] - results[0]['used']

    results[0]['rate'] = get_percent(results[0]['total'], results[0]['used'])
    results[0]['stat'] = get_status(results[0]['rate'])

    return results
