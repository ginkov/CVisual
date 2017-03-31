# -*- coding: utf-8
import re
from parsers import get_status, get_percent


def parse(text):

    results = [
        {
            'name':     u'MAC地址TCAM表',
            'id':       'L2Mac',
            'grp':      'l2',
            'icon':     'fa-barcode',
            'unit':     'KB',
            'table': {
                'data': [
                    {'module': 1, 'util': 0.0},
                    {'module': 2, 'util': 0.0},
                    {'module': 3, 'util': 0.0},
                    {'module': 4, 'util': 0.0},
                    {'module': 5, 'util': 0.0, 'inst': '', 'tcam': '', 'used': ''},
                    {'module': 6, 'util': 0.0, 'inst': '', 'tcam': '', 'used': ''},
                    {'module': 7, 'util': 0.0},
                    {'module': 8, 'util': 0.0}
                ],
                'column': [
                    {'title': 'Module',     'data': 'module'},
                    # {'title': u'实例',       'data': 'inst'},
                    {'title': 'Inst',       'data': 'inst'},
                    {'title': 'Tcam',       'data': 'tcam'},
                    # {'title': u'已用',       'data': 'used'},
                    {'title': 'Used',       'data': 'used'},
                    # {'title': u'利用率%',    'data': 'util'}
                    {'title': '%',    'data': 'util'}
                ]
            }
        },
        {
            'name':     u'QoS 聚合 Policer',
            'id':       'SvcQost',
            'grp':      'svc',
            'icon':     'fa-filter',
            'unit':     u'个',
            'table': {
                'data': [],
                'column': [
                    {'title': 'Module',     'data': 'module'},
                    {'title': 'Total',      'data': 'total'},
                    {'title': 'Used',       'data': 'used'},
                    # {'title': u'利用率%',          'data': 'util'},
                    {'title': '%',          'data': 'util'}
                ]
            }
        },
        {
            'name':     u'ACL Tcam',
            'id':       'SvcAclt',
            'grp':      'svc',
            'unit':     u'条',
            'icon':     'fa-microchip',
            'detail':   {},
            'table': {
                'data': [
                    {'module': 1, 'inst': '', 'bank': 0, 'used': 0, 'free': 0, 'util': 0.0},
                    {'module': 2, 'inst': '', 'bank': 0, 'used': 0, 'free': 0, 'util': 0.0},
                    {'module': 3, 'inst': '', 'bank': 0, 'used': 0, 'free': 0, 'util': 0.0},
                    {'module': 4, 'inst': '', 'bank': 0, 'used': 0, 'free': 0, 'util': 0.0},
                    {'module': 5, 'inst': '', 'bank': 0, 'used': 0, 'free': 0, 'util': 0.0},
                    {'module': 6, 'inst': '', 'bank': 0, 'used': 0, 'free': 0, 'util': 0.0},
                    {'module': 7, 'inst': '', 'bank': 0, 'used': 0, 'free': 0, 'util': 0.0},
                    {'module': 8, 'inst': '', 'bank': 0, 'used': 0, 'free': 0, 'util': 0.0}
                ],
                'column': [
                    {'title': 'Module',     'data': 'module'},
                    {'title': 'Inst',       'data': 'inst'},
                    {'title': 'Bank',       'data': 'bank'},
                    {'title': 'Used',       'data': 'used'},
                    {'title': 'Free',       'data': 'free'},
                    {'title': u'利用率%',    'data': 'util'}
                ]
            }
        }
    ]

    l2_resources_section = []
    qos_resources_section = []
    acl_resources_seciton = []

#
#  本命令输出的内容非常多, 把相关的内容摘出来, 分到不同的 Section 处理
#

    flag = False
    for _line in text:

        if _line.startswith('L2 Forwarding Resources'):
            flag = True
        elif _line.startswith('INSTANCE 0x0'):
            break

        if flag:
            l2_resources_section.append(_line)

    flag = False
    for _line in text:

        if _line.startswith('INSTANCE 0x0'):
            flag = True
        elif _line.startswith('Key: Log/Phys = Logical entries / Physical '):
            break

        if flag:
            acl_resources_seciton.append(_line)

    flag = False
    for _line in text:

        if _line.startswith('QoS Resource Utilization'):
            flag = True

        if flag:
            qos_resources_section.append(_line)

#
# 开始各 section 的逻辑处理
#

    for _line in l2_resources_section:
        m_line = re.match(r'(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+\d+\s+\d+\s+\d+\s+\d', _line, re.M | re.I)
        if m_line:
            m_modn = int(m_line.group(1)) - 1
            m_inst = int(m_line.group(2))
            m_tcam = int(m_line.group(3))
            m_used = int(m_line.group(4))

            m_percent = round(100*float(m_used) / float(m_tcam), 2)

            if 'util' in results[0]['table']['data'][m_modn]:
                if m_percent > results[0]['table']['data'][m_modn]['util']:
                    results[0]['table']['data'][m_modn]['util'] = m_percent
                    results[0]['table']['data'][m_modn]['inst'] = m_inst
                    results[0]['table']['data'][m_modn]['tcam'] = m_tcam
                    results[0]['table']['data'][m_modn]['used'] = m_used
            else:
                results[0]['table']['data'][m_modn]['util'] = m_percent
                results[0]['table']['data'][m_modn]['inst'] = m_inst
                results[0]['table']['data'][m_modn]['tcam'] = m_tcam
                results[0]['table']['data'][m_modn]['used'] = m_used

    for _line in qos_resources_section:

        m_line = re.match(r'Aggregate policers:\s+(\d+)\s+(\d+)\s+(\d+)\s+\d+', _line, re.M | re.I)
        if m_line:
            m_modn = int(m_line.group(1))
            m_item = {
                'module': m_modn,
                'total': int(m_line.group(2)),
                'used': int(m_line.group(3)),
                'util': round(100*float(m_line.group(3)) / float(m_line.group(2)), 2)
            }
            results[1]['table']['data'].append(m_item)

    for _line in acl_resources_seciton:

        m_line = re.match(r'^INSTANCE (\S+)$', _line, re.M | re.I)
        if m_line:
            m_inst = m_line.group(1)

        m_line = re.match(r'ACL Hardware Resource Utilization \(Mod\s+(\d+)', _line, re.M | re.I)
        if m_line:
            m_modn = int(m_line.group(1)) - 1

        m_line = re.match(r'Bank (\d) \[Tcam 0 \+ Tcam 1\]\s+(\d+)\s+(\d+)\s+(\S+)', _line, re.M | re.I)
        if m_line:
            m_bank = int(m_line.group(1))
            m_used = int(m_line.group(2))
            m_free = int(m_line.group(3))
            m_util = float(m_line.group(4))

            if m_util > results[2]['table']['data'][m_modn]['util']:
                results[2]['table']['data'][m_modn]['inst'] = m_inst
                results[2]['table']['data'][m_modn]['bank'] = m_bank
                results[2]['table']['data'][m_modn]['used'] = m_used
                results[2]['table']['data'][m_modn]['free'] = m_free
                results[2]['table']['data'][m_modn]['util'] = m_util

    module_max = max(results[0]['table']['data'], key=lambda item: item['util'])
    results[0]['total'] = module_max['tcam']
    results[0]['used'] = module_max['used']
    results[0]['free'] = results[0]['total'] - results[0]['used']
    results[0]['rate'] = get_percent(results[0]['total'], results[0]['used'])
    results[0]['stat'] = get_status(results[0]['rate'])

    module_max = max(results[1]['table']['data'], key=lambda item: item['util'])
    results[1]['total'] = module_max['total']
    results[1]['used'] = module_max['used']
    results[1]['free'] = results[1]['total'] - results[1]['used']
    results[1]['rate'] = get_percent(results[1]['total'], results[1]['used'])
    results[1]['stat'] = get_status(results[1]['rate'])

    module_max = max(results[2]['table']['data'], key=lambda item: item['util'])
    results[2]['total'] = module_max['used'] + module_max['free']
    results[2]['used'] = module_max['used']
    results[2]['free'] = module_max['free']
    results[2]['rate'] = get_percent(results[2]['total'], results[2]['used'])
    results[2]['stat'] = get_status(results[2]['rate'])

    return results


# YQB-OPN-DIS3-SW1(config)# show hardware capacity forwarding
# L2 Forwarding Resources
# -------------------------
#   L2 entries: Module inst   total    used   mcast   ucast   lines   lines_full
# ------------------------------------------------------------------------------
#               1         0   16384    7317       0    7317     512            0
#               1         1   16384    7317       0    7317     512            0
#               1         2   16384    7317       0    7317     512            0
#               1         3   16384    7317       0    7317     512            0
#               1         4   16384    7317       0    7317     512            0
#               1         5   16384    7317       0    7317     512            0
#               1         6   16384    7317       0    7317     512            0
#               1         7   16384    7317       0    7317     512            0
#               1         8   16384    7317       0    7317     512            0
#               1         9   16384    7317       0    7317     512            0
#               1        10   16384    7317       0    7317     512            0
#               1        11   16384    7317       0    7317     512            0
#
#
# L2 Forwarding Resources
# -------------------------
#   L2 entries: Module inst   total    used   mcast   ucast   lines   lines_full
# ------------------------------------------------------------------------------
#               2         0   16384    7317       0    7317     512            0
#               2         1   16384    7317       0    7317     512            0
#               2         2   16384    7317       0    7317     512            0
#               2         3   16384    7317       0    7317     512            0
#               2         4   16384    7317       0    7317     512            0
#               2         5   16384    7317       0    7317     512            0
#               2         6   16384    7317       0    7317     512            0
#               2         7   16384    7317       0    7317     512            0
#               2         8   16384    7317       0    7317     512            0
#               2         9   16384    7317       0    7317     512            0
#               2        10   16384    7317       0    7317     512            0
#               2        11   16384    7317       0    7317     512            0
#
#
# L2 Forwarding Resources
# -------------------------
#   L2 entries: Module inst   total    used   mcast   ucast   lines   lines_full
# ------------------------------------------------------------------------------
#               3         0   16384    7317       0    7317     512            0
#               3         1   16384    7317       0    7317     512            0
#               3         2   16384    7317       0    7317     512            0
#               3         3   16384    7317       0    7317     512            0
#               3         4   16384    7317       0    7317     512            0
#               3         5   16384    7317       0    7317     512            0
#               3         6   16384    7317       0    7317     512            0
#               3         7   16384    7317       0    7317     512            0
#               3         8   16384    7317       0    7317     512            0
#               3         9   16384    7317       0    7317     512            0
#               3        10   16384    7317       0    7317     512            0
#               3        11   16384    7317       0    7317     512            0
#
#
# L2 Forwarding Resources
# -------------------------
#   L2 entries: Module inst   total    used   mcast   ucast   lines   lines_full
# ------------------------------------------------------------------------------
#               4         0   16384    7317       0    7317     512            0
#               4         1   16384    7317       0    7317     512            0
#               4         2   16384    7317       0    7317     512            0
#               4         3   16384    7317       0    7317     512            0
#               4         4   16384    7317       0    7317     512            0
#               4         5   16384    7317       0    7317     512            0
#               4         6   16384    7317       0    7317     512            0
#               4         7   16384    7317       0    7317     512            0
#               4         8   16384    7317       0    7317     512            0
#               4         9   16384    7317       0    7317     512            0
#               4        10   16384    7317       0    7317     512            0
#               4        11   16384    7317       0    7317     512            0
#
#
# L2 Forwarding Resources
# -------------------------
#   L2 entries: Module inst   total    used   mcast   ucast   lines   lines_full
# ------------------------------------------------------------------------------
#               7         0   16384    7317       0    7317     512            0
#               7         1   16384    7317       0    7317     512            0
#               7         2   16384    7317       0    7317     512            0
#               7         3   16384    7317       0    7317     512            0
#               7         4   16384    7317       0    7317     512            0
#               7         5   16384    7317       0    7317     512            0
#               7         6   16384    7317       0    7317     512            0
#               7         7   16384    7317       0    7317     512            0
#               7         8   16384    7317       0    7317     512            0
#               7         9   16384    7317       0    7317     512            0
#               7        10   16384    7317       0    7317     512            0
#               7        11   16384    7317       0    7317     512            0
#
#
# L2 Forwarding Resources
# -------------------------
#   L2 entries: Module inst   total    used   mcast   ucast   lines   lines_full
# ------------------------------------------------------------------------------
#               8         0   16384    7317       0    7317     512            0
#               8         1   16384    7317       0    7317     512            0
#               8         2   16384    7317       0    7317     512            0
#               8         3   16384    7317       0    7317     512            0
#               8         4   16384    7317       0    7317     512            0
#               8         5   16384    7317       0    7317     512            0
#               8         6   16384    7317       0    7317     512            0
#               8         7   16384    7317       0    7317     512            0
#               8         8   16384    7317       0    7317     512            0
#               8         9   16384    7317       0    7317     512            0
#               8        10   16384    7317       0    7317     512            0
#               8        11   16384    7317       0    7317     512            0
#
#
#
# INSTANCE 0x0
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 1)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  669     7523    8.17
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   2       1533    0.13
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x1
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 1)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  1060    7132    12.94
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      5       486     1.01
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x2
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 1)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  737     7455    9.00
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      4       487     0.81
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x3
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 1)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  737     7455    9.00
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      4       487     0.81
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x4
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 1)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  737     7455    9.00
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      4       487     0.81
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x5
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 1)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  737     7455    9.00
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      4       487     0.81
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x6
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 1)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  596     7596    7.28
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   5       1530    0.32
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x7
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 1)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  596     7596    7.28
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   5       1530    0.32
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x8
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 1)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  601     7591    7.34
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   6       1529    0.39
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x9
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 1)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  601     7591    7.34
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   6       1529    0.39
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0xa
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 1)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  601     7591    7.34
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   6       1529    0.39
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0xb
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 1)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  858     7334    10.47
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   8       1527    0.52
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      4       487     0.81
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x0
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 2)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  669     7523    8.17
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   2       1533    0.13
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x1
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 2)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  1060    7132    12.94
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      5       486     1.01
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x2
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 2)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  737     7455    9.00
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      4       487     0.81
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x3
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 2)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  737     7455    9.00
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      4       487     0.81
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x4
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 2)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  737     7455    9.00
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      4       487     0.81
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x5
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 2)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  737     7455    9.00
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      4       487     0.81
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x6
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 2)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  596     7596    7.28
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   5       1530    0.32
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x7
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 2)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  596     7596    7.28
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   5       1530    0.32
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x8
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 2)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  601     7591    7.34
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   6       1529    0.39
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x9
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 2)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  601     7591    7.34
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   6       1529    0.39
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0xa
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 2)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  601     7591    7.34
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   6       1529    0.39
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0xb
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 2)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  858     7334    10.47
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   8       1527    0.52
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      4       487     0.81
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x0
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 3)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  601     7591    7.34
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   6       1529    0.39
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   131074  254     0.78
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x1
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 3)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  601     7591    7.34
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   6       1529    0.39
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   131074  254     0.78
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x2
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 3)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  601     7591    7.34
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   6       1529    0.39
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   131074  254     0.78
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x3
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 3)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  579     7613    7.07
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   131074  254     0.78
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x4
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 3)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  579     7613    7.07
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   131074  254     0.78
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x5
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 3)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  737     7455    9.00
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      4       487     0.81
#
# Ingress Dest info table   131074  254     0.78
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x6
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 3)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  346     7846    4.22
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   2       1533    0.13
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      2       489     0.40
#
# Ingress Dest info table   131074  254     0.78
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x7
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 3)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  346     7846    4.22
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   2       1533    0.13
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      2       489     0.40
#
# Ingress Dest info table   131074  254     0.78
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x8
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 3)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  345     7847    4.21
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   2       1533    0.13
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      2       489     0.40
#
# Ingress Dest info table   131074  254     0.78
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x9
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 3)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  296     7896    3.61
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   1       1534    0.06
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      2       489     0.40
#
# Ingress Dest info table   131074  254     0.78
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0xa
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 3)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  296     7896    3.61
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   1       1534    0.06
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      2       489     0.40
#
# Ingress Dest info table   131074  254     0.78
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0xb
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 3)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  296     7896    3.61
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   1       1534    0.06
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      2       489     0.40
#
# Ingress Dest info table   131074  254     0.78
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x0
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 4)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  601     7591    7.34
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   6       1529    0.39
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   131074  254     0.78
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x1
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 4)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  924     7268    11.28
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   6       1529    0.39
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      4       487     0.81
#
# Ingress Dest info table   131074  254     0.78
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x2
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 4)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  601     7591    7.34
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   6       1529    0.39
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   131074  254     0.78
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x3
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 4)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  579     7613    7.07
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   131074  254     0.78
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x4
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 4)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  579     7613    7.07
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   131074  254     0.78
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x5
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 4)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  324     7868    3.96
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   2       1533    0.13
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      2       489     0.40
#
# Ingress Dest info table   131074  254     0.78
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x6
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 4)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  346     7846    4.22
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   2       1533    0.13
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      2       489     0.40
#
# Ingress Dest info table   131074  254     0.78
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x7
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 4)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  346     7846    4.22
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   2       1533    0.13
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      2       489     0.40
#
# Ingress Dest info table   131074  254     0.78
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x8
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 4)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  296     7896    3.61
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   1       1534    0.06
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      2       489     0.40
#
# Ingress Dest info table   131074  254     0.78
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x9
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 4)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  296     7896    3.61
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   1       1534    0.06
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      2       489     0.40
#
# Ingress Dest info table   131074  254     0.78
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0xa
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 4)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  296     7896    3.61
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   1       1534    0.06
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      2       489     0.40
#
# Ingress Dest info table   131074  254     0.78
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0xb
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 4)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  296     7896    3.61
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   1       1534    0.06
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      2       489     0.40
#
# Ingress Dest info table   131074  254     0.78
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x0
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 7)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  619     7573    7.56
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   1       1534    0.06
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x1
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 7)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  737     7455    9.00
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      4       487     0.81
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x2
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 7)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  737     7455    9.00
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      4       487     0.81
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x3
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 7)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  737     7455    9.00
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      4       487     0.81
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x4
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 7)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  737     7455    9.00
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      4       487     0.81
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x5
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 7)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  737     7455    9.00
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      4       487     0.81
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x6
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 7)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  596     7596    7.28
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   5       1530    0.32
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x7
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 7)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  596     7596    7.28
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   5       1530    0.32
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x8
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 7)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  596     7596    7.28
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   5       1530    0.32
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x9
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 7)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  579     7613    7.07
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0xa
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 7)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  579     7613    7.07
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0xb
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 7)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  296     7896    3.61
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   1       1534    0.06
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      2       489     0.40
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x0
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 8)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  619     7573    7.56
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   1       1534    0.06
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x1
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 8)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  737     7455    9.00
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      4       487     0.81
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x2
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 8)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  737     7455    9.00
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      4       487     0.81
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x3
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 8)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  737     7455    9.00
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      4       487     0.81
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x4
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 8)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  737     7455    9.00
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      4       487     0.81
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x5
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 8)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  737     7455    9.00
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      4       487     0.81
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x6
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 8)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  596     7596    7.28
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   5       1530    0.32
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x7
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 8)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  596     7596    7.28
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   5       1530    0.32
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x8
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 8)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  596     7596    7.28
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   5       1530    0.32
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0x9
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 8)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  579     7613    7.07
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0xa
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 8)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  579     7613    7.07
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   4       1531    0.26
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      3       488     0.61
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
#
# INSTANCE 0xb
# -------------
#
#
#          ACL Hardware Resource Utilization (Mod 8)
#          --------------------------------------------
#                           Used    Free    Percent
#                                           Utilization
# -----------------------------------------------------
# Bank 0 [Tcam 0 + Tcam 1]  296     7896    3.61
# Bank 1 [Tcam 0 + Tcam 1]  322     7870    3.93
#
# LOU                       4       100     3.84
# Both LOU Operands         4
# Single LOU Operands       0
# LOU L4 src port:          0
# LOU L4 dst port:          0
# LOU L3 packet len:        0
# LOU IP tos:               0
# LOU IP dscp:              0
# LOU ip precedence:        0
# LOU ip TTL:               0
# TCP Flags                 0       16      0.00
#
# Protocol CAM              3       4       42.85
# Mac Etype/Proto CAM       9       5       64.28
#
# Non L4op labels, Tcam 0   0       1535    0.00
# Non L4op labels, Tcam 1   1       1534    0.06
# L4 op labels, Tcam 0      0       491     0.00
# L4 op labels, Tcam 1      2       489     0.40
#
# Ingress Dest info table   65538   255     0.39
# Egress Dest info table    65537   255     0.39
#
# Key: Log/Phys = Logical entries / Physical 72-bit entries
# Note: Utilization may not reach the maximum.
#
# Module 1 usage:
# TCAM usage statistics for instance :0
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :1
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :2
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :3
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :4
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :5
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :6
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :7
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :8
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :9
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      37
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          15301/15301     62    24576/24576
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         22016          11008                     5504
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :10
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      56
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                           7109/7109      43    16384/16384
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         30208          15104                     7552
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :11
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
#
# Key: Log/Phys = Logical entries / Physical 72-bit entries
# Note: Utilization may not reach the maximum.
#
# Module 2 usage:
# TCAM usage statistics for instance :0
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :1
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :2
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :3
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :4
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :5
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :6
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :7
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :8
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :9
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      37
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          15301/15301     62    24576/24576
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         22016          11008                     5504
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :10
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      56
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                           7109/7109      43    16384/16384
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         30208          15104                     7552
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :11
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
#
# Key: Log/Phys = Logical entries / Physical 72-bit entries
# Note: Utilization may not reach the maximum.
#
# Module 3 usage:
# TCAM usage statistics for instance :0
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :1
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :2
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :3
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :4
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      39
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          14277/14277     60    23552/23552
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         23040          11520                     5760
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :5
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      39
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          14277/14277     60    23552/23552
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         23040          11520                     5760
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :6
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :7
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      56
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                           7109/7109      43    16384/16384
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         30208          15104                     7552
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :8
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :9
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :10
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :11
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
#
# Key: Log/Phys = Logical entries / Physical 72-bit entries
# Note: Utilization may not reach the maximum.
#
# Module 4 usage:
# TCAM usage statistics for instance :0
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :1
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :2
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :3
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :4
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      39
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          14277/14277     60    23552/23552
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         23040          11520                     5760
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :5
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      39
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          14277/14277     60    23552/23552
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         23040          11520                     5760
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :6
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :7
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :8
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :9
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :10
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :11
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
#
# Key: Log/Phys = Logical entries / Physical 72-bit entries
# Note: Utilization may not reach the maximum.
#
# Module 7 usage:
# TCAM usage statistics for instance :0
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :1
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :2
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :3
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :4
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :5
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :6
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :7
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :8
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :9
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      56
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                           7109/7109      43    16384/16384
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         30208          15104                     7552
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :10
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      37
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          15301/15301     62    24576/24576
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         22016          11008                     5504
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :11
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
#
# Key: Log/Phys = Logical entries / Physical 72-bit entries
# Note: Utilization may not reach the maximum.
#
# Module 8 usage:
# TCAM usage statistics for instance :0
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :1
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :2
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :3
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :4
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :5
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :6
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :7
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :8
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :9
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      56
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                           7109/7109      43    16384/16384
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         30208          15104                     7552
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :10
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      37
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          15301/15301     62    24576/24576
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         22016          11008                     5504
# ----------------------------------------------------------------------------
# TCAM usage statistics for instance :11
#
# Route Type              Used      %Used      Free      %Free      Total
#                      (Log/Phys)            (Log/Phys)           (Log/Phys)
# ---------------------------------------------------------------------------
# IPv4 Unicast:        9275/9275      34
# FCOE key :              0/0          0
#                                        -------------------------------------
#                                          17861/17861     65    27136/27136
#                                        -------------------------------------
# IPv4 Multicast:         4/8          0
# IPv6 Unicast:           3/6          0
#                                        -------------------------------------
#                                           1263/2526      99     1270/2540
#                                        -------------------------------------
# IPv6 Multicast:         5/20         0
#                                        -------------------------------------
#                                            631/2524      99      636/2544
#                                        -------------------------------------
# Free Logical Entries    IPV4 ucast  or IPV4 mcast/IPV6 ucast  or IPV6 mcast
#                         19456          9728                      4864
# ----------------------------------------------------------------------------
#
# Adjacency table usage.
# Module 1 usage:
#
# Adjacency usage statistics for Instance 0
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 1
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 2
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 3
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 4
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 5
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 6
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 7
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 8
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 9
# Feature             Used     %Used
# -------------------------------------
# UFIB                6689      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6699      FREE: 9612      TOTAL: 16311
#
# Adjacency usage statistics for Instance 10
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 11
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency table usage.
# Module 2 usage:
#
# Adjacency usage statistics for Instance 0
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 1
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 2
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 3
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 4
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 5
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 6
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 7
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 8
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 9
# Feature             Used     %Used
# -------------------------------------
# UFIB                6689      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6699      FREE: 9612      TOTAL: 16311
#
# Adjacency usage statistics for Instance 10
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 11
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency table usage.
# Module 3 usage:
#
# Adjacency usage statistics for Instance 0
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 1
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 2
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 3
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 4
# Feature             Used     %Used
# -------------------------------------
# UFIB                6675      40
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6685      FREE: 9626      TOTAL: 16311
#
# Adjacency usage statistics for Instance 5
# Feature             Used     %Used
# -------------------------------------
# UFIB                6675      40
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6685      FREE: 9626      TOTAL: 16311
#
# Adjacency usage statistics for Instance 6
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 7
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 8
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 9
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 10
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 11
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency table usage.
# Module 4 usage:
#
# Adjacency usage statistics for Instance 0
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 1
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 2
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 3
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 4
# Feature             Used     %Used
# -------------------------------------
# UFIB                6675      40
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6685      FREE: 9626      TOTAL: 16311
#
# Adjacency usage statistics for Instance 5
# Feature             Used     %Used
# -------------------------------------
# UFIB                6675      40
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6685      FREE: 9626      TOTAL: 16311
#
# Adjacency usage statistics for Instance 6
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 7
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 8
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 9
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 10
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 11
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency table usage.
# Module 7 usage:
#
# Adjacency usage statistics for Instance 0
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 1
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 2
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 3
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 4
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 5
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 6
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 7
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 8
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 9
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 10
# Feature             Used     %Used
# -------------------------------------
# UFIB                6673      40
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6683      FREE: 9628      TOTAL: 16311
#
# Adjacency usage statistics for Instance 11
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency table usage.
# Module 8 usage:
#
# Adjacency usage statistics for Instance 0
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 1
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 2
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 3
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 4
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 5
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 6
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 7
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 8
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 9
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
#
# Adjacency usage statistics for Instance 10
# Feature             Used     %Used
# -------------------------------------
# UFIB                6673      40
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6683      FREE: 9628      TOTAL: 16311
#
# Adjacency usage statistics for Instance 11
# Feature             Used     %Used
# -------------------------------------
# UFIB                6693      41
# MFIB                7         0
# FCFIB               2         0
# VACL                1         0
# USED: 6703      FREE: 9608      TOTAL: 16311
# LS_MET table usage. (UFIB, FCFIB share one region, MFIB has one region)
#
# LS_MET usage statistics for Instance 0
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 1
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 2
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 3
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 4
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 5
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 6
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 7
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 8
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 9
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 10
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 11
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
# LS_MET table usage. (UFIB, FCFIB share one region, MFIB has one region)
#
# LS_MET usage statistics for Instance 0
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 1
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 2
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 3
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 4
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 5
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 6
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 7
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 8
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 9
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 10
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 11
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
# LS_MET table usage. (UFIB, FCFIB share one region, MFIB has one region)
#
# LS_MET usage statistics for Instance 0
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 1
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 2
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 3
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 4
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 5
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 6
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 7
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 8
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 9
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 10
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 11
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
# LS_MET table usage. (UFIB, FCFIB share one region, MFIB has one region)
#
# LS_MET usage statistics for Instance 0
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 1
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 2
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 3
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 4
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 5
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 6
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 7
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 8
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 9
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 10
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 11
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
# LS_MET table usage. (UFIB, FCFIB share one region, MFIB has one region)
#
# LS_MET usage statistics for Instance 0
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 1
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 2
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 3
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 4
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 5
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 6
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 7
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 8
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 9
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 10
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 11
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
# LS_MET table usage. (UFIB, FCFIB share one region, MFIB has one region)
#
# LS_MET usage statistics for Instance 0
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 1
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 2
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 3
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 4
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 5
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 6
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 7
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 8
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 9
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 10
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# LS_MET usage statistics for Instance 11
# Feature        Used     %Used   Free    Total   mcast-groups
# ----------------------------------------------------
# UFIB ECMP      0         0.00      32768     32768
# FCFIB ECMP     0         0.00      32768     32768
# MFIB MET       0         0.00      16384     16384     0
#
# QoS Resource Utilization
# ------------------------
#
# Resource                      Module    Total        Used         Free
# --------                      ------    -----        ----         ----
# Aggregate policers:               1     12288        168          12120
# Distributed policers:             1     12288        0            12288
# Policer Profiles:                 1     3072         132          2940
#
# QoS Resource Utilization
# ------------------------
#
# Resource                      Module    Total        Used         Free
# --------                      ------    -----        ----         ----
# Aggregate policers:               2     12288        168          12120
# Distributed policers:             2     12288        0            12288
# Policer Profiles:                 2     3072         132          2940
#
# QoS Resource Utilization
# ------------------------
#
# Resource                      Module    Total        Used         Free
# --------                      ------    -----        ----         ----
# Aggregate policers:               3     12288        168          12120
# Distributed policers:             3     12288        0            12288
# Policer Profiles:                 3     3072         132          2940
#
# QoS Resource Utilization
# ------------------------
#
# Resource                      Module    Total        Used         Free
# --------                      ------    -----        ----         ----
# Aggregate policers:               4     12288        168          12120
# Distributed policers:             4     12288        0            12288
# Policer Profiles:                 4     3072         132          2940
#
# QoS Resource Utilization
# ------------------------
#
# Resource                      Module    Total        Used         Free
# --------                      ------    -----        ----         ----
# Aggregate policers:               7     12288        168          12120
# Distributed policers:             7     12288        0            12288
# Policer Profiles:                 7     3072         132          2940
#
# QoS Resource Utilization
# ------------------------
#
# Resource                      Module    Total        Used         Free
# --------                      ------    -----        ----         ----
# Aggregate policers:               8     12288        168          12120
# Distributed policers:             8     12288        0            12288
# Policer Profiles:                 8     3072         132          2940
#
