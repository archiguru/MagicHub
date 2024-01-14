#!/usr/bin/env python3
# coding=utf-8
import os
import requests
import subprocess
import re

sync_url = "https://magic.eoysky.com/bin/sync_url.list"
save_dir = "/opt/src/MagicHub/src/sync/"

# 拉取远程分支并强制重置到远程的最新提交
subprocess.call(['git', '-C', '/opt/src/MagicHub', 'fetch', '--all'])
subprocess.call(['git', '-C', '/opt/src/MagicHub', 'reset', '--hard', 'origin/main'])

# 推送强制更新后的分支到远程仓库
subprocess.call(['git', '-C', '/opt/src/MagicHub', 'push', '--force'])


# 获取同步列表和排除列表
sync_response = requests.get(sync_url)
sync_content = sync_response.text
url_list = []
for line in sync_content.split('\n'):
    line = line.strip()
    if line and not line.isspace() and not line.startswith('#'):
        url_list.append(line)

# 下载并保存文件
def download_file(url, save_path):
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

def create_directory(directory):
    # 创建文件夹（如果不存在）
    os.makedirs(directory, exist_ok=True)

# 删除保存目录下的所有内容
if os.path.exists(save_dir):
    for root, dirs, files in os.walk(save_dir, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))


# 下载并保存文件
for line in url_list:
    line = line.strip()
    line = line.strip()
    parts = re.split(r'\s+|,\s*|\s*,\s*', line)

    if len(parts) == 1:
        # 直接下载保存在
        file_url = parts[0]
        file_name = file_url.split("/")[-1]
        save_path = os.path.join(save_dir, file_name)
        download_file(file_url, save_path)
    elif len(parts) == 2:
        # 将文件保存在指定路径下
        directory, file_url = parts
        save_path = os.path.join(save_dir, directory, file_url.split("/")[-1])
        create_directory(os.path.join(save_dir, directory))
        download_file(file_url, save_path)

# 添加所有变更
subprocess.call(['git', '-C', '/opt/src/MagicHub', 'add', '.'])

# 提交变更
subprocess.call(['git', '-C', '/opt/src/MagicHub', 'commit', '-m', 'Auto commit'])

# 推送到远程仓库
subprocess.call(['git', '-C', '/opt/src/MagicHub', 'push', '--force'])
print("done")

