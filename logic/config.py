# -*- coding: utf-8 -*-
# 默认配置 适用于450级以上

config = {
    "global": {
        "reserve": {
            "gold": 300,  # 保留金币
            "copper": 50000000,  # 保留银币
            "blower": 300000,  # 保留玉石
            "jungong": 10000000,  # 保留军功
            "tickets": 100000000,  # 点券
        },
    },
    "mainCity": {
        "auto_get_login_reward": True,  # 自动领取登录奖励(今日手气、礼包、登录送礼、恭贺、俸禄)
        "auto_build_general_tower": True,  # 自动筑造将军塔
        "auto_right_army": True,  # 自动征义兵
        "auto_apply_token": True,  # 自动领取军令
        "build_list": ["纺织局", "铁匠铺", "招商局", "军机处", "商店", "钱庄", "账房", "账房二", "铸币厂", "兵营", "校场", "校场二", "校场三", "银库一", "银库二", "民居一", "民居二", "民居三", "民居四", "民居五", "民居六", "民居七", "民居八", "民居九", "民居十", "货仓", "城墙"],  # 建造列表，只建造列表中的建筑
    },
    "outCity": {
        "auto_end_bao_shi_pick": True,  # 自动采集宝石
        "end_pick_proportion": 0.5,  # 采集比例>=N
        "auto_tech_research": True,  # 自动技术研究
        "jail_baoshi": True,  # 监狱劳作优化宝石
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
        "event": {  # 祭祀活动
            "神农": 0,  # 银币
            "昊天": 3,  # 行动力
            "轩辕": 2,  # 点券
            "伏羲": 0,  # 玉石
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
                # "批发券",
                # "横扫卷",
                "玉石",
                "宝石",
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
    "active": {
        "reserve": 100,  # 保留行动力<=N
        "sort": ["royalty", "refine_bin_tie", "refine", "caravan"],  # 执行顺序
        "royalty": {  # 纺织
            "enable": True,  # 开启功能
            "finish_task": True,  # 完成日常任务
            "do_high": True,  # 高效状态
            "do_tired": True,  # 疲劳状态
            "refresh": 0,  # 刷新换购商人花费金币<=N
            "list": [  # 换购商人列表
                # "皇家南越商人",
                # "皇家大理商人",
                # "皇家关东商人",
                # "皇家楼兰商人",
                "稀有黑市商人",
            ],
            "cost": [  # 换购列表
                # {"type": 58, "lv": 1, "num": 400, "needweavenum": 650},  # 紫晶石 皇家南越商人
                # {"type": 57, "lv": 1, "num": 120, "needweavenum": 600},  # 磨砺石 皇家大理商人
                # {"type": 56, "lv": 1, "num": 30, "needweavenum": 550},  # 觉醒酒 皇家关东商人
                # {"type": 38, "lv": 50, "num": 3, "needweavenum": 260},  # 日月光华 皇家楼兰商人
                {"type": 51, "lv": 5, "num": 1, "needweavenum": 4500},  # 5星专属 稀有黑市商人
            ],
        },
        "refine_bin_tie": {  # 炼制
            "enable": True,  # 开启功能
            "finish_task": True,  # 完成日常任务
            "do_high": True,  # 高效状态
            "do_tired": False,  # 疲劳状态
            "mode": 2,  # 炼制模式 1:镔铁 2:铁锤
        },
        "refine": {  # 精炼
            "enable": True,  # 开启功能
            "finish_task": True,  # 完成日常任务
            "do_high": False,  # 高效状态
            "do_tired": False,  # 疲劳状态
            "refresh_refiner": {  # 升级精炼工人
                "per_cost": 0,  # 花费金币<=N
                "list": {
                    "100": 0,  # 红紫紫 -> 紫紫紫
                    "211": 2,  # 黄红红 -> 黄红紫
                    "220": 1,  # 黄黄紫 -> 黄红紫
                    "331": 1,  # 绿绿红 -> 绿黄红
                    "332": 1,  # 绿绿黄 -> 绿黄黄
                    "310": 1,  # 绿红紫 -> 黄红紫
                    "410": 1,  # 蓝红紫 -> 蓝紫紫
                    "421": 1,  # 蓝黄红 -> 蓝红红
                    "433": 2,  # 蓝绿绿 -> 蓝绿黄
                    "441": 2,  # 蓝蓝红 -> 蓝蓝紫
                    "442": 2,  # 蓝蓝黄 -> 蓝蓝红
                },
            },
        },
        "caravan": {  # 通商
            "enable": True,  # 开启功能
            "finish_task": True,  # 完成日常任务
            "event": {  # 通商事件
                "1": {  # 西域国王
                    "double_cost": 0,  # 双倍领取金币<=N
                },
                "2": {  # 神秘商人
                    "use_cost": 0,  # 花费金币<=N
                },
                "3": {  # 西域通商
                    "double_cost": 0,  # 双倍领取金币<=N
                },
            },
            "limit": {  # 限制
                "gold": 0,  # 金币<=N
                "copper": 3000000,  # 银币<=N
                "active": 60,  # 行动力<=N
                "max_reserve": 200,  # 当通商完成还有很多行动力时，保留行动力<=N
            },
        },
    },
    "dayTreasureGame": {  # 王朝寻宝
        "enable": True,  # 自动寻宝
        "active_proportion": 0.75,  # 行动力比例<=N
    },
    "world": {  # 世界
        "apply_att_token": {  # 领取攻击令
            "enable": True,  # 开启
            "proportion": 0.125,  # 攻击令比例<=N
        },
        "tu_city": {  # 屠城
            "enable": True,  # 开启
            "people_num": 10,  # 城池人数<=N
            "proportion": 0.125,  # 攻击令比例<=N，随机屠城
        },
        "score": {  # 战绩
            "enable": True,  # 开启
        },
        "fengdi": {  # 封地
            "enable": True,  # 开启
            "big": ["李白", "成吉思汗", "项羽"],  # 优化大将令，不在列表内则觉醒酒
            "cd": 600000,  # 封地冷却时间>=N
        },
        "nation_task": {  # 攻坚战
            "enable": True,  # 开启
        },
        "city_event": {  # 悬赏
            "enable": True,  # 开启
            "star": 5,  # 最大星级<=N
            "reserve": 0,  # 保留悬赏次数<=N
        },
        "use_token": {  # 使用个人令
            "enable": True,  # 开启
            "list": ["1", "4", "8"],  # 使用类型
        },
        "treasure": {  # 国家宝箱
            "enable": True,  # 开启
            "reserve": 100,  # 保留宝箱<=N
            "arrest_reserve": 30,  # 屠城时，保留宝箱<=N
            "proportion": 0.125,  # 开启宝箱条件，攻击令比例<=N
        },
        "attack": {  # 攻击
            "enable": True,  # 开启
            "exculde": ["许都", "成都", "武昌"],  # 排除三国主城
            "ignore_arrest": True,  # 忽略被抓的不打
            "main_city": [0, 112, 113, 134],  # 三国对应都城
            "near_main_city": [[], [114, 119, 107, 128, 133, 135], [128, 133, 135, 111, 118], [114, 119, 107, 111, 118]],  # 三国对应都城附近
            "reserve_transfer_cd_clear_num": 10,  # 保留移动cd清除次数
            "lost_times": 5,  # 停止对此人攻击，当失败次数>=N
            "diff_level": 20,  # 决斗相差等级
            "duel_city_hp_limit": 80,  # 不能决斗，当城防<=N
        },
    },
    "dinner": {  # 宴会
        "enable": True,  # 开启
    },
    "equip": {  # 强化
        "war_chariot": {  # 战车
            "enable": True,  # 开启
            "only_use_hammer": True,  # 只用铁锤强化
            "hammer_level": 4,  # 使用铁锤暴击<=N
            "auto_exchange_weapon": True,  # 自动兑换兵器
            "auto_exchange_bowlder": True,  # 自动兑换玉石
            "equipment_num": 20000,  # 兵器<=N
        },
        "special_equip": {  # 装备铸造
            "enable": True,  # 开启
            "firstcost": 0,  # 铸造花费金币<=N
            "secondcost": 0,  # 精火铸造花费金币<=N
            "smelt": {  # 熔化条件
                "quality": 5,  # 品质<=N
                "level": 3,  # 等级<=N
            },
        },
        "polish": {  # 炼化
            "polish": {  # 炼化玉佩
                "enable": True,  # 开启
                "use_gold": True,  # 使用金币炼化
                "need_attrs": {  # 炼化次数对应最低属性
                    "0": 5,
                    "1": 7,
                    "2": 9,
                    "3": 11,
                    "4": 13,
                    "5": 15,
                    "6": 20,
                    "7": 25,
                    "8": 30,
                    "9": 35,
                },
            },
            "baowu": {  # 家传玉佩
                "enable": True,  # 强化家传玉佩
            },
            "specialtreasure": {  # 专属玉佩
                "enable": True,  # 强化专属玉佩
                "reverse": 30,  # 保留N个0属性专属玉佩
                "attribute": [  # 专属玉佩技能要求
                    "全攻系数", "全防系数", "普攻系数", "战法系数", "策略系数",
                    "普通攻击", "战法攻击", "策略攻击",
                    # "普通防御", "战法防御", "策略防御",
                    # "兵力", "格挡", "闪避", "暴击"
                ],
            },
        },
        "monkey": {  # 套装
            "enable": True,  # 开启
            "use_tickets": 300000,  # 花费点券<=N
            "reverse_tickets": 1000000000,  # 保留点券
        },
        "crystal": {  # 水晶石进阶
            "enable": True,  # 开启
            "level": 106,  # 水晶石等级>=N
        },
        "goods": {  # 仓库
            "enable": True,  # 开启
            "draw": ["日月光华", "家传玉佩"],  # 取出物品列表
        },
        "zhuge": {  # 淬炼
            "enable": True,  # 开启
        },
    },
    "general": {  # 武将
        "wash": {  # 培养
            "enable": True,  # 开启
            "diff_attr": 1,  # 属性差<=N，结束洗练
        },
        "awaken": {  # 觉醒
            "enable": True,  # 开启
            "use_stone": True,  # 使用觉醒酒
            "only_awaken": True,  # 觉醒后停止
        },
        "tech": {  # 科技
            "enable": True,  # 开启
            "list": ["大将强攻", "大将强防"],  # 允许科技
        },
        "big": {  # 大将
            "enable": True,  # 开启
            "fast_train": 1,  # 突飞花费大将令
            "new_train": 10,  # 突破花费大将令
            "dict": {
                "李白": 1000,
                "成吉思汗": 1100,
                "项羽": 1200,
                "黄帝": 1300,
                "夏桀": 1400,
                "后羿": 1500,
                "墨子": 1600,
                "张良": 1700,
                "鬼谷子": 1800,
                "荆轲": 1900,
                "商汤": 2000,
                "蚩尤": 2100,
                "姜子牙": 2200,
                "秦始皇": 2300,
                "王翦": 2400,
                "李牧": 2500,
                "曹操": 2600,
                "伏羲": 2700,
                "炎帝": 2800,
                "大禹": 2900,
                "周文王": 3000,
                "西施": 3100,
                "吕布": 3200,
                "赵云": 3300,
                "蒙恬": 3400,
                "张辽": 3500,
                "典韦": 3600,
                "白起": 3700,
            },
        },
    },
    "battle": {  # 征战
        "enable": True,  # 开启
        "armyid": 14919,  # 征战NPC
        "powerid": 133,  # 征战地图从360周易演成开始
    },
}
