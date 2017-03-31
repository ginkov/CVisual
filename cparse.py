# -*- coding: utf-8
import copy
import importlib
import re


def do_parse(model, raw_content):

    # cc: capacity contents, predefined in parsers/<model>/__init__.py
    cc = copy.deepcopy(importlib.import_module("parsers."+model).cc)

    sections = dict()   # 保存不同 show 命令的输出结果
    section = []        # 某个具体 show 命令的结果
    key = ''

    # 这个 pattern 分隔不同 show/dir 命令的结果
    pattern = re.compile('(\S+)(\(\S+\))?#\s+(sh|show|dir)\s+(.*)', re.M | re.I)

    #
    # 把不同 show 命令的结果分开
    #
    for line in raw_content:
        s = line.strip()
        if not s:
            continue

        pm = pattern.match(s)
        if pm:
            if section:
                sections[key.upper()] = section
            section = []

            cmd = pm.group(3)
            if cmd.startswith('sh'):
                cmd = 'show'
            key = cmd + ' ' + pm.group(4)  # key 是具体的 show 命令, 如 show ip interface brief
        else:
            section.append(s)

    sections[key.upper()] = section

    #
    # 根据不同的 show 命令, 即 k, 调用不同的解析器
    #
    parser_lookup = importlib.import_module("parsers."+model).parser_lookup
    unknow_commands = []

    for k in sections.keys():

        results = []

        # show vdc [具体 vdc 名字] resource -- 这种含有用户定义名称的命令, 需要特殊处理
        # TODO: 这里是个麻烦, 今天不可扩展
        m_line = re.match(r'show\s+vdc\s+(\S+)\s+res', k, re.M | re.I)

        if m_line:
            vdc_name = m_line.group(1)
            parser = importlib.import_module('parsers.' + model + '.' + 'show_vdc_vdcname_resource')
            results = parser.parse(sections[k], vdc_name)

        else:
            if k in parser_lookup:
                parser = importlib.import_module("parsers." + model + "." + parser_lookup[k])
                results = parser.parse(sections[k])
            else:
                if k:
                    unknow_commands.append(k.lower())

        if results:
            for r in results:
                cc[r['grp']]['ci_list'].append(r)

    return [cc, unknow_commands]
