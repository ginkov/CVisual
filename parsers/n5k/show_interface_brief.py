# -*- coding: utf-8

import re
from parsers import get_status, get_percent


def parse(text):

    results = [
        {
            'name': u"以太网端口使用情况",
            "id": "PhyPort",
            "grp": "phy",
            "icon": "fa-caret-square-o-up",
            'unit': u'个',
            'free': 0,
            'table': {
                'data': [],
                'column': [
                    {'title': 'Interface',   'data': 'ifname'},
                    {'title': u'状态',        'data': 'status'},
                    {'title': u'说明',        'data': 'reason'}
                ]
            }
        }
    ]

    header_count = 0
    for _line in text:
        if header_count < 4:
            if _line.startswith('--------') and header_count == 0:
                header_count = 1
            elif _line.startswith('Ethernet ') and header_count == 1:
                header_count = 2
            elif _line.startswith('Interface') and header_count == 2:
                header_count = 3
            elif _line.startswith('--------') and header_count == 3:
                header_count = 4
            else:
                header_count = 0
        else:
            m_ether = re.match(r'(Eth\S+)\s+\S+\s+\S+\s+\w+\s+(\w+)\s+(.{18})\s+', _line, re.M | re.I)
            if m_ether:
                results[0]['table']['data'].append({
                    'ifname': m_ether.group(1),
                    'status': m_ether.group(2),
                    'reason': m_ether.group(3).strip()
                })
            else:
                break

    results[0]['total'] = len(results[0]['table']['data'])

#   只有 Admin Down 的才算 unused
    for ethernet_if in results[0]['table']['data']:
        if ethernet_if['status'] == 'down' and ethernet_if['reason'].startswith('Administratively'):
            results[0]['free'] += 1
        if ethernet_if['status'] == 'down' and ethernet_if['reason'].startswith('SFP not ins'):
            results[0]['free'] += 1

    results[0]['used'] = results[0]['total'] - results[0]['free']
    results[0]['rate'] = get_percent(results[0]['total'], results[0]['used'])
    results[0]['stat'] = get_status(results[0]['rate'])

    return results

# YQB-OPN-DIS3-SW1# show interface brief
# --------------------------------------------------------------------------------
# Port   VRF          Status IP Address                              Speed    MTU
# --------------------------------------------------------------------------------
# mgmt0  --           up     11.170.226.1                            1000     1500
#
# --------------------------------------------------------------------------------
# Ethernet      VLAN    Type Mode   Status  Reason                   Speed     Port
# Interface                                                                    Ch #
# --------------------------------------------------------------------------------
# Eth1/1        --      eth  routed down    Link not connected         auto(D) 31
# Eth1/2        --      eth  routed down    Link not connected         auto(D) 32
# Eth1/3        1       eth  trunk  up      none                        10G(D) 71
# Eth1/4        --      eth  routed up      none                        10G(D) 36
# Eth1/5        --      eth  routed up      none                        10G(D) 35
# Eth1/6        1       eth  trunk  up      none                        10G(D) 53
# Eth1/7        1       eth  trunk  up      none                        10G(D) 101
# Eth1/8        1       eth  trunk  up      none                        10G(D) 121
# Eth1/9        1       eth  trunk  up      none                        10G(D) 102
# Eth1/10       1       eth  trunk  up      none                        10G(D) 121
# Eth1/11       1       eth  trunk  up      none                        10G(D) 103
# Eth1/12       --      eth  routed down    Link not connected         auto(D) --
# Eth1/13       1       eth  trunk  up      none                        10G(D) 104
# Eth1/14       --      eth  routed down    Link not connected         auto(D) --
# Eth1/15       1       eth  trunk  up      none                        10G(D) 105
# Eth1/16       --      eth  routed down    SFP not inserted           auto(D) --
# Eth1/17       1       eth  trunk  up      none                        10G(D) 106
# Eth1/18       --      eth  routed down    Link not connected         auto(D) --
# Eth1/19       1       eth  trunk  up      none                        10G(D) 107
# Eth1/20       --      eth  routed down    Link not connected         auto(D) --
# Eth1/21       1       eth  trunk  up      none                        10G(D) 108
# Eth1/22       --      eth  routed down    Link not connected         auto(D) --
# Eth1/23       1       eth  trunk  up      none                        10G(D) 109
# Eth1/24       --      eth  routed down    Link not connected         auto(D) --
# Eth1/25       1       eth  trunk  up      none                        10G(D) 110
# Eth1/26       --      eth  routed down    Link not connected         auto(D) --
# Eth1/27       1       eth  trunk  up      none                        10G(D) 110
# Eth1/28       --      eth  routed down    Link not connected         auto(D) --
# Eth1/29       1       eth  trunk  up      none                        10G(D) 111
# Eth1/30       --      eth  routed down    Link not connected         auto(D) --
# Eth1/31       1       eth  trunk  up      none                        10G(D) 111
# Eth1/32       --      eth  routed down    Link not connected         auto(D) --
# Eth1/33       1       eth  trunk  up      none                        10G(D) 112
# Eth1/34       --      eth  routed down    Link not connected         auto(D) --
# Eth1/35       1       eth  trunk  up      none                        10G(D) 126
# Eth1/36       1       eth  trunk  down    Administratively down      auto(D) --
# Eth1/37       1       eth  trunk  up      none                        10G(D) 125
# Eth1/38       1       eth  trunk  down    Administratively down      auto(D) --
# Eth1/39       1       eth  trunk  up      none                        10G(D) 127
# Eth1/40       1       eth  trunk  up      none                        10G(D) 127
# Eth1/41       1       eth  trunk  up      none                        10G(D) 126
# Eth1/42       1       eth  trunk  up      none                        10G(D) 125
# Eth1/43       731     eth  access up      none                        10G(D) 731
# Eth1/44       731     eth  access up      none                        10G(D) 730
# Eth1/45       1       eth  trunk  up      none                        10G(D) 200
# Eth1/46       --      eth  routed down    SFP not inserted           auto(D) --
# Eth1/47       1       eth  trunk  up      none                        10G(D) 100
# Eth1/48       --      eth  routed up      none                        10G(D) --
# Eth2/1        --      eth  routed down    Link not connected         auto(D) 31
# Eth2/2        --      eth  routed down    Link not connected         auto(D) 32
# Eth2/3        1       eth  trunk  up      none                        10G(D) 72
# Eth2/4        --      eth  routed up      none                        10G(D) 36
# Eth2/5        --      eth  routed up      none                        10G(D) 35
# Eth2/6        1       eth  trunk  up      none                        10G(D) 54
# Eth2/7        1       eth  trunk  up      none                        10G(D) 101
# Eth2/8        1       eth  trunk  up      none                        10G(D) 121
# Eth2/9        1       eth  trunk  up      none                        10G(D) 102
# Eth2/10       1       eth  trunk  up      none                        10G(D) 121
# Eth2/11       1       eth  trunk  up      none                        10G(D) 103
# Eth2/12       --      eth  routed down    Link not connected         auto(D) --
# Eth2/13       1       eth  trunk  up      none                        10G(D) 104
# Eth2/14       --      eth  routed down    Link not connected         auto(D) --
# Eth2/15       1       eth  trunk  up      none                        10G(D) 105
# Eth2/16       --      eth  routed down    Link not connected         auto(D) --
# Eth2/17       1       eth  trunk  up      none                        10G(D) 106
# Eth2/18       --      eth  routed down    SFP not inserted           auto(D) --
# Eth2/19       1       eth  trunk  up      none                        10G(D) 107
# Eth2/20       --      eth  routed down    Link not connected         auto(D) --
# Eth2/21       1       eth  trunk  up      none                        10G(D) 108
# Eth2/22       --      eth  routed down    Link not connected         auto(D) --
# Eth2/23       1       eth  trunk  up      none                        10G(D) 109
# Eth2/24       --      eth  routed down    Link not connected         auto(D) --
# Eth2/25       1       eth  trunk  up      none                        10G(D) 110
# Eth2/26       --      eth  routed down    Link not connected         auto(D) --
# Eth2/27       1       eth  trunk  up      none                        10G(D) 110
# Eth2/28       --      eth  routed down    Link not connected         auto(D) --
# Eth2/29       1       eth  trunk  up      none                        10G(D) 111
# Eth2/30       --      eth  routed down    Link not connected         auto(D) --
# Eth2/31       1       eth  trunk  up      none                        10G(D) 111
# Eth2/32       --      eth  routed down    Link not connected         auto(D) --
# Eth2/33       1       eth  trunk  up      none                        10G(D) 112
# Eth2/34       --      eth  routed down    Link not connected         auto(D) --
# Eth2/35       1       eth  trunk  up      none                        10G(D) 126
# Eth2/36       1       eth  trunk  down    Administratively down      auto(D) --
# Eth2/37       1       eth  trunk  up      none                        10G(D) 125
# Eth2/38       1       eth  trunk  down    Administratively down      auto(D) --
# Eth2/39       1       eth  trunk  up      none                        10G(D) 127
# Eth2/40       1       eth  trunk  up      none                        10G(D) 127
# Eth2/41       1       eth  trunk  up      none                        10G(D) 126
# Eth2/42       1       eth  trunk  up      none                        10G(D) 125
# Eth2/43       731     eth  access up      none                        10G(D) 731
# Eth2/44       731     eth  access up      none                        10G(D) 730
# Eth2/45       1       eth  trunk  up      none                        10G(D) 200
# Eth2/46       1       eth  trunk  down    Administratively down      auto(D) --
# Eth2/47       1       eth  trunk  up      none                        10G(D) 100
# Eth2/48       --      eth  routed down    Link not connected         auto(D) --
# Eth3/1        1       eth  trunk  up      none                        10G(D) 115
# Eth3/2        1       eth  trunk  up      none                        10G(D) --
# Eth3/3        1       eth  trunk  up      none                        10G(D) 116
# Eth3/4        --      eth  routed down    Link not connected         auto(D) --
# Eth3/5        1       eth  trunk  up      none                        10G(D) 117
# Eth3/6        --      eth  routed down    Link not connected         auto(D) --
# Eth3/7        1       eth  trunk  up      none                        10G(D) 115
# Eth3/8        --      eth  routed down    Link not connected         auto(D) --
# Eth3/9        1       eth  trunk  up      none                        10G(D) 116
# Eth3/10       --      eth  routed down    Link not connected         auto(D) --
# Eth3/11       1       eth  trunk  up      none                        10G(D) 117
# Eth3/12       --      eth  routed down    Link not connected         auto(D) --
# Eth3/13       --      eth  routed down    Link not connected         auto(D) 81
# Eth3/14       --      eth  routed down    Link not connected         auto(D) 81
# Eth3/15       1       eth  trunk  up      none                        10G(D) 118
# Eth3/16       1       eth  trunk  up      none                        10G(D) 118
# Eth3/17       1       eth  trunk  up      none                        10G(D) 119
# Eth3/18       1       eth  trunk  up      none                        10G(D) 119
# Eth3/19       1       eth  trunk  up      none                        10G(D) 120
# Eth3/20       1       eth  trunk  up      none                        10G(D) 120
# Eth3/21       1       eth  trunk  up      none                        10G(D) 128
# Eth3/22       1       eth  trunk  up      none                        10G(D) 128
# Eth3/23       1       eth  trunk  up      none                        10G(D) 129
# Eth3/24       1       eth  trunk  up      none                        10G(D) 129
# Eth3/25       1       eth  trunk  up      none                        10G(D) 75
# Eth3/26       --      eth  routed down    Link not connected         auto(D) --
# Eth3/27       1       eth  trunk  up      none                        10G(D) 77
# Eth3/28       --      eth  routed down    Link not connected         auto(D) --
# Eth3/29       1       eth  trunk  up      none                        10G(D) 73
# Eth3/30       1       eth  trunk  up      none                        10G(D) --
# Eth3/31       731     eth  access up      none                        10G(D) 732
# Eth3/32       731     eth  access up      none                        10G(D) 732
# Eth3/33       1       eth  trunk  up      none                        10G(D) 79
# Eth3/34       --      eth  routed down    Link not connected         auto(D) --
# Eth3/35       731     eth  access up      none                        10G(D) 733
# Eth3/36       731     eth  access up      none                        10G(D) 733
# Eth3/37       --      eth  routed down    Link not connected         auto(D) --
# Eth3/38       --      eth  routed down    Link not connected         auto(D) --
# Eth3/39       40      eth  access down    Link not connected         auto(D) --
# Eth3/40       --      eth  routed down    Link not connected         auto(D) --
# Eth3/41       731     eth  access up      none                        10G(D) 736
# Eth3/42       731     eth  access up      none                        10G(D) 737
# Eth3/43       --      eth  routed down    Link not connected         auto(D) --
# Eth3/44       731     eth  access up      none                        10G(D) 734
# Eth3/45       --      eth  routed down    Link not connected         auto(D) --
# Eth3/46       731     eth  access up      none                        10G(D) 735
# Eth3/47       1       eth  trunk  up      none                       1000(D) 299
# Eth3/48       1       eth  trunk  up      none                       1000(D) 299
# Eth4/1        --      eth  routed down    Link not connected         auto(D) --
# Eth4/2        1       eth  trunk  up      none                        10G(D) 115
# Eth4/3        --      eth  routed down    Link not connected         auto(D) --
# Eth4/4        1       eth  trunk  up      none                        10G(D) 116
# Eth4/5        --      eth  routed up      none                        10G(D) 35
# Eth4/6        1       eth  trunk  up      none                        10G(D) 117
# Eth4/7        --      eth  routed down    Link not connected         auto(D) --
# Eth4/8        1       eth  trunk  up      none                        10G(D) 115
# Eth4/9        --      eth  routed down    Link not connected         auto(D) --
# Eth4/10       1       eth  trunk  up      none                        10G(D) 116
# Eth4/11       --      eth  routed down    Link not connected         auto(D) --
# Eth4/12       1       eth  trunk  up      none                        10G(D) 117
# Eth4/13       --      eth  routed down    Link not connected         auto(D) 81
# Eth4/14       --      eth  routed down    Link not connected         auto(D) 81
# Eth4/15       1       eth  trunk  up      none                        10G(D) 118
# Eth4/16       1       eth  trunk  up      none                        10G(D) 118
# Eth4/17       1       eth  trunk  up      none                        10G(D) 119
# Eth4/18       1       eth  trunk  up      none                        10G(D) 119
# Eth4/19       1       eth  trunk  up      none                        10G(D) 120
# Eth4/20       1       eth  trunk  up      none                        10G(D) 120
# Eth4/21       1       eth  trunk  up      none                        10G(D) 128
# Eth4/22       1       eth  trunk  up      none                        10G(D) 128
# Eth4/23       1       eth  trunk  down    Administratively down      auto(D) 129
# Eth4/24       1       eth  trunk  down    Administratively down      auto(D) 129
# Eth4/25       --      eth  routed down    Administratively down      auto(D) --
# Eth4/26       1       eth  trunk  up      none                        10G(D) 76
# Eth4/27       --      eth  routed down    Link not connected         auto(D) --
# Eth4/28       1       eth  trunk  up      none                        10G(D) 78
# Eth4/29       --      eth  routed down    SFP not inserted           auto(D) --
# Eth4/30       1       eth  trunk  up      none                        10G(D) 74
# Eth4/31       --      eth  routed down    Link not connected         auto(D) --
# Eth4/32       --      eth  routed down    Link not connected         auto(D) --
# Eth4/33       --      eth  routed down    Link not connected         auto(D) --
# Eth4/34       1       eth  trunk  down    Link not connected         auto(D) 80
# Eth4/35       --      eth  routed down    Link not connected         auto(D) --
# Eth4/36       --      eth  routed down    Link not connected         auto(D) --
# Eth4/37       --      eth  routed down    Link not connected         auto(D) --
# Eth4/38       --      eth  routed down    Link not connected         auto(D) --
# Eth4/39       --      eth  routed down    Link not connected         auto(D) --
# Eth4/40       --      eth  routed down    Link not connected         auto(D) --
# Eth4/41       731     eth  access up      none                        10G(D) 736
# Eth4/42       731     eth  access up      none                        10G(D) 737
# Eth4/43       --      eth  routed down    Link not connected         auto(D) --
# Eth4/44       --      eth  routed down    Link not connected         auto(D) --
# Eth4/45       1       eth  trunk  down    Link not connected         auto(D) 297
# Eth4/46       1       eth  trunk  down    Link not connected         auto(D) 297
# Eth4/47       --      eth  routed up      none                        10G(D) 90
# Eth4/48       1       eth  trunk  down    Link not connected         auto(D) 298
# Eth7/1        --      eth  routed up      none                        10G(D) 35
# Eth7/2        --      eth  routed down    Link not connected         auto(D) --
# Eth7/3        --      eth  routed down    Link not connected         auto(D) --
# Eth7/4        --      eth  routed up      none                        10G(D) 36
# Eth7/5        1       eth  trunk  up      none                        10G(D) 121
# Eth7/6        1       eth  trunk  up      none                        10G(D) 121
# Eth7/7        --      eth  routed down    Link not connected         auto(D) --
# Eth7/8        1       eth  trunk  up      none                        10G(D) 101
# Eth7/9        --      eth  routed down    Link not connected         auto(D) --
# Eth7/10       1       eth  trunk  up      none                        10G(D) 102
# Eth7/11       --      eth  routed down    Link not connected         auto(D) --
# Eth7/12       1       eth  trunk  up      none                        10G(D) 103
# Eth7/13       --      eth  routed down    Link not connected         auto(D) --
# Eth7/14       1       eth  trunk  up      none                        10G(D) 104
# Eth7/15       --      eth  routed down    Link not connected         auto(D) --
# Eth7/16       1       eth  trunk  down    Link not connected         auto(D) 105
# Eth7/17       --      eth  routed down    Link not connected         auto(D) --
# Eth7/18       1       eth  trunk  up      none                        10G(D) 106
# Eth7/19       --      eth  routed down    Link not connected         auto(D) --
# Eth7/20       1       eth  trunk  up      none                        10G(D) 107
# Eth7/21       --      eth  routed down    Link not connected         auto(D) --
# Eth7/22       1       eth  trunk  up      none                        10G(D) 108
# Eth7/23       --      eth  routed down    Link not connected         auto(D) --
# Eth7/24       1       eth  trunk  up      none                        10G(D) 109
# Eth7/25       --      eth  routed down    Link not connected         auto(D) --
# Eth7/26       1       eth  trunk  up      none                        10G(D) 110
# Eth7/27       --      eth  routed down    Link not connected         auto(D) --
# Eth7/28       1       eth  trunk  up      none                        10G(D) 110
# Eth7/29       --      eth  routed down    Link not connected         auto(D) --
# Eth7/30       1       eth  trunk  up      none                        10G(D) 111
# Eth7/31       --      eth  routed down    Link not connected         auto(D) --
# Eth7/32       1       eth  trunk  up      none                        10G(D) 111
# Eth7/33       --      eth  routed down    Link not connected         auto(D) --
# Eth7/34       1       eth  trunk  up      none                        10G(D) 112
# Eth7/35       --      eth  routed down    Link not connected         auto(D) 83
# Eth7/36       --      eth  routed down    Link not connected         auto(D) 83
# Eth7/37       731     eth  access up      none                        10G(D) 738
# Eth7/38       731     eth  access up      none                        10G(D) 738
# Eth7/39       1       eth  trunk  up      none                        10G(D) 122
# Eth7/40       1       eth  trunk  up      none                        10G(D) 122
# Eth7/41       1       eth  trunk  up      none                        10G(D) 123
# Eth7/42       1       eth  trunk  up      none                        10G(D) 123
# Eth7/43       1       eth  trunk  up      none                        10G(D) 124
# Eth7/44       1       eth  trunk  up      none                        10G(D) 124
# Eth7/45       1       eth  trunk  up      none                       1000(D) 299
# Eth7/46       --      eth  routed down    Link not connected         auto(D) --
# Eth7/47       --      eth  routed down    Link not connected         auto(D) --
# Eth7/48       monitor eth  access down    Link not connected         auto(D) --
# Eth8/1        --      eth  routed up      none                        10G(D) 36
# Eth8/2        --      eth  routed down    Link not connected         auto(D) --
# Eth8/3        --      eth  routed down    Link not connected         auto(D) --
# Eth8/4        --      eth  routed down    Link not connected         auto(D) --
# Eth8/5        1       eth  trunk  up      none                        10G(D) 121
# Eth8/6        1       eth  trunk  up      none                        10G(D) 121
# Eth8/7        --      eth  routed down    Link not connected         auto(D) --
# Eth8/8        1       eth  trunk  up      none                        10G(D) 101
# Eth8/9        --      eth  routed down    Link not connected         auto(D) --
# Eth8/10       1       eth  trunk  up      none                        10G(D) 102
# Eth8/11       --      eth  routed down    Link not connected         auto(D) --
# Eth8/12       1       eth  trunk  up      none                        10G(D) 103
# Eth8/13       --      eth  routed down    Link not connected         auto(D) --
# Eth8/14       1       eth  trunk  up      none                        10G(D) 104
# Eth8/15       --      eth  routed down    Link not connected         auto(D) --
# Eth8/16       1       eth  trunk  down    Link not connected         auto(D) 105
# Eth8/17       --      eth  routed down    Link not connected         auto(D) --
# Eth8/18       1       eth  trunk  up      none                        10G(D) 106
# Eth8/19       --      eth  routed down    Link not connected         auto(D) --
# Eth8/20       1       eth  trunk  up      none                        10G(D) 107
# Eth8/21       --      eth  routed down    Link not connected         auto(D) --
# Eth8/22       1       eth  trunk  up      none                        10G(D) 108
# Eth8/23       --      eth  routed down    Link not connected         auto(D) --
# Eth8/24       1       eth  trunk  up      none                        10G(D) 109
# Eth8/25       --      eth  routed down    Link not connected         auto(D) --
# Eth8/26       1       eth  trunk  up      none                        10G(D) 110
# Eth8/27       --      eth  routed down    Link not connected         auto(D) --
# Eth8/28       1       eth  trunk  up      none                        10G(D) 110
# Eth8/29       --      eth  routed down    Link not connected         auto(D) --
# Eth8/30       1       eth  trunk  up      none                        10G(D) 111
# Eth8/31       --      eth  routed down    Link not connected         auto(D) --
# Eth8/32       1       eth  trunk  up      none                        10G(D) 111
# Eth8/33       --      eth  routed down    Link not connected         auto(D) --
# Eth8/34       1       eth  trunk  up      none                        10G(D) 112
# Eth8/35       --      eth  routed down    Link not connected         auto(D) 84
# Eth8/36       --      eth  routed down    Link not connected         auto(D) 84
# Eth8/37       731     eth  access up      none                        10G(D) 739
# Eth8/38       731     eth  access up      none                        10G(D) 739
# Eth8/39       1       eth  trunk  up      none                        10G(D) 122
# Eth8/40       1       eth  trunk  up      none                        10G(D) 122
# Eth8/41       1       eth  trunk  up      none                        10G(D) 123
# Eth8/42       1       eth  trunk  up      none                        10G(D) 123
# Eth8/43       1       eth  trunk  up      none                        10G(D) 124
# Eth8/44       1       eth  trunk  up      none                        10G(D) 124
# Eth8/45       --      eth  routed down    Link not connected         auto(D) --
# Eth8/46       --      eth  routed down    Link not connected         auto(D) --
# Eth8/47       --      eth  routed up      none                        10G(D) 90
# Eth8/48       1       eth  trunk  up      none                        10G(D) 296
#
# --------------------------------------------------------------------------------
# Port-channel VLAN    Type Mode   Status  Reason                    Speed   Protocol
# Interface
# --------------------------------------------------------------------------------
# Po31         --      eth  routed down    No operational members      auto(D)  lacp
# Po32         --      eth  routed down    No operational members      auto(D)  lacp
# Po35         --      eth  routed up      none                       a-10G(D)  lacp
# Po36         --      eth  routed up      none                       a-10G(D)  lacp
# Po53         1       eth  trunk  up      none                       a-10G(D)  lacp
# Po54         1       eth  trunk  up      none                       a-10G(D)  lacp
# Po71         1       eth  trunk  up      none                       a-10G(D)  lacp
# Po72         1       eth  trunk  up      none                       a-10G(D)  lacp
# Po73         1       eth  trunk  up      none                       a-10G(D)  lacp
# Po74         1       eth  trunk  up      none                       a-10G(D)  lacp
# Po75         1       eth  trunk  up      none                       a-10G(D)  lacp
# Po76         1       eth  trunk  up      none                       a-10G(D)  lacp
# Po77         1       eth  trunk  up      none                       a-10G(D)  lacp
# Po78         1       eth  trunk  up      none                       a-10G(D)  lacp
# Po79         1       eth  trunk  up      none                       a-10G(D)  lacp
# Po80         1       eth  trunk  down    No operational members      auto(D)  lacp
# Po81         --      eth  routed down    No operational members      auto(D)  lacp
# Po83         --      eth  routed down    No operational members      auto(D)  lacp
# Po84         --      eth  routed down    No operational members      auto(D)  lacp
# Po90         --      eth  routed up      none                       a-10G(D)  lacp
# Po100        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po101        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po102        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po103        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po104        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po105        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po106        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po107        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po108        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po109        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po110        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po111        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po112        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po113        1       eth  trunk  down    No operational members      auto(I)  lacp
# Po114        1       eth  trunk  down    No operational members      auto(I)  lacp
# Po115        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po116        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po117        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po118        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po119        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po120        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po121        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po122        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po123        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po124        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po125        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po126        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po127        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po128        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po129        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po200        1       eth  trunk  up      none                       a-10G(D)  lacp
# Po296        1       eth  trunk  up      none                       a-10G(D)  none
# Po297        monitor eth  trunk  down    No operational members      auto(D)  none
# Po298        monitor eth  trunk  down    No operational members      auto(D)  none
# Po299        1       eth  trunk  up      none                      a-1000(D)  none
# Po730        731     eth  access up      none                       a-10G(D)  lacp
# Po731        731     eth  access up      none                       a-10G(D)  lacp
# Po732        731     eth  access up      none                       a-10G(D)  lacp
# Po733        731     eth  access up      none                       a-10G(D)  lacp
# Po734        731     eth  access up      none                       a-10G(D)  lacp
# Po735        731     eth  access up      none                       a-10G(D)  lacp
# Po736        731     eth  access up      none                       a-10G(D)  lacp
# Po737        731     eth  access up      none                       a-10G(D)  lacp
# Po738        731     eth  access up      none                       a-10G(D)  lacp
# Po739        731     eth  access up      none                       a-10G(D)  lacp
#
# --------------------------------------------------------------------------------
# Interface     Status     Description
# --------------------------------------------------------------------------------
# Lo0           up         Globle_Router-ID
# Lo1           up         OOB_Router-ID
#
# -------------------------------------------------------------------------------
# Interface Secondary VLAN(Type)                    Status Reason
# -------------------------------------------------------------------------------
# Vlan1     --                                      down   Administratively down
# Vlan20    --                                      up     --
# Vlan21    --                                      up     --
# Vlan22    --                                      up     --
# Vlan23    --                                      up     --
# Vlan24    --                                      up     --
# Vlan25    --                                      up     --
# Vlan26    --                                      up     --
# Vlan27    --                                      up     --
# Vlan28    --                                      up     --
# Vlan29    --                                      up     --
# Vlan31    --                                      up     --
# Vlan32    --                                      up     --
# Vlan33    --                                      up     --
# Vlan34    --                                      up     --
# Vlan35    --                                      up     --
# Vlan36    --                                      up     --
# Vlan40    --                                      down   Administratively down
# Vlan500   --                                      up     --
# Vlan501   --                                      up     --
# Vlan502   --                                      up     --
# Vlan503   --                                      up     --
# Vlan504   --                                      up     --
# Vlan505   --                                      up     --
# Vlan506   --                                      up     --
# Vlan507   --                                      up     --
# Vlan508   --                                      up     --
# Vlan509   --                                      up     --
# Vlan510   --                                      up     --
# Vlan511   --                                      up     --
# Vlan512   --                                      up     --
# Vlan513   --                                      up     --
# Vlan514   --                                      up     --
# Vlan515   --                                      up     --
# Vlan516   --                                      up     --
# Vlan532   --                                      up     --
# Vlan533   --                                      up     --
# Vlan534   --                                      up     --
# Vlan535   --                                      up     --
# Vlan536   --                                      up     --
# Vlan537   --                                      up     --
# Vlan538   --                                      up     --
# Vlan539   --                                      up     --
# Vlan540   --                                      up     --
# Vlan541   --                                      up     --
# Vlan542   --                                      up     --
# Vlan543   --                                      up     --
# Vlan544   --                                      up     --
# Vlan545   --                                      up     --
# Vlan546   --                                      up     --
# Vlan547   --                                      up     --
# Vlan548   --                                      up     --
# Vlan550   --                                      up     --
# Vlan551   --                                      up     --
# Vlan552   --                                      up     --
# Vlan553   --                                      up     --
# Vlan555   --                                      up     --
# Vlan560   --                                      up     --
# Vlan561   --                                      up     --
# Vlan562   --                                      up     --
# Vlan563   --                                      up     --
# Vlan564   --                                      up     --
# Vlan565   --                                      up     --
# Vlan566   --                                      up     --
# Vlan567   --                                      up     --
# Vlan568   --                                      up     --
# Vlan569   --                                      up     --
# Vlan570   --                                      up     --
# Vlan571   --                                      up     --
# Vlan572   --                                      up     --
# Vlan573   --                                      up     --
# Vlan574   --                                      up     --
# Vlan575   --                                      up     --
# Vlan576   --                                      up     --
# Vlan577   --                                      up     --
# Vlan578   --                                      up     --
# Vlan579   --                                      up     --
# Vlan582   --                                      up     --
# Vlan583   --                                      up     --
# Vlan592   --                                      up     --
# Vlan593   --                                      up     --
# Vlan594   --                                      up     --
# Vlan595   --                                      up     --
# Vlan596   --                                      up     --
# Vlan597   --                                      up     --
# Vlan598   --                                      up     --
# Vlan599   --                                      up     --
# Vlan600   --                                      up     --
# Vlan601   --                                      up     --
# Vlan602   --                                      up     --
# Vlan603   --                                      up     --
# Vlan604   --                                      up     --
# Vlan605   --                                      up     --
# Vlan606   --                                      up     --
# Vlan607   --                                      up     --
# Vlan608   --                                      up     --
# Vlan609   --                                      up     --
# Vlan610   --                                      up     --
# Vlan611   --                                      up     --
# Vlan614   --                                      up     --
# Vlan615   --                                      up     --
# Vlan624   --                                      up     --
# Vlan625   --                                      up     --
# Vlan626   --                                      up     --
# Vlan627   --                                      up     --
# Vlan628   --                                      up     --
# Vlan631   --                                      up     --
# Vlan634   --                                      up     --
# Vlan637   --                                      up     --
# Vlan640   --                                      up     --
# Vlan643   --                                      up     --
# Vlan646   --                                      up     --
# Vlan648   --                                      up     --
# Vlan649   --                                      up     --
# Vlan650   --                                      up     --
# Vlan651   --                                      up     --
# Vlan660   --                                      up     --
# Vlan661   --                                      up     --
# Vlan662   --                                      up     --
# Vlan663   --                                      up     --
# Vlan664   --                                      up     --
# Vlan665   --                                      up     --
# Vlan666   --                                      up     --
# Vlan667   --                                      up     --
# Vlan668   --                                      up     --
# Vlan669   --                                      up     --
# Vlan670   --                                      up     --
# Vlan671   --                                      up     --
# Vlan672   --                                      up     --
# Vlan673   --                                      up     --
# Vlan674   --                                      up     --
# Vlan675   --                                      up     --
# Vlan726   --                                      up     --
# Vlan729   --                                      up     --
# Vlan731   --                                      up     --
# Vlan1100  --                                      up     --
# Vlan1101  --                                      up     --
# Vlan1102  --                                      up     --
# Vlan1103  --                                      up     --
# Vlan1104  --                                      up     --
# Vlan1105  --                                      up     --
# Vlan1106  --                                      up     --
# Vlan1107  --                                      up     --
# Vlan1108  --                                      up     --
# Vlan1109  --                                      up     --
# Vlan1110  --                                      up     --
# Vlan1111  --                                      up     --
# Vlan1112  --                                      up     --
# Vlan1113  --                                      up     --
# Vlan1114  --                                      up     --
# Vlan1115  --                                      up     --
# Vlan1116  --                                      up     --
# Vlan1132  --                                      up     --
# Vlan1133  --                                      up     --
# Vlan1134  --                                      up     --
# Vlan1135  --                                      up     --
# Vlan1136  --                                      up     --
# Vlan1137  --                                      up     --
# Vlan1138  --                                      up     --
# Vlan1139  --                                      up     --
# Vlan1140  --                                      up     --
# Vlan1141  --                                      up     --
# Vlan1142  --                                      up     --
# Vlan1143  --                                      up     --
# Vlan1144  --                                      up     --
# Vlan1145  --                                      up     --
# Vlan1146  --                                      up     --
# Vlan1147  --                                      up     --
# Vlan1148  --                                      up     --
# Vlan1152  --                                      up     --
# Vlan1153  --                                      up     --
# Vlan1155  --                                      up     --
# Vlan1160  --                                      up     --
# Vlan1161  --                                      up     --
# Vlan1162  --                                      up     --
# Vlan1163  --                                      up     --
# Vlan1164  --                                      up     --
# Vlan1165  --                                      up     --
# Vlan1166  --                                      up     --
# Vlan1167  --                                      up     --
# Vlan1168  --                                      up     --
# Vlan1169  --                                      up     --
# Vlan1170  --                                      up     --
# Vlan1171  --                                      up     --
# Vlan1172  --                                      up     --
# Vlan1173  --                                      up     --
# Vlan1174  --                                      up     --
# Vlan1175  --                                      up     --
# Vlan1176  --                                      up     --
# Vlan1177  --                                      up     --
# Vlan1178  --                                      up     --
# Vlan1179  --                                      up     --
# Vlan1192  --                                      up     --
# Vlan1193  --                                      up     --
# Vlan1194  --                                      up     --
# Vlan1195  --                                      up     --
# Vlan1196  --                                      up     --
# Vlan1197  --                                      up     --
# Vlan1198  --                                      up     --
# Vlan1199  --                                      up     --
# Vlan1200  --                                      up     --
# Vlan1201  --                                      up     --
# Vlan1202  --                                      up     --
# Vlan1203  --                                      up     --
# Vlan1204  --                                      up     --
# Vlan1205  --                                      up     --
# Vlan1206  --                                      up     --
# Vlan1207  --                                      up     --
# Vlan1208  --                                      up     --
# Vlan1209  --                                      up     --
# Vlan1210  --                                      up     --
# Vlan1211  --                                      up     --
# Vlan1224  --                                      up     --
# Vlan1225  --                                      up     --
# Vlan1226  --                                      up     --
# Vlan1227  --                                      up     --
# Vlan1228  --                                      up     --
# Vlan1229  --                                      up     --
# Vlan1230  --                                      up     --
# Vlan1231  --                                      up     --
# Vlan1232  --                                      up     --
# Vlan1233  --                                      up     --
# Vlan1234  --                                      up     --
# Vlan1235  --                                      up     --
# Vlan1236  --                                      up     --
# Vlan1237  --                                      up     --
# Vlan1238  --                                      up     --
# Vlan1239  --                                      up     --
# Vlan1240  --                                      up     --
# Vlan1241  --                                      up     --
# Vlan1242  --                                      up     --
# Vlan1243  --                                      up     --
# Vlan1244  --                                      up     --
# Vlan1245  --                                      up     --
# Vlan1246  --                                      up     --
# Vlan1248  --                                      up     --
# Vlan1249  --                                      up     --
# Vlan1250  --                                      up     --
# Vlan1251  --                                      up     --
# Vlan1260  --                                      up     --
# Vlan1261  --                                      up     --
# Vlan1262  --                                      up     --
# Vlan1263  --                                      up     --
# Vlan1264  --                                      up     --
# Vlan1265  --                                      up     --
# Vlan1266  --                                      up     --
# Vlan1267  --                                      up     --
# Vlan1268  --                                      up     --
# Vlan1269  --                                      up     --
# Vlan1270  --                                      up     --
# Vlan1271  --                                      up     --
# Vlan1272  --                                      up     --
# Vlan1273  --                                      up     --
# Vlan1274  --                                      up     --
# Vlan1275  --                                      up     --
# Vlan1291  --                                      up     --
# Vlan1331  --                                      up     --
# Vlan1332  --                                      up     --
