#!/usr/bin/env python3
"""TrollStore Chinese localization - run inside GitHub Actions runner"""
import glob, sys
sys.stdout.reconfigure(encoding='utf-8')

rules = {
    "TrollStore/TSRootViewController.m": {
        "Apps": "\u5e94\u7528",
        "Settings": "\u8bbe\u7f6e",
    },
    "TrollStore/TSSettingsListController.m": {
        "Update Available": "\u6709\u66f4\u65b0\u53ef\u7528",
        "Enable Developer Mode": "\u542f\u7528\u5f00\u53d1\u8005\u6a21\u5f0f",
        "Developer Mode": "\u5f00\u53d1\u8005\u6a21\u5f0f",
        "Respring": "\u6ce8\u9500\u684c\u9762",
        "Refresh App Registrations": "\u5237\u65b0\u5e94\u7528\u6ce8\u518c",
        "Rebuild Icon Cache": "\u91cd\u5efa\u56fe\u6807\u7f13\u5b58",
        "Install ldid": "\u5b89\u88c8ldid",
        "ldid: Installed": "ldid: \u5df2\u5b89\u88c5",
        "Install Persistence Helper": "\u5b89\u88c5\u6301\u4e45\u5316\u52a9\u624b",
        "Uninstall Persistence Helper": "\u5378\u8f7d\u6301\u4e45\u5316\u52a9\u624b",
        "Uninstall TrollStore": "\u5378\u8f7d\u5de8\u9b54\u5546\u5e97",
        "Select App": "\u9009\u62e9\u5e94\u7528",
        "Cancel": "\u53d6\u6d88",
        "Transfer Apps": "\u8f6c\u79fb\u5e94\u7528",
        "Transfering": "\u6b63\u5728\u8f6c\u79fb",
        "Transfer Failed": "\u8f6c\u79fb\u5931\u8d25",
        "Close": "\u5173\u95ed",
        "Reboot Now": "\u7acb\u5373\u91cd\u542f",
        "Reboot Required": "\u9700\u8981\u91cd\u542f",
        "Reboot Later": "\u7a0d\u540e\u91cd\u542f",
        "Rebuild Now": "\u7acb\u5373\u91cd\u5efa",
        "Donate": "\u6350\u8d60",
        "Security": "\u5b89\u5168",
        "Utilities": "\u5de5\u5177",
        "Persistence": "\u6301\u4e45\u5316",
        "Signing": "\u7b7e\u540d",
        "Advanced": "\u9ad8\u7ea7",
        "Show Install Confirmation Alert": "\u663e\u793a\u5b89\u88c5\u786e\u8ba4\u63d0\u793a",
        "Do the Dash": "\u6267\u884cDash",
        "Copy Debug Log": "\u590d\u5236\u8c03\u8bd5\u65e5\u5fd7",
        "Helper Installed as Standalone App": "\u52a9\u624b\u5df2\u5b89\u88c5",
        "URL Scheme Enabled": "URL\u65b9\u6848\u5df2\u542f\u7528",
        "Failed to enable developer mode.": "\u542f\u7528\u5f00\u53d1\u8005\u6a21\u5f0f\u5931\u8d25\u3002",
    },
    "TrollStore/TSAppTableViewController.m": {
        "Install IPA File": "\u5b89\u88c5IPA\u6587\u4ef6",
        "Install from URL": "\u4eceURL\u5b89\u88c5",
        "Open with JIT": "\u7528JIT\u6253\u5f00",
        "Show Details": "\u663e\u793a\u8be6\u60c5",
        "Uninstall App": "\u5378\u8f7d\u5e94\u7528",
        "Confirm Uninstallation": "\u786e\u8ba4\u5378\u8f7d",
        "Error": "\u9519\u8bef",
        "User": "\u7528\u6237",
        "System": "\u7cfb\u7edf",
    },
    "TrollStore/TSInstallationController.m": {
        "Installing": "\u6b63\u5728\u5b89\u88c5",
        "Downloading": "\u6b63\u5728\u4e0b\u8f7d",
        "Force Installation": "\u5f3a\u5236\u5b89\u88c5",
        "Warning": "\u8b66\u544a",
        "Installing ldid": "\u6b63\u5728\u5b89\u88c5ldid",
    },
    "TrollHelper/TSHRootViewController.m": {
        "Install TrollStore": "\u5b89\u88c5\u5de8\u9b54\u5546\u5e97",
        "Not Installed": "\u672a\u5b89\u88c5",
        "Uninstall TrollStore": "\u5378\u8f7d\u5de8\u9b54\u5546\u5e97",
        "Uninstall Persistence Helper": "\u5378\u8f7d\u6301\u4e45\u5316\u52a9\u624b",
        "Register Persistence Helper": "\u6ce8\u518c\u6301\u4e45\u5316\u52a9\u624b",
        "Unregister Persistence Helper": "\u53d6\u6d88\u6ce8\u518c\u6301\u4e45\u5316\u52a9\u624b",
        "TrollStore Helper": "\u5de8\u9b54\u5546\u5e97\u52a9\u624b",
    },
    "Shared/TSListControllerShared.m": {
        "Installing TrollStore": "\u6b63\u5728\u5b89\u88c5\u5de8\u9b54\u5546\u5e97",
        "Updating TrollStore": "\u6b63\u5728\u66f4\u65b0\u5de8\u9b54\u5546\u5e97",
    },
}

# Also fix download URL
import urllib.request
old_url = 'https://github.com/opa334/TrollStore/releases/latest/download/TrollStore.tar'
new_url = 'https://modelscope.cn/datasets/a27270401/ph/resolve/master/TrollStore.tar'

for fname, subs in rules.items():
    if not glob.glob(fname):
        print(f"SKIP {fname}")
        continue
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    for en, cn in subs.items():
        needle = '@"' + en + '"'
        replacement = '@"' + cn + '"'
        if needle in content:
            content = content.replace(needle, replacement)
            print(f"  {fname}: {en} -> {cn}")
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)

# Fix download URL
if glob.glob('Shared/TSListControllerShared.m'):
    with open('Shared/TSListControllerShared.m', 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace(old_url, new_url)
    with open('Shared/TSListControllerShared.m', 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"  URL: {old_url} -> {new_url}")

# Fixe Installed with format
if glob.glob('TrollHelper/TSHRootViewController.m'):
    with open('TrollHelper/TSHRootViewController.m', 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('@"Installed, %@"', '@"\u5df2\u5b89\u88c5\uff0c%@"')
    with open('TrollHelper/TSHRootViewController.m', 'w', encoding='utf-8') as f:
        f.write(c)
    print("  Fixed Installed format string")

# Fix Error downloading
if glob.glob('Shared/TSListControllerShared.m'):
    with open('Shared/TSListControllerShared.m', 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('@"Error downloading TrollStore: %@"', '@"\u4e0b\u8f7d\u5de8\u9b54\u5546\u5e97\u5931\u8d25\uff1a%@"')
    with open('Shared/TSListControllerShared.m', 'w', encoding='utf-8') as f:
        f.write(c)
    print("  Fixed Error downloading string")

# Handle the word "Install" and "Open" carefully - only at specific locations in TSAppTableViewController
# These are too generic to blanket-replace

print("Done!")
