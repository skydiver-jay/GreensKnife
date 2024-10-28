import time
import argparse
import win32file
import ctypes


def status():
    global pipe_name
    pipe = None
    try:
        pipe = win32file.CreateFile(
            pipe_name,
            win32file.GENERIC_WRITE,
            0, None, win32file.OPEN_EXISTING, 0, None
        )
    except:
        print("unlocked\n")
        return

    if pipe is not None:
        print("locked\n")
        win32file.CloseHandle(pipe)
    else:
        print("unlocked\n")


def lock():
    user32 = ctypes.windll.user32
    user32.LockWorkStation()


def unlock():
    global pipe_name, username, password
    pipe = None
    try:
        pipe = win32file.CreateFile(
            pipe_name,
            win32file.GENERIC_WRITE,
            0, None, win32file.OPEN_EXISTING, 0, None
        )
    except:
        print("Could not open pipe.\n")

    if pipe is not None:
        # Send username
        try:
            win32file.WriteFile(pipe, username)
            # win32file.FlushFileBuffers(pipe)
            time.sleep(1)
            # print("write username")
        except:
            print("write pipe error")
            win32file.CloseHandle(pipe)

        # Send password
        try:
            win32file.WriteFile(pipe, password)
            # win32file.FlushFileBuffers(pipe)
            time.sleep(1)
            # print("write password")
        except:
            print("write pipe error")
            win32file.CloseHandle(pipe)
        # 关闭管道
        win32file.CloseHandle(pipe)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", help="操作: status or lock or unlock")
    parser.add_argument("-o", "--operation", help="行动代号")
    parser.add_argument("-u", "--user", help="账号[domain]\\[username]")
    parser.add_argument("-p", "--password", help="密码")
    args = parser.parse_args()

    global pipe_name, username, password

    if args.action.lower() == "status":
        if args.operation is None:
            print("参数错误")
            exit(1)
        pipe_name = "\\\\.\\pipe\\" + args.operation
        status()
        exit(0)
    elif args.action.lower() == "lock":
        lock()
        exit(0)
    elif args.action.lower() == "unlock":
        if args.operation is None or args.user is None or args.password is None:
            print("参数错误")
            exit(1)
        pipe_name = "\\\\.\\pipe\\" + args.operation
        username = args.user + '\0'
        username = username.encode('utf-16-le')
        password = args.password + '\0'
        password = password.encode('utf-16-le')
        unlock()
        exit(0)
    elif args.action.lower() == "test1":
        pipe_name = "\\\\.\\pipe\\" + args.operation
        username = args.user + '\0'
        username = username.encode('utf-16-le')
        password = args.password + '\0'
        password = password.encode('utf-16-le')
        lock()
        time.sleep(5)
        unlock()
        exit(0)
    elif args.action.lower() == "test2":
        pipe_name = "\\\\.\\pipe\\" + args.operation
        username = args.user + '\0'
        username = username.encode('utf-16-le')
        password = args.password + '\0'
        password = password.encode('utf-16-le')
        lock()
        time.sleep(5)
        status()
        time.sleep(5)
        unlock()
        exit(0)

