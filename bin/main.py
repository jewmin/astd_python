# -*- coding: utf-8 -*-
import base64
import argparse
import logging
from logging.handlers import RotatingFileHandler
from model.account import Account
from model.enum.server_type import ServerType
from framework.app import App


def get_account_config():
    account_list = list()
    with open("account.ini", "r") as fd:
        lines = fd.readlines()
        for line in lines:
            line = line.strip()
            if len(line) == 0 or line.startswith("#"):
                continue
            index = line.find("=")
            if index == -1:
                continue
            key = line[:index]
            value = line[index + 1:]
            if key is None or value is None or len(key) == 0 or len(value) == 0:
                continue
            account = handle_account_config(key, value)
            if account is not None:
                account_list.append(account)
    return account_list


def handle_account_config(key, value):
    if key.lower() == "account":
        contents = value.split(":")
        if len(contents) >= 8:
            account = Account()
            account.m_eServerType = eval("ServerType.{}".format(contents[0]))
            account.m_nServerId = int(contents[1])
            account.m_szUserName = contents[2]
            account.m_szPassword = base64.b64decode(contents[3])
            account.m_szRoleName = contents[7]
            return account


def init_logging():
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s %(filename)s [%(levelname)s] %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        filename="astd.log",
                        when="D",
                        interval=1)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s %(filename)s [%(levelname)s] %(message)s")
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

    rotating = RotatingFileHandler(filename="error.log", maxBytes=1048576)
    rotating.setLevel(logging.ERROR)
    rotating.setFormatter(formatter)
    logging.getLogger().addHandler(rotating)

    warning_rotating = RotatingFileHandler(filename="warning.log", maxBytes=1048576)
    warning_rotating.setLevel(logging.WARNING)
    warning_rotating.setFormatter(formatter)
    logging.getLogger().addHandler(warning_rotating)


def init_pycharm_debug():
    import pydevd
    ip = "127.0.0.1"
    port = 18800
    logging.getLogger().info("init_pycharm_debug begin, connecting to pycharm(ip={}, port={})...".format(ip, port))
    pydevd.settrace(ip, port=port, stdoutToServer=False, stderrToServer=True, suspend=False)
    logging.getLogger().info("init_pycharm_debug end, connected to pycharm")


def handle_cmd(key, value, app_list):
    try:
        func_name, args = None, tuple()
        if key == "start":
            func_name = "start"
        elif key == "stop":
            func_name, args = "stop", (True,)
        elif key == "relogin":
            func_name = "start_re_login"

        if value == "all":
            for app in app_list:
                func = getattr(app, func_name)
                func(args)
        else:
            value = int(value)
            if value < len(app_list):
                func = getattr(app_list[value], func_name)
                func(args)
    except Exception as ex:
        print("执行命令出错：{}".format(str(ex)))


def main():
    init_logging()
    parser = argparse.ArgumentParser(description='傲视天地小助手')
    parser.add_argument('--user-name', default="")
    parser.add_argument('--role-name', default="")
    parser.add_argument('--enable-debug', default=False)
    args = parser.parse_args()
    account_list = get_account_config()
    user_names = args.user_name.split(",")
    role_names = args.role_name.decode("gbk").encode("utf-8").split(",")
    if args.enable_debug:
        init_pycharm_debug()
    if len(user_names) != len(role_names):
        logging.getLogger().error("参数不对，账号与角色数量不匹配")
    else:
        app_list = list()
        for index, user_name in enumerate(user_names):
            app = App(account_list, str(index))
            app.init(user_name, role_names[index])
            app_list.append(app)

        while True:
            cmd = input("请输入命令：退出(quit)、启动(start)、暂停(stop)、重新登录(relogin)")
            if cmd.startswith("quit"):
                break
            elif cmd.startswith("start") or cmd.startswith("stop") or cmd.startswith("relogin"):
                index = cmd.find("=")
                if index == -1:
                    continue
                key = cmd[:index]
                value = cmd[index + 1:]
                handle_cmd(key, value, app_list)

        for app in app_list:
            app.un_init()


if __name__ == "__main__":
    main()
