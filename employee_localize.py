#!/usr/bin/env python3
"""Apply the employee-build UI translations before compiling the complete tar.

This script intentionally performs only literal UI substitutions.  It does
not inject network or remote-control code; the license gate is implemented in
the checked-in Objective-C sources separately.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parent

REPLACEMENTS = {
    "TrollStore/TSAppTableViewController.m": {
        "Install IPA File": "安装 IPA 文件",
        "Install from URL": "从网址安装",
        "Install": "安装",
        "Cancel": "取消",
        "Open": "打开",
        "Open with JIT": "使用 JIT 打开",
        "Show Details": "查看详情",
        "Close": "关闭",
        "Uninstall App": "卸载应用",
        "Uninstall": "卸载",
        "Error": "错误",
        "Confirm Uninstallation": "确认卸载",
        "Switch to \\\"User\\\"": "切换为“用户”",
        "Switch to \\\"System\\\"": "切换为“系统”",
        "Respring": "注销桌面",
    },
    "TrollStore/TSInstallationController.m": {
        "Close": "关闭",
        "Force Installation": "强制安装",
        "Reboot Now": "立即重启",
        "Copy Debug Log": "复制调试日志",
        "Install": "安装",
        "Cancel": "取消",
        "Installing": "正在安装",
    },
    "TrollStore/TSSettingsListController.m": {
        "Update Available": "有可用更新",
        "Developer Mode": "开发者模式",
        "Enable Developer Mode": "启用开发者模式",
        "Utilities": "工具",
        "Signing": "签名",
        "Persistence": "持久化",
        "Refresh App Registrations": "刷新应用注册",
        "Rebuild Icon Cache": "重建图标缓存",
        "Helper Installed as Standalone App": "助手已作为独立应用安装",
        "Uninstall Persistence Helper": "卸载持久化助手",
        "Install Persistence Helper": "安装持久化助手",
        "Security": "安全",
        "URL Scheme Enabled": "启用网址协议",
        "Show Install Confirmation Alert": "显示安装确认提示",
        "Advanced": "高级",
        "Donate": "捐赠",
        "Uninstall TrollStore": "卸载巨魔商店",
        "Close": "关闭",
        "Cancel": "取消",
        "Transfer": "转移",
        "Copy Debug Log": "复制调试日志",
        "Rebuild Now": "立即重建",
        "Rebuild Later": "稍后重建",
        "Reboot Required": "需要重启",
        "Reboot Now": "立即重启",
        "Select App": "选择应用",
    },
    "TrollStore/TSSettingsAdvancedListController.m": {
        "Installation Method": "安装方式",
        "Installation Method Segment": "安装方式",
        "Uninstallation Method": "卸载方式",
        "Uninstallation Method Segment": "卸载方式",
    },
}


def main() -> None:
    changed = 0
    for relative, mapping in REPLACEMENTS.items():
        path = ROOT / relative
        text = path.read_text(encoding="utf-8")
        before = text
        for old, new in mapping.items():
            text = text.replace(f'"{old}"', f'"{new}"')
        if text != before:
            path.write_text(text, encoding="utf-8")
            changed += 1
    print(f"employee localization updated {changed} files")


if __name__ == "__main__":
    main()
