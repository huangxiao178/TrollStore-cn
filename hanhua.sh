#!/bin/bash
set -e
cd $GITHUB_WORKSPACE/trollstore
echo "=== HanHua in $(pwd) ==="
ls TrollStore/TSRootViewController.m && echo "source files exist"

# TSRootViewController
sed -i '' 's|@"Apps"|@"应用"|g' TrollStore/TSRootViewController.m
sed -i '' 's|@"Settings"|@"设置"|g' TrollStore/TSRootViewController.m

# TSSettingsListController
sed -i '' 's|@"Respring"|@"注销桌面"|g' TrollStore/TSSettingsListController.m
sed -i '' 's|@"Cancel"|@"取消"|g' TrollStore/TSSettingsListController.m
sed -i '' 's|@"Close"|@"关闭"|g' TrollStore/TSSettingsListController.m
sed -i '' 's|@"Reboot Now"|@"立即重启"|g' TrollStore/TSSettingsListController.m
sed -i '' 's|@"Reboot Required"|@"需要重启"|g' TrollStore/TSSettingsListController.m
sed -i '' 's|@"Security"|@"安全"|g' TrollStore/TSSettingsListController.m
sed -i '' 's|@"Utilities"|@"工具"|g' TrollStore/TSSettingsListController.m
sed -i '' 's|@"Persistence"|@"持久化"|g' TrollStore/TSSettingsListController.m
sed -i '' 's|@"Signing"|@"签名"|g' TrollStore/TSSettingsListController.m
sed -i '' 's|@"Advanced"|@"高级"|g' TrollStore/TSSettingsListController.m
sed -i '' 's|@"Donate"|@"捐赠"|g' TrollStore/TSSettingsListController.m
sed -i '' 's|@"Developer Mode"|@"开发者模式"|g' TrollStore/TSSettingsListController.m
sed -i '' 's|@"Update Available"|@"有更新可用"|g' TrollStore/TSSettingsListController.m
sed -i '' 's|@"Refresh App Registrations"|@"刷新应用注册"|g' TrollStore/TSSettingsListController.m
sed -i '' 's|@"Rebuild Icon Cache"|@"重建图标缓存"|g' TrollStore/TSSettingsListController.m
sed -i '' 's|@"Install Persistence Helper"|@"安装持久化助手"|g' TrollStore/TSSettingsListController.m
sed -i '' 's|@"Uninstall Persistence Helper"|@"卸载持久化助手"|g' TrollStore/TSSettingsListController.m
sed -i '' 's|@"Uninstall TrollStore"|@"卸载巨魔商店"|g' TrollStore/TSSettingsListController.m

# TSAppTableViewController
sed -i '' 's|@"Install"|@"安装"|g' TrollStore/TSAppTableViewController.m
sed -i '' 's|@"Open"|@"打开"|g' TrollStore/TSAppTableViewController.m
sed -i '' 's|@"Uninstall"|@"卸载"|g' TrollStore/TSAppTableViewController.m
sed -i '' 's|@"User"|@"用户"|g' TrollStore/TSAppTableViewController.m
sed -i '' 's|@"System"|@"系统"|g' TrollStore/TSAppTableViewController.m
sed -i '' 's|@"Error"|@"错误"|g' TrollStore/TSAppTableViewController.m
sed -i '' 's|@"Cancel"|@"取消"|g' TrollStore/TSAppTableViewController.m
sed -i '' 's|@"Close"|@"关闭"|g' TrollStore/TSAppTableViewController.m
sed -i '' 's|@"Respring"|@"注销桌面"|g' TrollStore/TSAppTableViewController.m
sed -i '' 's|@"Install IPA File"|@"安装IPA文件"|g' TrollStore/TSAppTableViewController.m
sed -i '' 's|@"Install from URL"|@"从URL安装"|g' TrollStore/TSAppTableViewController.m
sed -i '' 's|@"Open with JIT"|@"用JIT打开"|g' TrollStore/TSAppTableViewController.m
sed -i '' 's|@"Show Details"|@"显示详情"|g' TrollStore/TSAppTableViewController.m
sed -i '' 's|@"Uninstall App"|@"卸载应用"|g' TrollStore/TSAppTableViewController.m
sed -i '' 's|@"Confirm Uninstallation"|@"确认卸载"|g' TrollStore/TSAppTableViewController.m

# TSInstallationController
sed -i '' 's|@"Installing"|@"正在安装"|g' TrollStore/TSInstallationController.m
sed -i '' 's|@"Downloading"|@"正在下载"|g' TrollStore/TSInstallationController.m
sed -i '' 's|@"Warning"|@"警告"|g' TrollStore/TSInstallationController.m
sed -i '' 's|@"Force Installation"|@"强制安装"|g' TrollStore/TSInstallationController.m
sed -i '' 's|@"Installing ldid"|@"正在安装ldid"|g' TrollStore/TSInstallationController.m

# TrollHelper
sed -i '' 's|@"Install TrollStore"|@"安装巨魔商店"|g' TrollHelper/TSHRootViewController.m
sed -i '' 's|@"Uninstall TrollStore"|@"卸载巨魔商店"|g' TrollHelper/TSHRootViewController.m
sed -i '' 's|@"Not Installed"|@"未安装"|g' TrollHelper/TSHRootViewController.m
sed -i '' 's|@"TrollStore Helper"|@"巨魔商店助手"|g' TrollHelper/TSHRootViewController.m
sed -i '' 's|@"Register Persistence Helper"|@"注册持久化助手"|g' TrollHelper/TSHRootViewController.m
sed -i '' 's|@"Unregister Persistence Helper"|@"取消注册持久化助手"|g' TrollHelper/TSHRootViewController.m
sed -i '' 's|@"Installed, %@"|@"已安装，%@"|g' TrollHelper/TSHRootViewController.m

# Shared
sed -i '' 's|@"Installing TrollStore"|@"正在安装巨魔商店"|g' Shared/TSListControllerShared.m
sed -i '' 's|@"Updating TrollStore"|@"正在更新巨魔商店"|g' Shared/TSListControllerShared.m
sed -i '' 's|https://github.com/opa334/TrollStore/releases/latest/download/TrollStore.tar|https://modelscope.cn/datasets/a27270401/ph/resolve/master/TrollStore.tar|g' Shared/TSListControllerShared.m

echo "=== HanHua Done ==="
