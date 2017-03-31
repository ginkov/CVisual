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
#    'DIR BOOTFLASH:': 'dir_bootflash',
#    'DIR LOG:': 'dir_log',
    'SHOW ENVIRONMENT POWER': 'show_environment_power',
    'SHOW FEX': 'show_fex',
    'SHOW HARDWARE CAPACITY INTERFACE': 'show_hardware_capacity_interface',
    'SHOW HSRP SUMMARY': 'show_hsrp_summary',
    'SHOW INTERFACE BRIEF': 'show_interface_brief',
    'SHOW IP ARP SUMMARY': 'show_ip_arp_summary',
    'SHOW IP FIB ROUTE SUMMARY': 'show_ip_fib_route_summary',
#    'SHOW IP OSPF NEIGHBORS': 'show_ip_ospf_neighbor',
    'SHOW IP ROUTE SUMMARY': 'show_ip_route_summary',
    'SHOW MAC ADDRESS-TABLE COUNT': 'show_mac_address_table_count',
    'SHOW PLATFORM AFM INFO TCAM 0 REGION VACL': 'sh_platform_afm_IT0R_vacl',
    'SHOW PLATFORM AFM INFO TCAM 0 REGION IFACL': 'sh_platform_afm_IT0R_ifacl',
    'SHOW PLATFORM AFM INFO TCAM 0 REGION QOS': 'sh_platform_afm_IT0R_qos',
    'SHOW PLATFORM AFM INFO TCAM 0 REGION RBACL': 'sh_platform_afm_IT0R_rbacl',
    'SHOW PLATFORM AFM INFO TCAM 0 REGION SPAN': 'sh_platform_afm_IT0R_span',
    'SHOW PLATFORM AFM INFO TCAM 0 REGION SUP': 'sh_platform_afm_IT0R_sup',
    'SHOW PORT-CHANNEL CAPACITY': 'show_port_channel_capacity',
    'SHOW SPANNING-TREE SUMMARY': 'show_spanning_tree_summary',
    'SHOW VDC RESOURCE': 'show_vdc_resource',
    'SHOW VDC RESOURCE DETAIL': 'show_vdc_resource_detail'
}
