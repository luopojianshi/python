#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import base64
import requests
from bs4 import BeautifulSoup


configs_file_path = './configs.json'                # configs.json 配置文件 -> 路径
url = ''                                            # configs.json 配置文件 -> 免费账号网页链接
encryption_list = []                                # configs.json 配置文件 -> 加密方式列表
gui_config_file_path = ''                           # gui-config.json 配置文件 -> 路径
server_config_list = []                             # 网页中服务器配置标签列表
gui_configs = []                                    # 服务器配置列表 gui-config.json->configs
# 获取配置信息
with open(configs_file_path, 'r', encoding='utf8') as f:
    configs = json.load(f)
    url = configs['url']
    gui_config_file_path = configs['gui_config_file_path']
    encryption_list = configs['encryption_list']
    print('gui-config.json 文件路径:')
    print(gui_config_file_path)
    print('支持的加密方式列表:')
    print(encryption_list)
    print('-------- 分割线 --------')

# 抓取网页内容
def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0(Macintosh; Intel Mac OS X 10_11_4)\
        AppleWebkit/537.36(KHTML, like Gecko) Chrome/52 .0.2743. 116 Safari/537.36'
    }                                               # 模拟浏览器访问
    response = requests.get(url, headers=headers)   # 请求访问的网页链接
    html = response.text                            # 获取网页源码
    return html                                     # 返回网页源码

soup = BeautifulSoup(get_html(url), 'lxml')         # 初始化 BeautifulSoup 库，并设置解析器


for tbody in soup.find_all(name='tbody'):
    for tr in tbody.find_all(name='tr'):
        if(len(tr.find_all(name='td')) == 0):
            continue
        server_config_list.append([])
        for td in tr.find_all(name='td'):
            if td.string:
                server_config_list[-1].append(td.string)
            else:
                server_config_list[-1].append('')

# server_config_list 配置
# remarks、server、server_port、password、method、protocol、obfs
# 备注、服务器IP、服务器端口、密码、加密方式、协议、混淆
for config in server_config_list:
    if config[4] in encryption_list:
        gui_configs.append({
            "remarks": config[0],
            "server": config[1],
            "server_port": int(config[2]),
            "password": " ".join(config[3].split()),
            "method": config[4].lower(),
            "protocol": config[5],
            "obfs": config[6],
            "enable": True,
            "remarks_base64": base64.b64encode(config[0].encode('utf-8')).decode('utf-8')
        })

with open(gui_config_file_path, 'r', encoding='utf8') as f:
    json_config = json.load(f)
    json_config['configs'] = gui_configs

with open(gui_config_file_path, 'w', encoding='utf8') as f:
    json.dump(json_config, f, indent=2, ensure_ascii=True)

