#!/usr/bin/env python3
"""Chinese localization for TrollStore sources"""

subs = [
    ("TrollStore/TSRootViewController.m", [
        ("Apps", "应用"),
        ("Settings", "设置"),
    ]),
    ("TrollStore/TSAppTableViewController.m", [
        ("Install", "安装"),
        ("Uninstall", "卸载"),
        ("User", "用户"),
        ("System", "系统"),
        ("Error", "错误"),
    ]),
    ("TrollStore/TSInstallationController.m", [
        ("Warning", "警告"),
    ]),
    ("TrollStore/TSSettingsListController.m", [
        ("Security", "安全"),
        ("Advanced", "高级"),
    ]),
    ("TrollHelper/TSHRootViewController.m", [
        ("Install TrollStore", "安装巨魔商店"),
        ("Uninstall TrollStore", "卸载巨魔商店"),
        ("TrollStore Helper", "巨魔商店助手"),
        ("Not Installed", "未安装"),
    ]),
    ("Shared/TSListControllerShared.m", [
        ("Installing TrollStore", "正在安装巨魔商店"),
        ("Updating TrollStore", "正在更新巨魔商店"),
    ]),
]

import sys
for fname, reps in subs:
    print(f"Processing {fname}...")
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read()
    for en, cn in reps:
        old = '@"' + en + '"'
        new = '@"' + cn + '"'
        count = content.count(old)
        content = content.replace(old, new)
        print(f"  '{en}' -> '{cn}': {count} matches")
    with open(fname, "w", encoding="utf-8") as f:
        f.write(content)

# Fix update URL
fname = "Shared/TSListControllerShared.m"
with open(fname, "r", encoding="utf-8") as f:
    c = f.read()
old_url = "https://github.com/opa334/TrollStore/releases/latest/download/TrollStore.tar"
new_url = "https://modelscope.cn/datasets/a27270401/ph/resolve/master/TrollStore.tar"
count = c.count(old_url)
c = c.replace(old_url, new_url)
with open(fname, "w", encoding="utf-8") as f:
    f.write(c)
print(f"URL replace: {count} matches")
print("Localization done!")
