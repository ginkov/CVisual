# -*- coding: utf-8
import re
from parsers import get_percent, get_status


def parse(text):

    _QOS_BUF_RX_BYTES = 1572864
    _QOS_BUF_TX_BYTES = 734003

    results = [
        {
            'name': u'F卡 QoS Buffer 利用率',
            'id': 'SvcQosb',
            'grp': 'svc',
            'icon': 'fa-filter',
            'unit': u'%',
            'table': {
                'data': [],
                'column': [
                    {'title': 'Module',     'data': 'module'},
                    {'title': 'Tx Buffer',  'data': 'tx'},
                    {'title': 'Tx %',       'data': 'tx_util'},
                    {'title': 'Rx Buffer',  'data': 'rx'},
                    {'title': 'Rx %',       'data': 'rx_util'},
                ]
            },
            'detail': {}
        }
    ]


    flag = False
    for _line in text:
        m_line = re.match(r'Module\s+Bytes:\s+Tx buffer\s+Rx buffer', _line, re.M | re.I)
        if m_line:
            flag = True
        elif flag:
            m_line = re.match(r'(\d+)\s+(\d+)\s+(\d+)', _line, re.M | re.I)
            if m_line:
                m_module = {
                    'module': int(m_line.group(1)),
                    'tx': int(m_line.group(2)),
                    'tx_util': 100.0 * float(m_line.group(2)) / _QOS_BUF_TX_BYTES,
                    'rx': int(m_line.group(3)),
                    'rx_util': 100.0 * float(m_line.group(3)) / _QOS_BUF_RX_BYTES
                }
                results[0]['table']['data'].append(m_module)

    if results[0]['table']:

        max_module = max(results[0]['table']['data'], key=lambda item: max(item['rx_util'], item['tx_util']))

        results[0]['total'] = 100.0
        results[0]['used'] = max(max_module['rx_util'], max_module['tx_util'])
        results[0]['free'] = results[0]['total'] - results[0]['used']
        results[0]['rate'] = get_percent(results[0]['total'], results[0]['used'])
        results[0]['stat'] = get_status(results[0]['rate'])

    else:
        results = None

    return results
