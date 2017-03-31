# -*- coding: utf-8
import re
from parsers import get_percent, get_status

# YQB-OPN-DIS3-SW1# show hsrp summary
#
# HSRP Summary:
#
# Extended-hold (NSF) disabled
# Global HSRP-BFD disabled
#
# Total Groups: 255
#      Version::    V1-IPV4: 0       V2-IPV4: 255    V2-IPV6: 0
#        State::     Active: 53      Standby: 201     Listen: 0
#        State::  V6-Active: 0    V6-Standby: 0    V6-Listen: 0
#
# Total HSRP Enabled interfaces: 255
#
# Total Packets:
#              Tx - Pass: 1577316693 Fail: 0
#              Rx - Good: 1577287024
#
# Packet for unknown groups: 0
#
# Total MTS: Rx: 2428


def parse(text):

    _MAX_HSRP_GROUP = 2000

    results = [
        {
            'name': u'HSRP 条目数',
            "id": "L3Hsrp",
            "grp": "l3",
            'unit': u'条',
            'icon': 'fa-refresh',
            'total': _MAX_HSRP_GROUP,
            'detail': {}
        }
    ]

    for _line in text:
        m_line = re.match(r'Total Groups:\s+(\d+)', _line, re.M | re.I)
        if m_line:
            results[0]['detail']['hsrp'] = int(m_line.group(1))
            break

    results[0]['used'] = results[0]['detail']['hsrp']
    results[0]['free'] = results[0]['total'] - results[0]['used']
    results[0]['rate'] = get_percent(results[0]['total'], results[0]['used'])
    results[0]['stat'] = get_status(results[0]['rate'])

    return results
