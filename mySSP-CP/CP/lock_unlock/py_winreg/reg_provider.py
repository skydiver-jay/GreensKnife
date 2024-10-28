import ctypes
import os
import sys
import winreg
import argparse


# 打开或创建一个注册表键
def create_or_open_key(root_key, sub_key):
    try:
        # 尝试打开现有的键
        return winreg.OpenKey(root_key, sub_key, reserved=0, access=winreg.KEY_ALL_ACCESS)
    except FileNotFoundError:
        # 如果键不存在，则创建新的键
        return winreg.CreateKeyEx(root_key, sub_key, reserved=0, access=winreg.KEY_ALL_ACCESS)


# 设置注册表键的值
def set_value(reg_key, value_name, value):
    winreg.SetValueEx(reg_key, value_name, 0, winreg.REG_SZ, value)


# 获取注册表键的值
def get_value(reg_key, value_name):
    value, regtype = winreg.QueryValueEx(reg_key, value_name)
    return value


# 删除注册表键的值
def delete_value(reg_key, value_name):
    winreg.DeleteValue(reg_key, value_name)


# 删除注册表键
def delete_key(root_key, sub_key):
    winreg.DeleteKeyEx(root_key, sub_key, reserved=0, access=winreg.KEY_ALL_ACCESS)


# 判断注册表键是否存在
def is_key_exist(root_key, sub_key):
    try:
        # 尝试打开现有的键
        tmp_key = winreg.OpenKey(root_key, sub_key, reserved=0, access=winreg.KEY_ALL_ACCESS)
        winreg.CloseKey(tmp_key)
        return True
    except FileNotFoundError:
        # 如果键不存在
        return False


def close_key(reg_key):
    if reg_key is not None:
        winreg.CloseKey(reg_key)


def admin():
    aa = ctypes.windll.shell32.IsUserAnAdmin()
    return aa


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", help="add:注册provider, del:取消注册provider")
    parser.add_argument("-n", "--name", help="provider的name")
    parser.add_argument("-p", "--path", help="provider的path")
    parser.add_argument("-i", "--id", help="provider的id:{GUID}")
    args = parser.parse_args()

    rand_id = "{3D0DE0D2-C22F-40E8-9EAC-B999775C2D28}"
    # rand_id = "{8d79fbb0-0e36-4bab-98b4-1fb1d663d6ac}"

    if args.id is not None:
        rand_id = args.id

    root_local_machine = winreg.HKEY_LOCAL_MACHINE
    root_classes_root = winreg.HKEY_CLASSES_ROOT

    sub_key_provider = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Authentication\\Credential Providers\\" + rand_id
    sub_key_clsid = "CLSID\\" + rand_id
    sub_key_clsid_2 = sub_key_clsid + "\\InprocServer32"

    value_1 = "NoninteractiveUnlockCredentialProvider"
    value_1_path = ""
    value_2_key = "ThreadingModel"
    value_2 = "Apartment"

    # print(sub_key_provider)
    # print(sub_key_clsid)
    # print(sub_key_clsid_2)

    if args.name is not None:
        value_1 = args.name

    if args.path is not None:
        value_1_path = args.path
    else:
        # value_1_path = os.path.abspath(os.path.dirname(__file__)) # 使用Pyinstaller打包为可执行文件后，该方法无法获得exe文件的目录
        value_1_path = sys.path[0] # 使用Pyinstaller打包为可执行文件后，该方法无法获得exe文件的目录
    value_1 = value_1_path + "\\" + value_1

    # print(value_1)
    # exit(1)

    def add():
        print("add")
        key_provider = create_or_open_key(root_local_machine, sub_key_provider)
        set_value(key_provider, None, value_1)
        # print("key_provider Value:", get_value(key_provider, None))

        key_clsid = create_or_open_key(root_classes_root, sub_key_clsid)
        key_clsid_2 = create_or_open_key(root_classes_root, sub_key_clsid_2)
        set_value(key_clsid, None, value_1)
        set_value(key_clsid_2, None, value_1 + ".dll")
        set_value(key_clsid_2, value_2_key, value_2)
        # print("key_clsid Value:", get_value(key_clsid, None))
        # print("key_clsid_2 Value:", get_value(key_clsid_2, None))
        # print("key_clsid_2 Value2:", get_value(key_clsid_2, value_2_key))

        close_key(key_provider)
        close_key(key_clsid)
        close_key(key_clsid_2)

    def delete():
        print("del")
        key_provider = create_or_open_key(root_local_machine, sub_key_provider)
        delete_value(key_provider, None)
        delete_key(root_local_machine, sub_key_provider)

        key_clsid = create_or_open_key(root_classes_root, sub_key_clsid)
        key_clsid_2 = create_or_open_key(root_classes_root, sub_key_clsid_2)
        delete_value(key_clsid_2, None)
        delete_value(key_clsid_2, value_2_key)
        delete_key(root_classes_root, sub_key_clsid_2)
        delete_value(key_clsid, None)
        delete_key(root_classes_root, sub_key_clsid)

        close_key(key_provider)
        close_key(key_clsid)
        close_key(key_clsid_2)

    if args.action == "add":
        add()
    elif args.action == "del":
        delete()
    else:
        # print("default: add when provider not exist, del when exist")
        if is_key_exist(root_local_machine, sub_key_provider):
            delete()
        else:
            add()

    # exit(1)

    # if admin() == 1:
    #     print("is admin")
    # else:
    #     ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
