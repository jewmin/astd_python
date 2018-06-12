# -*- coding: utf-8 -*-
# 活动配置 适用于450级以上


activity_config = {
    # 对战
    "KFRank": {
        "enable": True,  # 开启
        "task": {  # 任务 战胜比自己等级高的玩家3次, 胜利25场, 累计获得100积分, 连胜5场
            "enable": True,  # 刷新任务
            "list": [  # 可刷新任务列表
                # "以弱胜强",
                # "胜者为王",
                "突飞猛进",
                # "连胜传奇",
            ],
        },
        "limit_token": 10,  # 每日限制军令<=N
        "ack_formation": "不变阵",  # 攻击阵型 不变阵, 鱼鳞阵, 长蛇阵, 锋矢阵, 偃月阵, 锥形阵, 八卦阵, 七星阵, 雁行阵
        "def_formation": "鱼鳞阵",  # 防御阵型 不变阵, 鱼鳞阵, 长蛇阵, 锋矢阵, 偃月阵, 锥形阵, 八卦阵, 七星阵, 雁行阵
        "def_enable": True,  # 开启积分下降
        "def_score": 800,  # 积分>=N，使用防御阵型
    },
    # 大宴群雄
    "BGEvent": {
        "enable": True,  # 开启
        "limit_cost": 10,  # 花费金币<=N
    },
    # 大练兵
    "Training": {
        "enable": True,  # 开启
    },
    # 抓年兽
    "BombNianEvent": {
        "enable": True,  # 开启
        "reward_index": {"58": 1, "56": 2, "57": 3, "48": 4, "38": 5},  # 奖励领取顺序
        "hp": [120, 60, 10],  # 血量不同
        "bomb": [{3: 1, 2: 2, 1: 3}, {2: 1, 1: 2, 3: 3}, {1: 1, 2: 2, 3: 3}],  # 使用不同鞭炮
        "gold": {1: 2, 2: 0, 3: 0},  # 花费金币<=N
    },
    # 百炼精铁
    "ShenHuo": {
        "enable": True,  # 开启
    },
    # 酒神觉醒
    "YuanDanQiFu": {
        "enable": True,  # 开启
        "gold": 2,  # 花费金币<=N
        "all_open_gold": 10,  # 全开花费金币<=N
        "all_open_fuqi": 200,  # 全开需要福气>=N
    },
    # 抓捕活动
    "ArrestEvent": {
        "enable": True,  # 开启
        "high_gold": 0,  # 使用鞭子花费金币<=N
        "buy_gold": 5,  # 购买抓捕令花费金币<=N
    },
}