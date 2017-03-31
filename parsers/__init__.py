# -*- coding: utf-8
u"""
为不同类型设备, 提供容量相关的 Show 命令解析器
不同类型的解析器放在不同目录中.

比如, n7k 目录下放的是 Cisco Nexus 7K 相关的各条命令解析器, 包括:

    /n7k/show_ip_route_summary.py
    /n7k/show_interface_brief.py
    /n7k/show_port_channel_capacity.py
    ...

格式约定:

    同一目录下的各文件为一组, 一个文件对应一个 Parser, 表示针对同一类型设备的 不同 show 命令的解析

Parser 的输入:

    def parse(text):

        其中 text 就是要解析的内容, 比如, show ip route 的结果, 以 String list 表示

Parser 的输出:

    因为一条 show 命令可能包含一个或多个容量指标的状态, 因此, 对单个 show 命令的解析结果
    是一个列表:

        result[ {容量 KPI 1 结果}, {容量 KPI 2 结果}, ...]

    每个容量 KPI 结果的信息如下:

    {
        'name':     KPI 指标名 (如物理端口数),
        'grp':      KPI 所属组的 id (为方便管理, 将 KPI 分为不同的组, 比如基础支持组, 物理资源, L2, L3, 服务等, 详见后"KPI 组")
        'id':       KPI 的 Id (通常以 grp_id + kpi_id, 比如 SvcAclt)
        'icon':     可选, 表示 KPI 的 icon (我们使用 Font-Awesome, 如 fa-list, fa-random 等)
        'rate':     表示利用率 {'used', 'free'} 以百分比表示, 可以用 parsers.get_percent() 函数计算出来
        'stat':     表示状态, 可用 parsers.get_status() 函数获得
        'table':    可选, 保存详细数据中的表格部分(如果有的话)
        {
            data: [ {'solt': 1, 'status': 'up'}, {'solt': 2, 'status': 'up'} ],
            column: [
                {'data': 'slot',   'title': u'槽位'},
                {'data': 'status', 'title': u'状态'}
            ]
        }
        'detail':   可选, 保存详细数据的字典部分(如果有的话)
        {
            'subject1': 'content1', 'subject2': 'content2'
        }
    }

KPI 分组

    对于一类设备, 比如 Nexus 7000, 有多种 KPI. 通常会把这些 KPI 分成多个组, 以方便管理和展示.

    这个信息放在每类设备目录的 __init__.py 文件中, 名为 cc 的字典里.

    例如:  n7k/__init__.py
        cc = {
            "inf":  {
                "layer": 10,
                "name": u"基础架构",
                "ci_list": []
            },
            "phy":  {
                "layer": 20,
                "name": u"物理资源",
                "ci_list": []
            },
            "l2":   {
                "layer": 30,
                "name": u"L2 资源",
                "ci_list": []
            },
            "l3":   {
                "layer": 40,
                "name": u"L3 资源",
                "ci_list": []
            }
        }

        其中 Layer 是各组的展次, layer 值越高越是上层.

查找 Parser

    在每类设备对应目录的 __init__.py 中, 定义了show 命令与 parser 文件的对应关系
    这个关系保存在名为 parser_lookup 的字典里

    例如: n5k/__init__.py 中

    parser_lookup = {
        'DIR BOOTFLASH:': 'dir_bootflash',
        'DIR LOG:': 'dir_log',
        'SHOW ENVIRONMENT POWER': 'show_environment_power',
        'SHOW FEX': 'show_fex',
        'SHOW HARDWARE CAPACITY INTERFACE': 'show_hardware_capacity_interface',
        'SHOW HSRP SUMMARY': 'show_hsrp_summary'
    }

    表示 "show fex" 这个命令的结果, 由 n5k/show_fex.py 这个解析文件进行处理.
"""

parser_lookup = {
    'DIR BOOTFLASH:-N7K': 'dir_bootflash',
    'DIR BOOTFLASH:-N5K': 'dir_bootflash',

    'DIR LOG:-N5K': 'dir_log_n5k',

    'SHOW ENVIRONMENT POWER-N5K': 'show_environment_power_n5k',

    'SHOW FEX-N5K': 'show_fex_n5k',

    'SHOW HARDWARE CAPACITY INTERFACE-N7K': 'show_hardware_capacity_interface',
    'SHOW HARDWARE CAPACITY INTERFACE-N5K': 'show_hardware_capacity_interface',

    'SHOW HARDWARE CAPACITY MODULE-N7K': 'show_hardware_capacity_module_n7k',

    'SHOW HARDWARE CAPACITY POWER-N7K': 'show_hardware_capacity_power_n7k',

    'SHOW HARDWARE FABRIC-UTILIZATION-N7K': 'show_hardware_fabric_util_n7k',

    'SHOW HARDWARE CAPACITY FORWARDING-N7K': 'show_hardware_capacity_forwarding_n7k',

    'SHOW HSRP SUMMARY-N7K': 'show_hsrp_summary',
    'SHOW HSRP SUMMARY-N5K': 'show_hsrp_summary',

    'SHOW INTERFACE BRIEF-N7K': 'show_interface_brief',
    'SHOW INTERFACE BRIEF-N5K': 'show_interface_brief',

    'SHOW IP ARP SUMMARY-N7K': 'show_ip_arp_summary',
    'SHOW IP ARP SUMMARY-N5K': 'show_ip_arp_summary',

    'SHOW IP FIB ROUTE SUMMARY-N7K': 'show_ip_fib_route_summary',
    'SHOW IP FIB ROUTE SUMMARY-N5K': 'show_ip_fib_route_summary',

    'SHOW IP OSPF NEIGHBORS-N7K': 'show_ip_ospf_neighbor',
    'SHOW IP OSPF NEIGHBORS-N5K': 'show_ip_ospf_neighbor',

    'SHOW IP ROUTE SUMMARY-N7K': 'show_ip_route_summary_n7k',
    'SHOW IP ROUTE SUMMARY-N5K': 'show_ip_route_summary_n5k',

    'SHOW MAC ADDRESS-TABLE COUNT-N5K': 'show_mac_address_table_count_n5k',

    'SHOW PLATFORM AFM INFO TCAM 0 REGION VACL-N5K': 'sh_platform_afm_IT0R_vacl_n5k',
    'SHOW PLATFORM AFM INFO TCAM 0 REGION IFACL-N5K': 'sh_platform_afm_IT0R_ifacl_n5k',
    'SHOW PLATFORM AFM INFO TCAM 0 REGION QOS-N5K': 'sh_platform_afm_IT0R_qos_n5k',
    'SHOW PLATFORM AFM INFO TCAM 0 REGION RBACL-N5K': 'sh_platform_afm_IT0R_rbacl_n5k',
    'SHOW PLATFORM AFM INFO TCAM 0 REGION SPAN-N5K': 'sh_platform_afm_IT0R_span_n5k',
    'SHOW PLATFORM AFM INFO TCAM 0 REGION SUP-N5K': 'sh_platform_afm_IT0R_sup_n5k',

    'SHOW PORT-CHANNEL CAPACITY-N7K': 'show_port_channel_capacity',
    'SHOW PORT-CHANNEL CAPACITY-N5K': 'show_port_channel_capacity',

    'SHOW SPANNING-TREE SUMMARY-N7K': 'show_spanning_tree_summary',
    'SHOW SPANNING-TREE SUMMARY-N5K': 'show_spanning_tree_summary',

    'SHOW SYSTEM INTERNAL FORWARDING IP ROUTE SUMMARY-N7K': 'show_system_internal_FIRS_n7k',

    'SHOW VDC-N7K': 'show_vdc_n7k',

    'SHOW VDC RESOURCE-N7K': 'show_vdc_resource_n7k',
    'SHOW VDC RESOURCE-N5K': 'show_vdc_resource_n5k',

    'SHOW VDC RESOURCE DETAIL-N7K': 'show_vdc_resource_detail',
    'SHOW VDC RESOURCE DETAIL-N5K': 'show_vdc_resource_detail'
}


def get_percent(total, used):
    u"""
    计算已用部分和可用部分在总量中的百分比
    :param total: 总量
    :param used: 已用
    :return: {used, free} 已用和可用部分的百分比
    """
    percent = {}

    if total > 0.001:

        percent['used'] = 100.0 * used / total
        percent['free'] = 100.0 - percent['used']

    else:

        percent['used'] = 0.0
        percent['free'] = 0.0

    return percent


def get_status(percentage, thresholds=[75, 50]):
    u"""
    根据使用的百分比, 计算当前的状态
    两个道阈值, 可以自定义
    :param percentage: {'used': used, 'free': free }
    :param thresholds: [ warning_threshold, danger_threshold ]
    :return: 'danger' | 'warning' | 'normal'
    """
    if percentage["used"] > thresholds[0]:
        return "danger"
    elif percentage["used"] > thresholds[1]:
        return "warning"
    else:
        return "normal"



