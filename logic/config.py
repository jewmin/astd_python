# -*- coding: utf-8 -*-
# 默认配置 适用于450级以上

config = {
    "global": {
        "reserve": {
            "gold": 300,  # 保留金币
            "copper": 50000000,  # 保留银币
            "blower": 300000,  # 保留玉石
            "jungong": 10000000,  # 保留军功
        },
    },
    "mainCity": {
        "auto_get_login_reward": True,  # 自动领取登录奖励(今日手气、礼包、登录送礼、恭贺、俸禄)
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
    "reward": {
        "name": ["type:0", "银币", "玉石", "type:3", "type:4", "宝石", "兵器", "兵器碎片", "征收次数", "纺织次数",
                 "通商次数", "炼化次数", "兵力减少", "副本重置卡", "战役双倍卡", "强化暴击卡", "强化打折卡", "兵器提升卡", "兵器暴击卡", "type:19",
                 "type:20", "type:21", "type:22", "type:23", "type:24", "攻击令", "type:26", "进货令", "军令", "政绩翻倍卡",
                 "征收翻倍卡", "商人召唤卡", "纺织翻倍卡", "type:33", "行动力", "摇钱树", "超级门票", "type:37", "宝物", "金币",
                 "type:40", "type:41", "点券", "神秘宝箱", "家传玉佩", "type:45", "type:46", "type:47", "铁锤", "大将令",
                 "镔铁", "专属装备", "type:52", "type:53", "type:54", "type:55", "觉醒酒", "磨砺石", "紫晶石"]
    },
    "impose": {
        "auto_impose": True,  # 自动征收
        "impose_event": ("金币", "征收", "民忠", "银币", "威望"),  # 征收事件回答优先顺序
        "reserve": 30,  # 征收次数>N
        "force": 0,  # 强征金币<=N
        "finish_task": True,  # 完成日常任务
    },
    "market": {
        "auto_buy_item": True,  # 自动购买
        "withdraw_gold_item": True,  # 下架金币商品
        "withdraw_discount_fail": {"enable": True, "gold": True, "copper": False},  # 下架还价失败商品
        "buy_special_item": True,  # 购买特供商品
        "supplement_item": {"enable": True, "limit": 15},  # 商品数量<=N，使用进货令
        "gift": {  # 赠送商品
            "enable": True,
            "list": [
                "打折券",
                "玉石",
                "宝石",
                # "批发券",
                "无敌将军炮",
                "五毒问心钉",
                "玄霆角",
                "七戮锋",
                "落魂冥灯",
                "蟠龙华盖",
                "轩辕指南车",
            ],
        },
    },
    "tickets": {
        "auto_exchange": True,  # 自动兑换点券商品
        "hero": {
            "enable": True,  # 兑换大将令
            "list": [
                "赵匡胤", "武则天", "狄仁杰", "玄奘", "李白",
                "蚩尤", "黄帝", "后羿", "夏桀", "商汤",
                "姜子牙", "墨子", "秦始皇", "荆轲", "鬼谷子",
                "曹操", "诸葛亮", "项羽", "张良", "成吉思汗"
            ],
            "limit_tickets": 300000,  # 花费点券<=N
        },
        "once_on_day": {
            "enable": True,  # 每天一次
            "list": {
                "军功": 0,  # sell type
                "玉石": 0,  # sell type
            },
        },
        "more_on_day": {
            "enable": True,  # 每天多次
            "list": {
                "银币": 0,  # sell type
                "玉石": 1,  # sell type
                "无敌将军炮": 1,  # sell type
            },
        },
    },
}
