# -*- coding: utf-8
import re
from parsers import get_percent, get_status

#  FEX         FEX           FEX                       FEX
# Number    Description      State            Model            Serial
# ------------------------------------------------------------------------
# 101     C2232(10G)                Online    N2K-C2232TM-10GE   SSI18050109
# 102     C2232(10G)                Online    N2K-C2232TM-10GE   SSI1805011K
# 111      C2248(1G)                Online   N2K-C2248TP-E-1GE   FOX1802GV3H
# 112      C2248(1G)                Online   N2K-C2248TP-E-1GE   FOX1802GV0V


def parse(text):

    _MAX_L2_FEX = 24
    _MAX_L2_L3_FEX = 16

    key = 'show fex'

    results = [
        {
            'name': u"FEX 容量",
            "id": "InfFex",
            "grp": "infra",
            "icon": "fa-sitemap",
            'unit': u'个',
            'total': _MAX_L2_FEX,
            'table': {
                'data': [],
                'column': [
                    {'title': 'Number',   'data': 'number'},
                    {'title': u'描述',    'data': 'descri'},
                    {'title': u'状态',    'data': 'status'},
                    {'title': u'型号',    'data': 'model'},
                    {'title': u'序列号',  'data': 'serial'}
               ]
            }
        }
    ]

    for _line in text:
        m_line = re.match(r'(\d+)\s+(\S+)\s+(\w+)\s+(\S+)\s+(\w+)', _line, re.M | re.I)
        if m_line:
            m_fex = {
                'number': int(m_line.group(1)),
                'descri': m_line.group(2),
                'status': m_line.group(3),
                'model': m_line.group(4),
                'serial': m_line.group(5)
            }
            results[0]['table']['data'].append(m_fex)

    results[0]['used'] = len(results[0]['table']['data'])
    results[0]['free'] = results[0]['total'] - results[0]['used']

    results[0]['rate'] = get_percent(results[0]['total'], results[0]['used'])
    results[0]['stat'] = get_status(results[0]['rate'])

    return results
