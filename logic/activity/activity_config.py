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
        "gold": {1: 1, 2: 0, 3: 0},  # 花费金币<=N
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
    # 充值赠礼
    "GiftEvent": {
        "enable": True,  # 开启
    },
    # 阅兵庆典
    "ParadeEvent": {
        "enable": True,  # 开启
        "round_cost": 0,  # 购买轮数金币<=N
    },
    # 草船借箭
    "BorrowingArrowsEvent": {
        "enable": True,  # 开启
        "unlock": {"0": 4, "1": 1, "2": 2, "3": 3},  # 开启宝箱顺序，"镔铁", "点卷", "宝物", "宝石"
        "cost_limit": 150000,  # 邀功花费军功<=N
        "sail_gold": 5,  # 发船花费金币<=N
        "arrow_diff": 10000,  # 承重差<=N
    },
    # 新年敲钟
    "RingEvent": {
        "enable": True,  # 开启
        "cost": 5,  # 敲钟花费金币<=N
        "reward": 1,  # 奖励选项 1:大将令 2:镔铁
    },
    # 武斗会
    "KfWD": {
        "enable": True,  # 开启
    },
    # 百家宴
    "DuanWuEvent": {
        "enable": True,  # 开启
        "gold_hunger": 3,  # 粽子花费金币<=N
        "limit_hunger": 8,  # 免费粽子，饥饿度<=N
        "gold_round": 0,  # 轮数花费金币<=N
        "general": ["成吉思汗", "李白", "张良", "项羽"],  # 大将令列表
    },
    # 宝塔活动
    "TowerStage": {
        "enable": True,  # 开启
        "tower": 1,  # 选择宝塔 0'青龙镇国塔' 1'白虎伏灵塔' 2'朱雀迎瑞塔' 3'玄武定运塔'
    },
    # 武斗庆典
    "KFEvent": {
        "enable": True,  # 开启
    },
    # 群雄煮酒
    "QingMingEvent": {
        "enable": True,  # 开启
        "buycost": 10,  # 购买轮数花费金币<=N
        "golddrinkcost": 0,  # 酒仙附体花费金币<=N
        "golddrink": [True, True, True, True, True, True, True, False],  # 酒仙附体限制
        "drink": [30, 40, 50, 60, 70, 75, 95, 999],  # 醉意限制
    },
    # 宝石倾销
    "DumpEvent": {
        "enable": True,  # 开启
    },
    # 赏月送礼
    "MoonGeneralEvent": {
        "enable": True,  # 开启
        "buyroundcost": 0,  # 购买轮数花费金币<=N
        "cakecost": 0,  # 送礼花费金币<=N
    },
    # 超级翻牌
    "SuperFanPai": {
        "enable": True,  # 开启
        "buyall": 20,  # 卡牌全开花费金币<=N
        "superlv": 18,  # 卡牌全开限制，宝石等级>=N
        "buyone": 5,  # 购买次数花费金币<=N
    },
    # 消费送礼
    "DoubleElevenEvent": {
        "enable": True,  # 开启
    },
    # 宝石翻牌
    "GemCard": {
        "enable": True,  # 开启
        "comboxs": 5,  # 组合倍数>=N
        "total": 9,  # 卡牌总值>=N
        "buygold": 0,  # 购买次数花费金币<=N
        "doublecost": 0,  # 翻倍花费金币<=N
        "upgradegold": 0,  # 升级花费金币<=N
        "combo": [111, 222, 333, 444, 555, 123, 234, 345],  # 组合
        "upgrade": {  # 升级组合
            113: 1,
            122: 2,
            134: 0,
            224: 1,
            233: 2,
            245: 0,
            335: 1,
            344: 2,
            455: 0,
        },
    },
    # 雪地通商
    "SnowTrading": {
        "enable": True,  # 开启
        "choose": 1,  # 选择奖励 1:镔铁 2:点券
        "reinforce": {  # 加固雪橇
            "enable": False,  # 开启
            "cost": 0,  # 加固雪橇花费金币<=N
            "type": 3,  # 宝箱类型>=N 1:木质 2:白银 3:黄金
        },
        "buyroundcost": 5,  # 购买次数花费金币<=N
    },
    # 群雄争霸
    "KFZB": {
        "enable": True,  # 开启
    },
    # 盛宴活动
    "GoldGiftType": {
        "enable": True,  # 开启
        "buyjoingold": 0,  # 购买盛宴次数花费金币<=N
    },
    # 英雄帖
    "KfPVP": {
        "enable": True,  # 开启
    },
    # 中秋月饼
    "EatMoonCakeEvent": {
        "enable": True,  # 开启
        "gold": 4,  # 花费金币<=N
    },
}
