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

for fname, reps in subs:
    try:
        with open(fname, "r", encoding="utf-8") as f:
            content = f.read()
        for en, cn in reps:
            old = '@"' + en + '"'
            new = '@"' + cn + '"'
            count = content.count(old)
            content = content.replace(old, new)
            if count:
                print(f"  {fname}: '{en}' -> '{cn}' ({count} matches)")
            else:
                print(f"  {fname}: '{en}' -> '{cn}' (0 matches, SKIPPED)")
        with open(fname, "w", encoding="utf-8") as f:
            f.write(content)
    except FileNotFoundError:
        print(f"  {fname}: FILE NOT FOUND, trying checkout root...")
        # Try different working directories
        import os
        for root in ['.', '/Users/runner/work/TrollStore-cn/TrollStore-cn']:
            fpath = os.path.join(root, fname)
            if os.path.exists(fpath):
                print(f"  Found at {fpath}")
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                for en, cn in reps:
                    old = '@"' + en + '"'
                    new = '@"' + cn + '"'
                    content = content.replace(old, new)
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(content)
                break

# Fix update URL
try:
    fname = "Shared/TSListControllerShared.m"
    with open(fname, "r", encoding="utf-8") as f:
        c = f.read()
    c = c.replace(
        "https://github.com/opa334/TrollStore/releases/latest/download/TrollStore.tar",
        "https://modelscope.cn/datasets/a27270401/ph/resolve/master/TrollStore.tar"
    )
    with open(fname, "w", encoding="utf-8") as f:
        f.write(c)
    print("Updated download URL")
except:
    pass

print("Localization done!")
