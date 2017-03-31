# -*- coding: utf-8
import re
from parsers import get_percent, get_status

# YQB-OPN-DIS3-SW1#  sh vdc YQB-OPN-DIS3-SW1 resource
#
#      Resource                   Min       Max       Used      Unused    Avail
#      --------                   ---       ---       ----      ------    -----
#      vlan                       16        4094      592       0         3502
#      monitor-session            0         2         2         0         0
#      monitor-session-erspan-dst 0         23        0         0         23
#      vrf                        2         4096      4         0         4092
#      port-channel               0         768       65        0         703
#      u4route-mem                96        96        3         93        93
#      u6route-mem                24        24        1         23        23
#      m4route-mem                58        58        1         57        57
#      m6route-mem                8         8         1         7         7
#      monitor-session-inband-src 0         1         1         0         0


def parse(text, vdc_name):

    _MAX_PRODUCTION_VLAN = 1000

    results = [
        {
            'name': u'VDC 中的 VLAN 容量',
            "id": "L2Vlan",
            "grp": "l2",
            'icon': 'fa-sitemap',
            'unit': u'个',
            'total': _MAX_PRODUCTION_VLAN,
            'detail': {}
        }
    ]

    for _line in text:
        m_line = re.match(r'vlan\s+\d+\s+\d+\s+(\d+)\s+\d+\s+\d+', _line, re.M | re.I)

        if m_line:

            results[0]['used'] = int(m_line.group(1))
            results[0]['free'] = results[0]['total'] - results[0]['used']
            results[0]['rate'] = get_percent(results[0]['total'], results[0]['used'])
            results[0]['stat'] = get_status(results[0]['rate'])

    return results
