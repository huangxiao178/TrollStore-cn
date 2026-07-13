#!/usr/bin/env python3
"""TrollStore Chinese localization - uses ONLY ASCII escape sequences"""
import glob, sys, os

# Verify we're in the right directory
if not os.path.isdir('TrollStore'):
    print("ERROR: must run from TrollStore source root")
    sys.exit(1)

rules = {
    "TrollStore/TSRootViewController.m": {
        "Apps": "\u5e94\u7528",
        "Settings": "\u8bbe\u7f6e",
    },
    "TrollStore/TSSettingsListController.m": {
        "Respring": "\u6ce8\u9500\u684c\u9762",
        "Cancel": "\u53d6\u6d88",
        "Close": "\u5173\u95ed",
        "Reboot Now": "\u7acb\u5373\u91cd\u542f",
        "Reboot Required": "\u9700\u8981\u91cd\u542f",
        "Security": "\u5b89\u5168",
        "Utilities": "\u5de5\u5177",
        "Persistence": "\u6301\u4e45\u5316",
        "Signing": "\u7b7e\u540d",
        "Advanced": "\u9ad8\u7ea7",
        "Donate": "\u6350\u8d60",
        "Developer Mode": "\u5f00\u53d1\u8005\u6a21\u5f0f",
        "Update Available": "\u6709\u66f4\u65b0\u53ef\u7528",
        "Refresh App Registrations": "\u5237\u65b0\u5e94\u7528\u6ce8\u518c",
        "Rebuild Icon Cache": "\u91cd\u5efa\u56fe\u6807\u7f13\u5b58",
        "Install Persistence Helper": "\u5b89\u88c5\u6301\u4e45\u5316\u52a9\u624b",
        "Uninstall Persistence Helper": "\u5378\u8f7d\u6301\u4e45\u5316\u52a9\u624b",
        "Uninstall TrollStore": "\u5378\u8f7d\u5de8\u9b54\u5546\u5e97",
    },
    "TrollStore/TSAppTableViewController.m": {
        "Install": "\u5b89\u88c5",
        "Open": "\u6253\u5f00",
        "Uninstall": "\u5378\u8f7d",
        "User": "\u7528\u6237",
        "System": "\u7cfb\u7edf",
        "Error": "\u9519\u8bef",
        "Cancel": "\u53d6\u6d88",
        "Close": "\u5173\u95ed",
        "Respring": "\u6ce8\u9500\u684c\u9762",
        "Install IPA File": "\u5b89\u88c5IPA\u6587\u4ef6",
        "Install from URL": "\u4eceURL\u5b89\u88c5",
        "Open with JIT": "\u7528JIT\u6253\u5f00",
        "Show Details": "\u663e\u793a\u8be6\u60c5",
        "Uninstall App": "\u5378\u8f7d\u5e94\u7528",
        "Confirm Uninstallation": "\u786e\u8ba4\u5378\u8f7d",
    },
    "TrollStore/TSInstallationController.m": {
        "Installing": "\u6b63\u5728\u5b89\u88c5",
        "Downloading": "\u6b63\u5728\u4e0b\u8f7d",
        "Warning": "\u8b66\u544a",
        "Force Installation": "\u5f3a\u5236\u5b89\u88c5",
        "Installing ldid": "\u6b63\u5728\u5b89\u88c5ldid",
    },
    "TrollHelper/TSHRootViewController.m": {
        "Install TrollStore": "\u5b89\u88c5\u5de8\u9b54\u5546\u5e97",
        "Uninstall TrollStore": "\u5378\u8f7d\u5de8\u9b54\u5546\u5e97",
        "Not Installed": "\u672a\u5b89\u88c5",
        "TrollStore Helper": "\u5de8\u9b54\u5546\u5e97\u52a9\u624b",
        "Register Persistence Helper": "\u6ce8\u518c\u6301\u4e45\u5316\u52a9\u624b",
        "Unregister Persistence Helper": "\u53d6\u6d88\u6ce8\u518c\u6301\u4e45\u5316\u52a9\u624b",
    },
    "Shared/TSListControllerShared.m": {
        "Installing TrollStore": "\u6b63\u5728\u5b89\u88c5\u5de8\u9b54\u5546\u5e97",
        "Updating TrollStore": "\u6b63\u5728\u66f4\u65b0\u5de8\u9b54\u5546\u5e97",
    },
}

for fname, subs in rules.items():
    for fn in glob.glob(fname):
        with open(fn, 'r', encoding='utf-8') as fh:
            c = fh.read()
        for en, cn in subs.items():
            old = '@"' + en + '"'
            new = '@"' + cn + '"'
            if old in c:
                c = c.replace(old, new)
                print(f'  {fn}: {en} OK')
            else:
                # Try with %@ format
                old2 = '@"' + en + ', %@"'
                if old2 in c:
                    continue
                print(f'  {fn}: {en} NOT FOUND')
        with open(fn, 'w', encoding='utf-8') as fh:
            fh.write(c)

# Download URL
if glob.glob('Shared/TSListControllerShared.m'):
    with open('Shared/TSListControllerShared.m', 'r', encoding='utf-8') as fh:
        c = fh.read()
    old_u = 'https://github.com/opa334/TrollStore/releases/latest/download/TrollStore.tar'
    new_u = 'https://modelscope.cn/datasets/a27270401/ph/resolve/master/TrollStore.tar'
    if old_u in c:
        c = c.replace(old_u, new_u)
        with open('Shared/TSListControllerShared.m', 'w', encoding='utf-8') as fh:
            fh.write(c)
        print('  URL: OK')

# Installed, %@ -> \u5df2\u5b89\u88c5\uff0c%@
if glob.glob('TrollHelper/TSHRootViewController.m'):
    with open('TrollHelper/TSHRootViewController.m', 'r', encoding='utf-8') as fh:
        c = fh.read()
    old_f = '@"Installed, %@"'
    new_f = '@"\u5df2\u5b89\u88c5\uff0c%@"'
    if old_f in c:
        c = c.replace(old_f, new_f)
        with open('TrollHelper/TSHRootViewController.m', 'w', encoding='utf-8') as fh:
            fh.write(c)
    print('  Installed,%@: OK')

print('=== HanHua Done ===')
