# -*- coding: utf-8
import re
from parsers import get_percent, get_status

# YQB-OPN-DIS3-SW1# show hardware capacity power
#
# Power Resources Summary:
# ------------------------
# Power Supply redundancy mode(administratively):  PS-Redundant
# Power Supply redundancy mode(operationally):     PS-Redundant
# Total Power Capacity                            12000.00 W
# Power reserved for SUP,Fabric,and Fan Module(s)  2610.00 W ( 21.75 % )
# Power currently used by Modules                  2700.00 W ( 22.50 % )
# Total Power Available                            6690.00 W ( 55.75 % )
# Total Power Output (actual draw)                 2407.00 W


def parse(text):

    results = [
        {
            'name':     u'电源容量',
            "id":       "InfPower",
            "grp":      "infra",
            'unit':     'W',
            'icon':     "fa-plug",
            'detail':   {}
        }
    ]

    for _line in text:

        if _line:

            m_total_power = re.match(r'Total Power Capacity\s+(\S+)\s+W', _line, re.M | re.I)

            if m_total_power:
                results[0]['detail']['total_power'] = float(m_total_power.group(1))

            else:
                m_reserved_power = re.match(r'Power reserved .+\s(\S+)\s+W', _line, re.M | re.I)

                if m_reserved_power:
                    results[0]['detail']['reserved_power'] = float(m_reserved_power.group(1))
                else:
                    m_module_power = re.match(r'Power currently used by Modules\s+(\S+)\s+W', _line, re.M | re.I)

                    if m_module_power:
                        results[0]['detail']['module_power'] = float(m_module_power.group(1))

    results[0]['total'] = results[0]['detail']['total_power'] / 2.0  # 冗余电源,容量实际上只有一半
    results[0]['used'] = results[0]['detail']['reserved_power'] + results[0]['detail']['module_power']
    results[0]['free'] = results[0]['total'] - results[0]['used']

    results[0]['rate'] = get_percent(results[0]['total'], results[0]['used'])
    results[0]['stat'] = get_status(results[0]['rate'])

    return results
