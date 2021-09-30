#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

configs_file_path = './configs.json'                # configs.json 配置文件 -> 路径
gui_config_file_path = ''                           # gui-config.json 配置文件 -> 路径
ssr_gui_config_file_path = ''                       # shadowsocksR gui-config.json 配置文件 -> 路径
# 获取配置信息
with open(configs_file_path, 'r', encoding='utf8') as f:
    configs = json.load(f)
    gui_config_file_path = configs['gui_config_file_path']
    ssr_gui_config_file_path = configs['ssr_gui_config_file_path']
    print('gui-config.json 源文件路径：', gui_config_file_path)
    print('gui-config.json 目标文件路径：', ssr_gui_config_file_path)

with open(gui_config_file_path, 'r', encoding='utf8') as f:
    json_config = json.load(f)

with open(ssr_gui_config_file_path, 'w', encoding='utf8') as f:
    json.dump(json_config, f, indent=2, ensure_ascii=True)

