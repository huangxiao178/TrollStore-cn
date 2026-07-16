#!/usr/bin/env python3
"""Chinese localization for TrollStore sources"""
import sys

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

total_replaced = 0
for fname, reps in subs:
    print(f"[{fname}]", file=sys.stderr)
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read()
    for en, cn in reps:
        old = '@"' + en + '"'
        new = '@"' + cn + '"'
        count = content.count(old)
        content = content.replace(old, new)
        total_replaced += count
        if count:
            print(f"  {en} -> {cn} ({count})", file=sys.stderr)
    with open(fname, "w", encoding="utf-8") as f:
        f.write(content)

# Fix URL
with open("Shared/TSListControllerShared.m", "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace(
    "https://github.com/opa334/TrollStore/releases/latest/download/TrollStore.tar",
    "https://modelscope.cn/datasets/a27270401/ph/resolve/master/TrollStore.tar"
)
with open("Shared/TSListControllerShared.m", "w", encoding="utf-8") as f:
    f.write(c)

print(f"Total replacements: {total_replaced}", file=sys.stderr)

# Verify
with open("TrollStore/TSRootViewController.m", "r", encoding="utf-8") as f:
    test = f.read()
if "应用" in test and "设置" in test:
    print("VERIFY OK: Chinese chars present in file", file=sys.stderr)
else:
    print("VERIFY FAIL: Chinese chars NOT in file!", file=sys.stderr)
