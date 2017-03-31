# -*- coding: utf-8
import re
from parsers import get_percent, get_status

# YQB-OPN-F07AP1-SW1# sh platform afm info tcam 0 region span
# span tcam TCAM configuration for asic id 0:
# [ vacl tcam]: range     0 - 2047
# [ifacl tcam]: range  2048 - 3199
# [  qos tcam]: range  3200 - 3647
# [rbacl tcam]: range  3648 - 3775
# [ span tcam]: range  3776 - 3839 *
# [  sup tcam]: range  3840 - 3967
#
#     TCAM [span tcam]: [v:1, size:64, start:3776 end:3839]
#     In use tcam entries: 2
#         3776,3839


def parse(text):

    results = [
        {
            'name': u'SPAN ACL TCAM',
            "id": "SvcSpanaclt",
            "grp": "svc",
            "icon": "fa-microchip",
            'unit': u'项',
            'detail': {}
        }
    ]

    for _line in text:

        m_line = re.match(r'TCAM \[span tcam\]: \S+, size:(\d+), start:\d+ end:\d+', _line, re.M | re.I)
        if m_line:
            results[0]['total'] = int(m_line.group(1))
            continue

        m_line = re.match(r'In use tcam entries: (\d+)', _line, re.M | re.I)
        if m_line:
            results[0]['used'] = int(m_line.group(1))

    results[0]['free'] = results[0]['total'] - results[0]['used']

    results[0]['rate'] = get_percent(results[0]['total'], results[0]['used'])
    results[0]['stat'] = get_status(results[0]['rate'])

    return results
