# -*- coding: utf-8

# cc: capacity contents
# ci: capacity item
# 每个 section 有一个层号(layer), layer 小的在底部, layer 大的在顶部, layer 号只比较相对大小

cc = {
    "infra":  {
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
    },
    "svc":  {
        "layer": 50,
        "name": u"服务资源",
        "ci_list": []
    }
}

parser_lookup = {
    'DIR BOOTFLASH:': 'dir_bootflash',
#    'SHOW HARDWARE CAPACITY INTERFACE': 'show_hardware_capacity_interface',
    'SHOW HARDWARE CAPACITY MODULE': 'show_hardware_capacity_module',
    'SHOW HARDWARE CAPACITY POWER': 'show_hardware_capacity_power',
    'SHOW HARDWARE FABRIC-UTILIZATION': 'show_hardware_fabric_util',
    'SHOW HARDWARE CAPACITY FORWARDING': 'show_hardware_capacity_forwarding',
    'SHOW HSRP SUMMARY': 'show_hsrp_summary',
    'SHOW INTERFACE BRIEF': 'show_interface_brief',
    'SHOW IP ARP SUMMARY': 'show_ip_arp_summary',
    'SHOW IP FIB ROUTE SUMMARY': 'show_ip_fib_route_summary',
    'SHOW IP OSPF NEIGHBORS': 'show_ip_ospf_neighbor',
    'SHOW IP ROUTE SUMMARY': 'show_ip_route_summary',
    'SHOW PORT-CHANNEL CAPACITY': 'show_port_channel_capacity',
    'SHOW SPANNING-TREE SUMMARY': 'show_spanning_tree_summary',
    'SHOW SYSTEM INTERNAL FORWARDING IP ROUTE SUMMARY': 'show_system_internal_FIRS',
    'SHOW VDC': 'show_vdc',
    'SHOW VDC RESOURCE': 'show_vdc_resource',
    'SHOW VDC RESOURCE DETAIL': 'show_vdc_resource_detail'
}

