# -*- coding: utf-8
import re
from parsers import get_percent, get_status

# YQB-OPN-F02WB1-SW1# dir bootflash:
#           0    Jan 01 15:28:54 2009  20090101_072854_poap_3569_init.log
#           0    Jan 01 15:42:24 2009  20090101_074224_poap_3476_init.log
#           0    Feb 06 13:54:11 2009  20090206_055411_poap_3476_init.log
#           0    Feb 06 14:21:18 2009  20090206_062118_poap_3476_init.log
#           0    Feb 06 14:35:21 2009  20090206_063521_poap_3484_init.log
#     1371870    Feb 06 16:39:04 2009  D8-05
#         249    Feb 06 14:45:33 2009  convert_pfm1.log
#         344    Feb 06 14:45:33 2009  fcoe_mgr_cnv.log
#        1044    Feb 06 14:44:44 2009  fwm_pre_issu_dump.txt
#        3117    Mar 23 10:40:43 2013  mts.log
#    31646720    Jan 23 15:23:56 2013  n5000-uk9-kickstart.5.2.1.N1.1.bin
#    31650816    Feb 06 14:01:03 2009  n5000-uk9-kickstart.5.2.1.N1.2a.bin
#   173087826    Jan 23 15:24:54 2013  n5000-uk9.5.2.1.N1.1.bin
#   173135786    Feb 06 14:05:54 2009  n5000-uk9.5.2.1.N1.2a.bin
#        5524    Mar 23 10:52:49 2013  span.log
#        4606    Feb 06 14:44:44 2009  stp.log.1
#        4096    Jan 01 15:27:56 2009  vdc_2/
#        4096    Jan 01 15:27:56 2009  vdc_3/
#        4096    Jan 01 15:27:56 2009  vdc_4/
#         596    Feb 06 14:45:33 2009  vfc_cnv.log
#
# Usage for bootflash://sup-local
#   528846848 bytes used
#  1122058240 bytes free
#  1650905088 bytes total


def parse(text):

    results = [
        {
            "name":     u"Bootflash 容量",
            "id":       "InfStore",
            'icon':     'fa-hdd-o',
            "grp":      "infra",
            "unit":     'MB',
            "detail":   {}
        }
    ]

    for line in text:
        m_line = re.match(r'(\d+)\s+bytes\s+used', line, re.M | re.I)

        if m_line:
            m_used = int(m_line.group(1))
            continue

        m_line = re.match(r'(\d+)\s+bytes\s+free', line, re.M | re.I)
        if m_line:
            m_free = int(m_line.group(1))

    results[0]['total'] = round((m_free + m_used) / 1048576.0, 1)
    results[0]['used'] = round(m_used / 1048576.0, 1)
    results[0]['free'] = round(m_free / 1048576.0, 1)
    results[0]['rate'] = get_percent(results[0]['total'], results[0]['used'])
    results[0]['stat'] = get_status(results[0]['rate'])

    return results
