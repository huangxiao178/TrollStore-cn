#!/bin/bash
set -e
# Chinese localization for TrollStore source files
sed -i '' 's|@"Apps"|@"应用"|g' TrollStore/TSRootViewController.m
sed -i '' 's|@"Settings"|@"设置"|g' TrollStore/TSRootViewController.m
sed -i '' 's|@"Install"|@"安装"|g' TrollStore/TSAppTableViewController.m
sed -i '' 's|@"Uninstall"|@"卸载"|g' TrollStore/TSAppTableViewController.m
sed -i '' 's|@"User"|@"用户"|g' TrollStore/TSAppTableViewController.m
sed -i '' 's|@"System"|@"系统"|g' TrollStore/TSAppTableViewController.m
sed -i '' 's|@"Error"|@"错误"|g' TrollStore/TSAppTableViewController.m
sed -i '' 's|@"Warning"|@"警告"|g' TrollStore/TSInstallationController.m
sed -i '' 's|@"Security"|@"安全"|g' TrollStore/TSSettingsListController.m
sed -i '' 's|@"Advanced"|@"高级"|g' TrollStore/TSSettingsListController.m
sed -i '' 's|@"Install TrollStore"|@"安装巨魔商店"|g' TrollHelper/TSHRootViewController.m
sed -i '' 's|@"Uninstall TrollStore"|@"卸载巨魔商店"|g' TrollHelper/TSHRootViewController.m
sed -i '' 's|@"TrollStore Helper"|@"巨魔商店助手"|g' TrollHelper/TSHRootViewController.m
sed -i '' 's|@"Not Installed"|@"未安装"|g' TrollHelper/TSHRootViewController.m
sed -i '' 's|@"Installing TrollStore"|@"正在安装巨魔商店"|g' Shared/TSListControllerShared.m
sed -i '' 's|@"Updating TrollStore"|@"正在更新巨魔商店"|g' Shared/TSListControllerShared.m
sed -i '' 's|https://github.com/opa334/TrollStore/releases/latest/download/TrollStore.tar|https://modelscope.cn/datasets/a27270401/ph/resolve/master/TrollStore.tar|g' Shared/TSListControllerShared.m
echo "=== HanHua Done ==="
