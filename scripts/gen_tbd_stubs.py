#!/usr/bin/env python3
"""Generate stub .tbd files for missing private frameworks"""
import os, sys

sdk_path = sys.argv[1] if len(sys.argv) > 1 else os.popen('xcrun --sdk iphoneos --show-sdk-path').read().strip()
priv_fw = os.path.join(sdk_path, 'System/Library/PrivateFrameworks')

frameworks = ['Preferences','MobileContainerManager','SpringBoardServices','BackBoardServices','FrontBoardServices','RunningBoardServices']

for fw in frameworks:
    fw_dir = os.path.join(priv_fw, fw + '.framework')
    if os.path.isdir(fw_dir):
        print(f'SKIP: {fw} already exists')
        continue
    
    os.makedirs(fw_dir, exist_ok=True)
    
    tbd = f'''--- !tapi-tbd
tbd-version:     4
targets:         [ arm64, arm64e ]
uuids:
  - target:          arm64
    value:           00000000-0000-0000-0000-000000000000
  - target:          arm64e
    value:           00000000-0000-0000-0000-000000000000
flags:           [ flat_namespace, not_app_extension_safe ]
install-name:    '/System/Library/PrivateFrameworks/{fw}.framework/{fw}'
current-version: 1
compatibility-version: 1
exports:
  - archs:           [ arm64, arm64e ]
    symbols:         [ _fake_symbol_for_linking ]
'''
    
    tbd_path = os.path.join(fw_dir, fw + '.tbd')
    with open(tbd_path, 'w') as f:
        f.write(tbd)
    
    bin_path = os.path.join(fw_dir, fw)
    open(bin_path, 'a').close()
    
    print(f'CREATED: {fw}.framework ({fw}.tbd + stub)')
