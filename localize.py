#!/usr/bin/env python3
"""Full Chinese localization for TrollStore - all stdout goes to stderr for logging"""
import sys

SUBS = [
    ("TrollStore/TSRootViewController.m", [("Apps","应用"),("Settings","设置")]),
    ("TrollStore/TSAppTableViewController.m", [
        ("Install","安装"),("Uninstall","卸载"),("User","用户"),("System","系统"),("Error","错误"),
        ("Install IPA File","安装 IPA 文件"),("Install from URL","从 URL 安装"),
        ("Parse Error %ld","解析错误 %ld"),
        ("Error enabling JIT: trollstorehelper returned %d","启用 JIT 错误: trollstorehelper 返回 %d"),
        ("Confirm Uninstallation","确认卸载"),("Uninstall App","卸载应用"),("Cancel","取消"),
        ("Uninstalling the app '%@' will delete the app and all data associated to it.","卸载 '%@' 将删除此应用及所有相关数据。"),
    ]),
    ("TrollStore/TSInstallationController.m", [
        ("Warning","警告"),("Installing","安装中"),("Install Error %d","安装错误 %d"),
        ("Force Installation","强制安装"),("Installing ldid","正在安装 ldid"),
        ("Error downloading app: %@","下载应用失败: %@"),("Error downloading ldid: %@","下载 ldid 失败: %@"),
    ]),
    ("TrollStore/TSSettingsListController.m", [
        ("Security","安全"),("Advanced","高级"),("UTILITIES","工具"),("SIGNING","签名"),("PERSISTENCE","持久化"),
        ("Respring","注销"),("Refresh App Registrations","刷新应用注册"),("Rebuild Icon Cache","重建图标缓存"),
        ("Install Persistence Helper","安装持久助手"),("Uninstall Persistence Helper","卸载持久助手"),
        ("Install ldid","安装 ldid"),("ldid: Installed","ldid: 已安装"),
        ("ldid is installed and allows TrollStore to install unsigned IPA files.","ldid 已安装，允许巨魔商店安装未签名 IPA 文件。"),
        ("If an app does not immediately appear after installation, respring here and it should appear afterwards.","如果应用安装后未立即出现，请在此注销，之后应该会出现。"),
        ("In order for TrollStore to be able to install unsigned IPAs, ldid has to be installed using this button. It can't be directly included in TrollStore because of licensing issues.","要安装未签名 IPA，需通过此按钮安装 ldid。因许可证问题，ldid 无法直接内置在巨魔商店中。"),
        ("When iOS rebuilds the icon cache, all TrollStore apps including TrollStore itself will be reverted to \"User\" state and either disappear or no longer launch.","当 iOS 重建图标缓存时，所有巨魔商店应用将恢复为\"用户\"状态，可能消失或无法启动。"),
        ("Helper Installed as Standalone App","助手已安装为独立应用"),("Helper Installed into %@","助手已安装到 %@"),
        ("Apps will be registered as User by default since AppSync Unified is installed.","由于已安装 AppSync Unified，应用将默认注册为用户。"),
        ("Apps will be registered as System by default since AppSync Unified is not installed.","由于未安装 AppSync Unified，应用将默认注册为系统应用。"),
        ("Uninstall","卸载"),("Update TrollStore to %@","更新巨魔商店到 %@"),
        ("You are about to uninstall TrollStore, do you want to preserve the apps installed by it?","您即将卸载巨魔商店，是否保留已安装的应用？"),
        ("Uninstall TrollStore, Uninstall Apps","卸载巨魔，卸载应用"),("Uninstall TrollStore, Preserve Apps","卸载巨魔，保留应用"),
        ("Uninstalling the persistence helper will revert this app back to it's original state, you will however no longer be able to persistently refresh the TrollStore app registrations. Continue?","卸载持久助手将使此应用恢复原状，但您将无法再持久刷新巨魔商店应用注册。是否继续？"),
    ]),
    ("TrollHelper/TSHRootViewController.m", [
        ("Install TrollStore","安装巨魔商店"),("Uninstall TrollStore","卸载巨魔商店"),
        ("TrollStore Helper","巨魔商店助手"),("Not Installed","未安装"),
        ("INFO","信息"),("TrollStore","巨魔商店"),
        ("Refresh App Registrations","刷新应用注册"),("Register Persistence Helper","注册持久助手"),
        ("Uninstall Persistence Helper","卸载持久助手"),("Unregister Persistence Helper","取消注册持久助手"),
        ("If you want to use this app as the TrollStore persistence helper, you can register it here.","如果想将此应用设为巨魔商店持久助手，请在此注册。"),
        ("This app is registered as the TrollStore persistence helper and can be used to fix TrollStore app registrations in case they revert back to \"","此应用已注册为巨魔商店持久助手，可在应用注册恢复\"用户\"状态时用于修复。"),
        ("Registered, %@","已注册, %@"),("Installed, %@","已安装, %@"),("Install Persistence Helper","安装持久助手"),
        ("Update TrollStore to %@","更新巨魔商店到 %@"),("Update","更新"),("Install","安装"),
        ("Uninstall","卸载"),("Register","注册"),("Unregister","取消注册"),
        ("Installed (Standalone)","已安装 (独立)"),
        ("registerPersistenceHelperPressed -> %d","注册持久助手 -> %d"),
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
try:
    with open("Shared/TSListControllerShared.m", "r", encoding="utf-8") as f:
        c = f.read()
    c = c.replace("https://github.com/opa334/TrollStore/releases/latest/download/TrollStore.tar",
                  "http://124.223.199.167/TrollStore.tar")
    with open("Shared/TSListControllerShared.m", "w", encoding="utf-8") as f:
        f.write(c)
except:
    pass

print("OK: " + str(total) + " replacements", file=sys.stderr)
