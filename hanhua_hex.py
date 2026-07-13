#!/usr/bin/env python3
"""Pure ASCII Chinese localization - constructs UTF-8 from hex bytes"""
import glob, sys, os

def cn(hexstr):
    """Convert hex string to UTF-8 Chinese characters"""
    return bytes.fromhex(hexstr).decode('utf-8')

rules = {
    "TrollStore/TSRootViewController.m": {
        "Apps": cn("e5ba94e794a8"),
        "Settings": cn("e8aebee7bdae"),
    },
    "TrollStore/TSSettingsListController.m": {
        "Respring": cn("e6b3a8e99480e6a18ce99da2"),
        "Cancel": cn("e58f96e6b688"),
        "Close": cn("e585b3e997ad"),
        "Reboot Now": cn("e7ab8be58db3e9878de590af"),
        "Reboot Required": cn("e99c80e8a681e9878de590af"),
        "Security": cn("e5ae89e585a8"),
        "Utilities": cn("e5b7a5e585b7"),
        "Persistence": cn("e68c81e4b985e58c96"),
        "Signing": cn("e7adbee5908d"),
        "Advanced": cn("e9ab98e7baa7"),
        "Donate": cn("e68d90e8b5a0"),
        "Developer Mode": cn("e5bc80e58f91e88085e6a8a1e5bc8f"),
        "Update Available": cn("e69c89e69bb4e696b0e58fafe794a8"),
        "Refresh App Registrations": cn("e588b7e696b0e5ba94e794a8e6b3a8e5868c"),
        "Rebuild Icon Cache": cn("e9878de5bbbae59bbee6a087e7bc93e5ad98"),
        "Install Persistence Helper": cn("e5ae89e8a385e68c81e4b985e58c96e58aa9e6898b"),
        "Uninstall Persistence Helper": cn("e58db8e8bdbde68c81e4b985e58c96e58aa9e6898b"),
        "Uninstall TrollStore": cn("e58db8e8bdbde5b7a8e9ad94e59586e5ba97"),
    },
    "TrollStore/TSAppTableViewController.m": {
        "Install": cn("e5ae89e8a385"),
        "Open": cn("e68993e5bc80"),
        "Uninstall": cn("e58db8e8bdbd"),
        "User": cn("e794a8e688b7"),
        "System": cn("e7b3bbe7bb9f"),
        "Error": cn("e99499e8afaf"),
        "Cancel": cn("e58f96e6b688"),
        "Close": cn("e585b3e997ad"),
        "Respring": cn("e6b3a8e99480e6a18ce99da2"),
        "Install IPA File": cn("e5ae89e8a385495041e69687e4bbb6"),
        "Install from URL": cn("e4bb8e55524ce5ae89e8a385"),
        "Open with JIT": cn("e794a84a4954e68993e5bc80"),
        "Show Details": cn("e698bee7a4bae8afa6e68385"),
        "Uninstall App": cn("e58db8e8bdbde5ba94e794a8"),
        "Confirm Uninstallation": cn("e7a1aee8aea4e58db8e8bdbd"),
    },
    "TrollStore/TSInstallationController.m": {
        "Installing": cn("e6ada3e59ca8e5ae89e8a385"),
        "Downloading": cn("e6ada3e59ca8e4b88be8bdbd"),
        "Warning": cn("e8ada6e5918a"),
        "Force Installation": cn("e5bcbae588b6e5ae89e8a385"),
        "Installing ldid": cn("e6ada3e59ca8e5ae89e8a3856c646964"),
    },
    "TrollHelper/TSHRootViewController.m": {
        "Install TrollStore": cn("e5ae89e8a385e5b7a8e9ad94e59586e5ba97"),
        "Uninstall TrollStore": cn("e58db8e8bdbde5b7a8e9ad94e59586e5ba97"),
        "Not Installed": cn("e69caae5ae89e8a385"),
        "TrollStore Helper": cn("e5b7a8e9ad94e59586e5ba97e58aa9e6898b"),
        "Register Persistence Helper": cn("e6b3a8e5868ce68c81e4b985e58c96e58aa9e6898b"),
        "Unregister Persistence Helper": cn("e58f96e6b688e6b3a8e5868ce68c81e4b985e58c96e58aa9e6898b"),
    },
    "Shared/TSListControllerShared.m": {
        "Installing TrollStore": cn("e6ada3e59ca8e5ae89e8a385e5b7a8e9ad94e59586e5ba97"),
        "Updating TrollStore": cn("e6ada3e59ca8e69bb4e696b0e5b7a8e9ad94e59586e5ba97"),
    },
}

ok = 0
total = 0
for fname, subs in rules.items():
    for fn in glob.glob(fname):
        with open(fn, 'r', encoding='utf-8') as fh:
            content = fh.read()
        for en, cn_text in subs.items():
            total += 1
            old = '@"' + en + '"'
            new = '@"' + cn_text + '"'
            if old in content:
                content = content.replace(old, new)
                ok += 1
                print('  OK  ' + fn + ': ' + en)
        with open(fn, 'w', encoding='utf-8') as fh:
            fh.write(content)

# Handle Installed, %@ format string
for fn in glob.glob('TrollHelper/TSHRootViewController.m'):
    with open(fn, 'r', encoding='utf-8') as fh:
        c = fh.read()
    old = '@"Installed, %@"'
    new = '@"' + cn("e5b7b2e5ae89e8a385efbc8c") + '%@"'
    if old in c:
        c = c.replace(old, new)
        ok += 1; total += 1
        print('  OK  ' + fn + ': Installed,%@')
        with open(fn, 'w', encoding='utf-8') as fh:
            fh.write(c)

# Handle Error downloading format string
for fn in glob.glob('Shared/TSListControllerShared.m'):
    with open(fn, 'r', encoding='utf-8') as fh:
        c = fh.read()
    old = '@"Error downloading TrollStore: %@"'
    new = '@"' + cn("e4b88be8bdbde5b7a8e9ad94e59586e5ba97e5a4b1e8b4a5efbc9a") + '%@"'
    if old in c:
        c = c.replace(old, new)
        ok += 1; total += 1
        print('  OK  ' + fn + ': Error downloading')
        with open(fn, 'w', encoding='utf-8') as fh:
            fh.write(c)

# Fix download URL
for fn in glob.glob('Shared/TSListControllerShared.m'):
    with open(fn, 'r', encoding='utf-8') as fh:
        c = fh.read()
    old_url = 'https://github.com/opa334/TrollStore/releases/latest/download/TrollStore.tar'
    new_url = 'https://modelscope.cn/datasets/a27270401/ph/resolve/master/TrollStore.tar'
    if old_url in c:
        c = c.replace(old_url, new_url)
        with open(fn, 'w', encoding='utf-8') as fh:
            fh.write(c)
        ok += 1; total += 1
        print('  OK  URL replaced')

print('=== Matched: %d/%d ===' % (ok, total))
