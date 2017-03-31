# -*- coding: utf-8

cc = [
    {
        "name": u"基础架构",
        "items": [
            {
                "name":     u"电源",
                "unit":     "W",
                "id":       "InfPower",
                "icon":     "fa-plug",
                "total":    6000,
                "used":     5000,
                "stat":     "danger",
                "rate": {
                    "used": 82,
                    "free": 18
                }
            },
            {
                "name":     u"Flash1 容量",
                "unit":     "KB",
                "id":       "InfFlash",
                "icon":     "",
                "total":    1000,
                "used":     80,
                "stat":     "normal",
                "rate": {
                    "used": 8,
                    "free": 92
                }
            },
            {
                "name":     u"Flash2 容量",
                "unit":     "KB",
                "id":       "InfFlash2",
                "icon":     "",
                "total":    1000,
                "used":     80,
                "stat":     "normal",
                "rate": {
                    "used": 8,
                    "free": 92
                }
            },
            {
                "name":    u"Flash3 容量",
                "unit":     "KB",
                "id":       "InfFlash3",
                "icon":     "",
                "total":    1000,
                "used":     80,
                "stat":     "normal",
                "rate": {
                    "used": 8,
                    "free": 92
                }
            },
            {
                "name":    u"Flash4 容量",
                "unit":     "KB",
                "id":       "InfFlash3",
                "icon":     "",
                "total":    1000,
                "used":     80,
                "stat":     "normal",
                "rate": {
                    "used": 8,
                    "free": 92
                }
            }
        ]
    },
    {
        "name": u"物理资源",
        "items": [
            {
                "name":     u"端口数",
                "icon":     "fa-plug",
                "id":       "PhyPort",
                "total":    48,
                "used":     32,
                "stat":     "warning",
                "rate": {
                    "used": 75,
                    "free": 25
                }
            }
        ]
    }
]