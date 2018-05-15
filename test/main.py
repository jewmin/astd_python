# -*- coding: utf-8 -*-
import base64
import argparse
import logging
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


def main():
    init_logging()
    parser = argparse.ArgumentParser(description='傲视天地小助手')
    parser.add_argument('--user-name', default="")
    parser.add_argument('--role-name', default="")
    args = parser.parse_args()
    app = App(get_account_config())
    app.init(args.user_name, args.role_name.decode("gbk").encode("utf-8"))
    app.main_loop()
    app.un_init()


if __name__ == "__main__":
    main()
