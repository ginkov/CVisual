# -*- coding: utf-8
import re
from parsers import get_status, get_percent

# YQB-OPN-DIS3-SW1# show hardware capacity module
#
# Supervisor Redundancy HW State(Dual-SUPs):   Enabled
# Redundancy state: Active with HA standby
#
# Switching Resources:
# -------------------
# Module  Model Number      Part Number       Serial Number
# ---------------------------------------------------------
#  1      N7K-F248XP-25E    73-14976-02       JAF1644ATSC
#  2      N7K-F248XP-25E    73-14976-02       JAF1702BCCJ
#  3      N7K-F248XP-25E    73-14976-02       JAF1704ATTB
#  4      N7K-F248XP-25E    73-14976-02       JAF1725AAAJ
#  5      N7K-SUP2E         73-12098-04       JAF1649BCDA
#  6      N7K-SUP2E         73-12098-04       JAF1651ATFQ
#  7      N7K-F248XP-25E    73-14976-02       JAF1723ASRF
#  8      N7K-F248XP-25E    73-14976-02       JAF1723ASRA
#
# XBAR Resources:
# -------------------
# XbarNum Model Number      Part Number       Serial Number
# ---------------------------------------------------------
#  1      N7K-C7010-FAB-2   73-13199-02       JAF1649ATNM
#  2      N7K-C7010-FAB-2   73-13199-02       JAF1649AHDP
#  3      N7K-C7010-FAB-2   73-13199-02       JAF1649ATNH
#  4      N7K-C7010-FAB-2   73-13199-02       JAF1650ACFM
#  5      N7K-C7010-FAB-2   73-13199-02       JAF1650ACFT
#
# Flash/NVRAM Resources:
# ------------------------------------------------------------
#  Usage: Module  Device        Total(KB)    Free(KB)    %Used
# ------------------------------------------------------------
#           5      bootflash     1773912      294864     83
#           6      bootflash     1773912      589312     66
#           5      usb1          7802508     6665736     14


def parse(text):

    _MAX_MODULES = 8

    switching_rources_text = []
    flash_resources_text = []

    results = [
        {
            'name':     u'槽位资源',
            'id':       'PhySlot',
            'grp':      'phy',
            'icon':     'fa-server',
            'unit':     u'个',
            'detail':   {},
            'total':    _MAX_MODULES
        },
        {
            'name': u'Flash/USB 容量',
            'id': 'InfStore',
            'grp': 'infra',
            'icon': 'fa-hdd-o',
            'unit': 'KB',
            'table': {
                'data': [],
                'column': [
                    {'title': 'Module',     'data': 'module'},
                    {'title': 'Device',     'data': 'device'},
                    {'title': 'Total',      'data': 'total'},
                    {'title': 'Free',       'data': 'free'},
                    {'title': u'利用率%',  'data': 'used_percent'}
                ]
            },
            'detail': {}
        }
    ]

    flag = False

    for _line in text:
        if _line.startswith('Switching Resources:'):
            flag = True
        elif _line.startswith('Flash/NVRAM Resources:') or _line.startswith('XBAR Resources:'):
            flag = False

        if flag:
            switching_rources_text.append(_line)

    flag = False
    for _line in text:
        if _line.startswith('Flash/NVRAM Resources:'):
            flag = True

        if flag:
            flash_resources_text.append(_line)

    #
    # 处理 switching resources
    #

    header_lines_found = 0
    module_count = 0

    for _line in switching_rources_text:
        if header_lines_found < 3:
            if _line.startswith('--------') and header_lines_found == 0:
                header_lines_found = 1
            elif _line.startswith('Module ') and header_lines_found == 1:
                header_lines_found = 2
            elif _line.startswith('--------') and header_lines_found == 2:
                header_lines_found = 3
        else:
            m_line = re.match(r'(\d)+\s+(\S+)\s+\S+\s+\S+$', _line, re.M | re.I)
            if m_line:

                m_modn = int(m_line.group(1))

                if m_modn < 5 or m_modn > 6:
                    module_count += 1

                results[0]['detail']['solt_' + m_line.group(1)] = m_line.group(2)

            else:
                break

    results[0]['total'] = 8
    results[0]['used'] = module_count
    results[0]['free'] = results[0]['total'] - results[0]['used']
    results[0]['rate'] = get_percent(results[0]['total'], results[0]['used'])
    results[0]['stat'] = get_status(results[0]['rate'])

    #
    # 处理 Flash resources
    #

    header_lines_found = 0

    for _line in flash_resources_text:

        if header_lines_found < 3:
            if _line.startswith('--------') and header_lines_found == 0:
                header_lines_found = 1
            elif _line.startswith('Usage: ') and header_lines_found == 1:
                header_lines_found = 2
            elif _line.startswith('--------') and header_lines_found == 2:
                header_lines_found = 3

        else:

            m_flash = re.match(r'(\d+)+\s+(\S+)\s+(\d+)\s+(\d+)\s+(\d+)$', _line, re.M | re.I)

            if m_flash:
                flash = dict()
                flash['module'] = int(m_flash.group(1))
                flash['device'] = m_flash.group(2)
                flash['total'] = int(m_flash.group(3))
                flash['free'] = int(m_flash.group(4))
                flash['used_percent'] = float(m_flash.group(5))
                results[1]['table']['data'].append(flash)
            else:
                break

    max_used_flash = max(results[1]['table']['data'], key=lambda item: item['used_percent'])

    results[1]['total'] = max_used_flash['total']
    results[1]['used'] = max_used_flash['total'] - max_used_flash['free']
    results[1]['free'] = max_used_flash['free']

    results[1]['rate'] = get_percent(results[1]['total'], results[1]['used'])
    results[1]['stat'] = get_status(results[1]['rate'])

    return results
