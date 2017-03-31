# -*- coding: utf-8
import re
from parsers import get_status, get_percent

# YQB-OPN-DIS3-SW1# show hardware fabric-utilization
# ------------------------------------------------
# Slot        Total Fabric        Utilization
#             Bandwidth      Ingress % Egress %
# ------------------------------------------------
# 1             550 Gbps          0.00     0.30
# 2             550 Gbps          0.50     0.00
# 3             550 Gbps          0.00     0.00
# 4             550 Gbps          0.40     0.50
# 5             275 Gbps          0.00     0.00
# 6             275 Gbps          0.00     0.00
# 7             550 Gbps          0.00     0.00
# 8             550 Gbps          0.00     0.60


def parse(text):

    results = [
        {
            'name':     u'交换矩阵最大利用率',
            'id':       'PhyFabric',
            'grp':      'phy',
            'icon':     'fa-random',
            'unit':     '%',
            'table':    {
                'data': [],
                'column': [
                    {'title': u'槽位',       'data': 'slot'},
                    {'title': 'Ingress%',   'data': 'ingress_util'},
                    {'title': 'Egress%',    'data': 'egress_util'},
                ]
            },
            'detail':   {}
        }
    ]

    header_count = 0

    for _line in text:

        if header_count < 4:
            if _line.startswith('--------') and header_count == 0:
                header_count = 1
            elif _line.startswith('Mod ') and header_count == 1:
                header_count = 2
            elif _line.startswith('Bandwidth ') and header_count == 2:
                header_count = 3
            elif _line.startswith('--------') and header_count == 3:
                header_count = 4
            else:
                header_count = 0

        else:
            m_line = re.match(r'(\d+)\s+\d+\s\w+\s+(\S+)\s+(\S+)', _line, re.M | re.I)

            if m_line:
                results[0]['table']['data'].append({
                    'slot': m_line.group(1),
                    'ingress_util': float(m_line.group(2)),
                    'egress_util': float(m_line.group(3))
                })
            else:
                break

    results[0]['total'] = 100.0

    max_item = max(results[0]['table']['data'], key=lambda item: max(item['ingress_util'], item['egress_util']))

    results[0]['used'] = max(max_item['ingress_util'], max_item['egress_util'])
    results[0]['free'] = 100.0 - results[0]['used']

    results[0]['rate'] = get_percent(results[0]['total'], results[0]['used'])
    results[0]['stat'] = get_status(results[0]['rate'])

    return results
