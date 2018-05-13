# -*- coding: utf-8 -*-
# 默认配置 适用于450级以上

config = {
    "global": {
        "reserve": {
            "gold": 300,  # 保留金币
            "copper": 0,  # 保留银币
            "blower": 0,  # 保留玉石
            "jungong": 0,  # 保留军功
        },
    },
    "mainCity": {
        "auto_get_login_reward": True,  # 自动领取登录奖励(试试手气、登录礼包、登录送礼、恭贺)
        "auto_build_general_tower": True,  # 自动筑造将军塔
        "auto_right_army": True,  # 自动征义兵
    },
    "fete": {
        "auto_fete": True,  # 自动祭祀
        "common": {  # 祭祀到多少金币
            "神农": 0,  # 银币
            "盘古": 0,  # 军功
            "共工": 0,  # 威望
            "伏羲": 0,  # 玉石
            "女娲": 0,  # 宝石
            "Total": 0,  # 大祭祀
        },
        "task15": {  # 祭祀女娲15次任务
            "神农": 0,  # 银币
            "盘古": 0,  # 军功
            "共工": 0,  # 威望
            "伏羲": 0,  # 玉石
            "女娲": 3,  # 宝石
            "Total": 0,  # 大祭祀
        },
        "task50": {  # 祭祀50次任务
            "神农": 1,  # 银币
            "盘古": 1,  # 军功
            "共工": 1,  # 威望
            "伏羲": 2,  # 玉石
            "女娲": 2,  # 宝石
            "Total": 0,  # 大祭祀
        },
    },
    "task": {
        "auto_task": True,  # 自动日常任务
    },
}
