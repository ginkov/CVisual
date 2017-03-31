# -*- coding: utf-8
import re
from parsers import get_percent, get_status


def parse(text):

    _MAX_VDC = 8

    results = [
        {
            'name':     u'VDC 容量',
            "id":       "InfVdc",
            "grp":      "infra",
            'icon':     'fa-clone',
            'unit':     u'个',
            'total':    _MAX_VDC,
            'table': {
                'data': [],
                'column': [
                    {'title': 'VDC',    'data': 'vdc_name'},
                    {'title': 'State',  'data': 'state'}
                ]
            }
        }
    ]

    header_count = 0

    for _line in text:

        if header_count < 2:
            if _line.startswith('vdc_id') and header_count == 0:
                header_count = 1
            elif _line.startswith('------') and header_count == 1:
                header_count = 2
            else:
                header_count = 0

        else:

            m_line = re.match(r'(\d+)\s+(\S+)\s+(\w+)\s+\S+\s+\w+', _line, re.M | re.I)

            if m_line:

                results[0]['table']['data'].append(
                    {
                        'vdc_id': m_line.group(1),
                        'vdc_name': m_line.group(2),
                        'state': m_line.group(3)
                    }
                )

            else:
                break

    results[0]['used'] = len(results[0]['table']['data'])
    results[0]['free'] = results[0]['total'] - results[0]['used']
    results[0]['rate'] = get_percent(results[0]['total'], results[0]['used'])
    results[0]['stat'] = get_status(results[0]['rate'])

    return results
