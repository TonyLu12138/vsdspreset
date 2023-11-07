#! /usr/bin/env python3

import argparse
from network_manager import NetworkManager
from system import System
from log_record import Logger
from targetcli import TargetCLIConfig
from versds import VersaSDS

# 禁用系统自动升级


def disable_system_upgrades(system):
    if not system.stop_unattended_upgrades():
        print("程序将继续执行")
    else:
        print("停止无人值守升级成功")
    if not system.disable_unattended_upgrades():
        print("程序将继续执行")
    else:
        print("禁用无人值守升级成功")
    if not system.check_unattended_upgrades():
        print("禁用无人值守升级失败，程序将继续执行")
    if not system.modify_configuration_file_parameters():
        print("程序将继续执行")
    if not system.check_configuration_file():
        print("配置文件参数修改失败，程序将继续执行")


# 禁用 VersaSDS 服务开机自启
def disable_VersaSDS_service_startup(versds):
    note = "程序将继续执行后续部分"

    if not versds.disable_service("drbd"):
        print(f"禁用drbd程序执行失败，{note}")
    else:
        print("禁用drbd程序执行成功")
    if not versds.disable_service("linstor-controller"):
        print(f"禁用linstor-controller程序执行失败，{note}")
    else:
        print("禁用linstor-controller程序执行成功")
    if not versds.disable_service("rtslib-fb-targetctl"):
        print(f"禁用rtslib-fb-targetctl程序执行失败，{note}")
    else:
        print("禁用rtslib-fb-targetctl程序执行成功")
    if not versds.disable_service("linstor-satellite"):
        print(f"禁用linstor-satellite程序执行失败，{note}")
    else:
        print("禁用linstor-satellite程序执行成功")
    if not versds.disable_service("pacemaker"):
        print(f"禁用pacemaker程序执行失败，{note}")
    else:
        print("禁用pacemaker程序执行成功")
    if not versds.disable_service("corosync"):
        print(f"禁用corosync程序执行失败，{note}")
    else:
        print("禁用corosync程序执行成功")

    # 调用通用方法检查不同的服务
    if not versds.is_service_disabled("drbd"):
        print(f"禁用drbd服务失败，{note}")
    if not versds.is_service_disabled("linstor-controller"):
        print(f"禁用linstor-controller服务失败，{note}")
    if not versds.is_service_disabled("rtslib-fb-targetctl"):
        print(f"禁用rtslib-fb-targetctl服务失败，{note}")
    if not versds.is_service_disabled("linstor-satellite"):
        print(f"禁用linstor-satellite服务失败，{note}")
    if not versds.is_service_disabled("pacemaker"):
        print(f"禁用pacemaker服务失败，{note}")
    if not versds.is_service_disabled("corosync"):
        print(f"禁用corosync服务失败，{note}")


# 配置 Network Manager
def setup_network_manager(network_manager):
    if not network_manager.set_network_manager_interfaces():
        print(f"修改NetworkManager.conf失败")
    if not network_manager.restart_network_manager_service():
        print(f"重启NetworkManager服务失败")
    if not network_manager.update_netplan_config():
        print(f"修改01-netcfg.yaml失败")
    if not network_manager.apply_netplan_config():
        print(f"应用 Netplan 配置失败")
    else:
        print("配置网络管理成功")

# 初始化 targetcli 配置


def initialize_targetcli_configuration(targetcli):
    note = "初始化 targetcli 配置失败"
    if not targetcli.configure_targetcli("auto_add_default_portal=false"):
        print(f"1 {note}")
    elif not targetcli.check_targetcli_configuration("auto_add_default_portal"):
        print(f"2 {note}")
    if not targetcli.configure_targetcli("auto_add_mapped_luns=false"):
        print(f"3 {note}")
    elif not targetcli.check_targetcli_configuration("auto_add_mapped_luns"):
        print(f"4 {note}")
    if not targetcli.configure_targetcli("auto_enable_tpgt=true"):
        print(f"5 {note}")
    elif not targetcli.check_targetcli_configuration("auto_enable_tpgt"):
        print(f"6 {note}")


def display_system_status(system):
    system.display_system_status()

def display_version():
    print("version: v1.0.0")

def main():
    parser = argparse.ArgumentParser(description='None')
    parser.add_argument('-d', '--display', action='store_true',
                        help='Enable display_system_status')
    parser.add_argument('-u', '--upgrade', action='store_true',
                        help='Disable system upgrades')
    parser.add_argument('-s', '--service', action='store_true',
                        help='Disable VersaSDS service startup')
    parser.add_argument('-n', '--network', action='store_true',
                        help='Setup Network Manager')
    parser.add_argument('-i', '--initialize', action='store_true',
                        help='Initialize TargetCLI Configuration')
    parser.add_argument('-v', '--version', action='store_true',
                        help='Show version information')
    args = parser.parse_args()

    logger = Logger("log")
    system = System(logger)
    versds = VersaSDS(logger)
    network_manager = NetworkManager(logger)
    targetcli = TargetCLIConfig(logger)

    if args.upgrade:
        disable_system_upgrades(system)
    elif args.service:
        disable_VersaSDS_service_startup(versds)
    elif args.network:
        setup_network_manager(network_manager)
    elif args.initialize:
        initialize_targetcli_configuration(targetcli)
    elif args.display:
        display_system_status(system)
    elif args.version:
        display_version()
    else:
        disable_system_upgrades(system)
        disable_VersaSDS_service_startup(versds)
        setup_network_manager(network_manager)
        initialize_targetcli_configuration(targetcli)


if __name__ == '__main__':
    main()

# if __name__ == '__main__':
#     # 使用 sudo 来运行脚本以获取足够的权限
#     os.system('sudo python your_script.py')
