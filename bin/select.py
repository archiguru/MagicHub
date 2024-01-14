#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 导入所需的库
import requests
import re
import subprocess
import platform
import os  # 导入 os 库，用于文件操作
import os.path  # 导入 os.path 库，用于路径设置

# 定义 NodeList.list 文件的 URL
node_list_url = "https://bit.ly/AllNodeList"
# 自定义保存文件的位置量
new_node_list_file = os.path.join(os.path.expanduser("~"), "NewNode.list")
node_list_file = os.path.join(os.path.expanduser("~"), "NodeList.list")
# 在下载文件之前判断是否已存在，如果存在，可以先删除
if os.path.exists(new_node_list_file):
    os.remove(new_node_list_file)
if os.path.exists(node_list_file):
    os.remove(node_list_file)

response = requests.get(node_list_url)
with open(node_list_file, "w") as f:
    f.write(response.text)

# 从 NodeList.list 文件中提取节点信息
nodes = []
with open(node_list_file, "r") as f:
    for line in f:
        # 直接读取一整行，并用逗号分隔符来提取节点的地址
        # 假设每行都是 节点名称 = 节点的协议类型, 节点的服务器地址, 节点的服务器端口 开头的
        # 使用 split() 函数来分割字符串，并获取第三个元素作为地址
        address = line.split(",")[1].strip()
        # 将节点名和地址添加到列表中
        nodes.append((line, address))

# 对每个节点进行 Ping 测试，并记录延迟值
results = []
# 记录测试成功和失败的节点数量
success_count = 0
fail_count = 0
for name, address in nodes:
    # 调用 ping 命令并获取输出
    output = subprocess.check_output(["ping", "-c", "3", address])
    # 根据不同的操作系统，提取平均延迟值
    # 获取操作系统名称
    os_name = platform.system()
    # 如果是 macOS 系统，匹配 round-trip min/avg/max/stddev = ... 的格式
    if os_name == "Darwin":
        match = re.search(
            r"round-trip min/avg/max/stddev = ([\d\.]+)/", output.decode())
    # 如果是 Linux 系统，匹配 rtt min/avg/max/mdev = ... 的格式
    elif os_name == "Linux":
        match = re.search(
            r"rtt min/avg/max/mdev = ([\d\.]+)/", output.decode())
    # 如果是其他系统，暂不支持
    else:
        match = None

    if match:
        # 提取平均延迟值，并转换为浮点数
        latency = float(match.group(1))
        # 如果延迟大于 1200 ms，则视为超时失败
        if latency > 1200:
            fail_count += 1
        else:
            # 将节点名、地址和延迟值添加到结果列表中，并增加成功计数
            results.append((name, address, latency))
            success_count += 1

    else:
        # 忽略不可用节点，并增加失败计数
        fail_count += 1

# 按照延迟值从小到大对结果列表进行排序
results.sort(key=lambda x: x[2])

# 将处理后的节点写入 NewNode.list 文件，并保存到指定位置
with open(new_node_list_file, "w") as f:
    # 添加注释，标出处理的节点数量和测试的结果
    # 使用中文提示和注释内容
    f.write(f"# 这个文件包含了测试后排序的节点列表。\n")
    f.write(f"# 总节点数：{len(nodes)}\n")
    f.write(f"# 测试成功：{success_count}\n")
    f.write(f"# 测试失败：{fail_count}\n")
    for name, address, latency in results:
        # 保持原始的一整行的节点信息
        f.write(name)

# 处理完成之后删除下载的文件，只保留新文件
# 使用 os.remove() 函数来删除文件
os.remove(node_list_file)

# 输出完成提示信息
# 使用中文提示
print("脚本已经完成了节点列表的处理。")
